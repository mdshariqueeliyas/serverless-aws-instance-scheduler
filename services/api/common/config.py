from pydantic import SecretStr, BaseSettings, StrictStr

class Config(BaseSettings):
    
    # aws auth config
    aws_access_key_id: SecretStr
    aws_secret_access_key: SecretStr
    aws_region: StrictStr
    
    # aws related config
    policy_name: StrictStr = "InstanceSchedulerPolicy"
    role_name: StrictStr = "InstanceSchedulerRole"
    lamda_function_name: StrictStr = "InstanceSchedulerLambda"
    lamda_function_arn: StrictStr = ""
    
    
    cloud_watch_prefix: StrictStr = "instance_scheduler_"
    

config = Config()