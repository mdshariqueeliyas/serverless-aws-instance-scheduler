from common.aws_session import aws_session



class EC2:
    client = None
    instance_id = None
    
    def __init__(self, session = None, instance_id = None) -> None:
        self.instance_id = instance_id
        if session is None:
            self.client = aws_session.client('ec2')
        else:
            self.client = session.client('ec2')
        
    def start(self):
        self.client.stop_instances(InstanceIds=[self.instance_id])
    
    def stop(self):
        self.client.start_instances(InstanceIds=[self.instance_id])
    
    
    
    

