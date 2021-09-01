import pathlib
import time

from models.iam import IAM
from models.lambdas import Lambda, LambdaSetup

from common.config import config


LAMBDA_POLICY = '''{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Start*",
                "ec2:Stop*"
            ],
            "Resource": "*"
        }
    ]
}'''

ASSUME_ROLE_POLICY = '''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'''

def setup():
    iam =IAM()
    
    policy_arn = iam.get_policy_arn()
    policy = iam.get_policies(arn = policy_arn)
    if policy is None:
        # create policy
        policy = iam.create_policies(config.policy_name, policy=LAMBDA_POLICY)
    
    role = iam.get_role(config.role_name)
    if role is None:
        role = iam.create_role(
            name=config.role_name,
            assume_role_policy=ASSUME_ROLE_POLICY
        )
        iam.attach_policy_to_role(
            config.role_name,
            policy_arn=policy['Policy']['Arn']
        )
    time.sleep(10)
    lambdas = Lambda()
    lambda_function = lambdas.get_lambdas(name=config.lamda_function_name)
    
    if lambda_function is None:
        lambda_setup = LambdaSetup()
        
        lambda_dir = pathlib.Path(__file__).parent
    
        lambda_code = lambda_dir.joinpath('change_state_of_ec2.py').resolve()
        lambda_zip = lambda_dir.joinpath('change_state_of_ec2.zip').resolve()
        
        lambda_setup.create_zip(lambda_code, lambda_zip)
        lambda_zip_content = lambda_setup.read_zipped_file(lambda_zip)
        
        lambda_function = lambdas.create_lambda(
            name=config.lamda_function_name,
            role=role['Role']['Arn'],
            lambda_zipped=lambda_zip_content
        )
        
        config.lamda_function_arn = lambda_function['FunctionArn']
    else:
        config.lamda_function_arn = lambda_function['Configuration']['FunctionArn']
        
    
        