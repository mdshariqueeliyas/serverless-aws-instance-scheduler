import boto3

def lambda_handler(event, context):
    
    instances = event.get("instance_ids") or []
    state = event.get("state")
    
    ec2 = boto3.client('ec2')
    
    if state == "running":
        ec2.start_instances(InstanceIds=instances)
    elif state == "stopped":
        ec2.stop_instances(InstanceIds=instances)
    