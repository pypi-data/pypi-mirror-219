import boto3
import logging
import subprocess


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_instance(instance_id):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    if instance.state['Name'] == 'running':
        logger.info(f'Instance {instance_id} is already running')
        return 'running'
    instance.start()
    logger.info(f'Starting instance {instance_id}')
    instance.wait_until_running()
    logger.info(f'Instance {instance_id} is now running')

def stop_instance(instance_id):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    if instance.state['Name'] == 'stopped':
        logger.info(f'Instance {instance_id} is already stopped')
        return False
    instance.stop()
    logger.info(f'Stopping instance {instance_id}')
    instance.wait_until_stopped()
    logger.info(f'Instance {instance_id} has been stopped')
    return True


def get_instance_info(instance_id):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    instance_info = {
        'Instance ID': instance.id,
        'Instance Type': instance.instance_type,
        'Availability Zone': instance.placement['AvailabilityZone'],
        'Launch Time': instance.launch_time.strftime('%Y-%m-%d %H:%M:%S'),
        'State': instance.state['Name'],
        'Public IP Address': instance.public_ip_address,
        'Private IP Address': instance.private_ip_address
    }
    return instance_info

def ssh_to_instance(instance_id, username, private_key_file):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    ip_address = instance.public_ip_address
    ssh_command = f'ssh -i {private_key_file} {username}@{ip_address}'
    logger.info(f'SSHing into instance {instance_id}')
    subprocess.run(ssh_command.split(), check=True)

