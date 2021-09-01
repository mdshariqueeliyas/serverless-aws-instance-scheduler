import boto3
from boto3.session import Session
from common.config import config

aws_session = Session(aws_access_key_id=config.aws_access_key_id.get_secret_value(),
                      aws_secret_access_key=config.aws_secret_access_key.get_secret_value(),
                      region_name=config.aws_region)