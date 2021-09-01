from fastapi import FastAPI
from common.config import Config

from scripts.lambdas.initial_setup import setup

from views.schedules import router as schedules_router


def get_application() -> FastAPI:
    
    setup()
    
    app = FastAPI()
    
    app.include_router(schedules_router)
    
    @app.get("/")
    async def root():
        import boto3
        cfg = Config()
        
        clt = boto3.resource('ec2', aws_access_key_id=cfg.aws_access_key_id.get_secret_value(),
                           aws_secret_access_key=cfg.aws_secret_access_key.get_secret_value(), region_name='us-east-2')
        ids = ["i-0baefa4c6941972d2"]
        resp = clt.instances.all().terminate()
        
        print(resp)
        
        return {"message": "Hello World " + cfg.aws_access_key_id.get_secret_value() + " " + cfg.aws_secret_access_key.get_secret_value()}
    
    return app