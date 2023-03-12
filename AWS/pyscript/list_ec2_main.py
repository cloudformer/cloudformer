import boto3
import json

region = 'ap-east-1'

# 创建 EC2 客户端
ec2 = boto3.client('ec2', region_name=region)

# 使用 describe_instances 方法列出所有 EC2 实例
response = ec2.describe_instances()

# 提取所有实例的信息并整理为 JSON 格式
instances = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_info = {
            'instance_id': instance['InstanceId'],
            'instance_type': instance['InstanceType'],
            'state': instance['State']['Name'],
            'instance_platform': instance['PlatformDetails'],
            'instance_PublicIp': instance['PublicIpAddress'],
            'launch_time': instance['LaunchTime'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        instances.append(instance_info)
json_result = json.dumps(instances, indent=4)
print(json_result)
