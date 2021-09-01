import botocore
from common.aws_session import aws_session
from common.config import config


class STS:
    client = None
    
    def __init__(self, client = None) -> None:
        self.client = client
        if self.client is None:
            self.client = aws_session.client('sts')
    
    def get_account_id(self):
        return self.client.get_caller_identity().get('Account')
    


class IAM:
    client = None
    
    def __init__(self, client = None) -> None:
        self.client = client
        if self.client is None:
            self.client = aws_session.client('iam')
    
    def get_policy_arn(self):
        sts = STS()
        return "arn:aws:iam::%s:policy/%s" % (sts.get_account_id(), config.policy_name)
    
    def get_policies(self, arn):
        try:
            response = self.client.get_policy(
                PolicyArn=arn
            )
            return response
        except self.client.exceptions.NoSuchEntityException:
            pass
    
    def create_policies(self, name, policy):
        response = self.client.create_policy(
            PolicyName=name,
            PolicyDocument= str(policy),
            Description='access for lambda function to change state of ec2',
        )
        return response
    
    def get_role(self, name):
        try:
            response = self.client.get_role(
                RoleName=name
            )
            return response
        except Exception as e:
            pass
    
    def create_role(self, name, assume_role_policy, description=""):
        response = self.client.create_role(
            RoleName=name,
            AssumeRolePolicyDocument=assume_role_policy,
            Description=description,
        )
        return response
    
    def attach_policy_to_role(self, name, policy_arn):
        response = self.client.attach_role_policy(
            RoleName=name,
            PolicyArn=policy_arn
        )
        return response
