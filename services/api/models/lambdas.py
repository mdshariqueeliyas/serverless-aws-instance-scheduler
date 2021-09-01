import json
import zipfile
from common.aws_session import aws_session



class Lambda:
    session = None
    client = None
    def __init__(self, session = None) -> None:
        self.session = session
        if self.session is None:
            self.session = aws_session
        
        self.client = self.session.client('lambda')
    
    def create_lambda(self, name, role, lambda_zipped, description = ""):
        response = self.client.create_function(
            FunctionName=name,
            Runtime='python3.9',
            Role=role,
            Handler= "lambda_function.lambda_handler",
            Code={
                'ZipFile': lambda_zipped
            },
            Description=description,
        )
        return response
    
    def get_lambdas(self, name):
        try:
            return self.client.get_function(FunctionName=name)
        except Exception as e:
            return None


class LambdaSetup:
    
    @staticmethod
    def create_zip(input_file_path, output_path):
        with zipfile.ZipFile(output_path, 'w') as zf:
            zf.write(input_file_path, arcname='lambda_function.py')
    
    @staticmethod
    def read_zipped_file(zip_file_path):
        content = None
        with open(zip_file_path, 'rb') as f: 
            content = f.read()
        return content
