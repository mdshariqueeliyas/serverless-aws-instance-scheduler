from common.aws_session import aws_session
from common.config import config

from pydantic import BaseModel
from enum import Enum


class Status(str, Enum):
    RUNNING = 'RUNNING'
    STOPPED = 'STOPPED'


class Day(str, Enum):
    
    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"


DAY_MAPPING = {
    Day.SUNDAY: 1,
    Day.MONDAY: 2,
    Day.TUESDAY: 3,
    Day.WEDNESDAY: 4,
    Day.THURSDAY: 5,
    Day.FRIDAY: 6,
    Day.SATURDAY: 7
}

class UpdateSchedule(BaseModel):
    status: Status
    day: Day
    description: str = ""


class CreateSchedule(UpdateSchedule):
    instance_id: str


class CloudWatch:
    client = None
    
    def __init__(self, session = None) -> None:
        if session is None:
            self.client = aws_session.client('events')
        else:
            self.client = session.client('events', region_name=config.aws_region)
    
    @staticmethod
    def get_rule_name(instance_id: str):
        return config.cloud_watch_prefix + instance_id
    
    def add_lambda(self, instance_id, state):
        response = self.client.put_targets(
            Rule=self.get_rule_name(instance_id),
            Targets=[{
                "Id" : config.lamda_function_name,
                "Arn" : config.lamda_function_arn,
                "Input" : '''{
                    "instance_ids" : ["%s"],
                    "state": "%s"
                }''' % (instance_id, state)
            }]
        )
        return response
        
    def list_schedules(self, instance_id=None):
        if instance_id and len(instance_id):
            return self.client.list_rules(NamePrefix=self.get_rule_name(instance_id))
        return self.client.list_rules()
    
    def create_schedule(self, name: str, day: int, enabled: Status, description: str = ""):
        resp = self.client.put_rule(
            Name=name,
            ScheduleExpression=f'cron(0 0 ? * {day} *)',
            State=enabled,
            Description=description,
        )
        return resp
    
    def delete_schedule(self, name:str):
        self.client.delete_rule(Name=name)
    