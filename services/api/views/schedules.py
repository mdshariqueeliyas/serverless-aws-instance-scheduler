from models.cloud_watch import CloudWatch, CreateSchedule, UpdateSchedule, DAY_MAPPING

from common.config import config

from fastapi.routing import APIRouter

router = APIRouter(prefix="/schedules")

@router.get("/")
def get_schedules():
    cloud_watch = CloudWatch()
    return cloud_watch.list_schedules()

@router.get("/{instance_id:str}")
def get_schedule(instance_id: str):
    cloud_watch = CloudWatch()
    return cloud_watch.list_schedules(instance_id=instance_id)

@router.post("/")
def create_schedule(body: CreateSchedule):
    cloud_watch = CloudWatch()
    cloud_watch.create_schedule(
        cloud_watch.get_rule_name(body.instance_id),
        DAY_MAPPING[body.day],
        "ENABLED",
        body.description
    )
    return cloud_watch.add_lambda(instance_id=body.instance_id, state=body.status)

@router.put("/{instance_id:str}")
def update_schedule(instance_id: str, body: UpdateSchedule):
    cloud_watch = CloudWatch()
    return cloud_watch.create_schedule(
        cloud_watch.get_rule_name(instance_id),
        DAY_MAPPING[body.day],
        "ENABLED",
        body.description
    )
    
@router.delete("/{instance_id:str}")
def delete_schedule(instance_id: str):
    cloud_watch = CloudWatch()
    cloud_watch.delete_schedule(name = cloud_watch.get_rule_name(instance_id))