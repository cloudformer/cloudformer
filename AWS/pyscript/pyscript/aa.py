import boto3
import json

def list_ec2(region = 'ap-east-1'):
    # 创建 EC2 客户端
    ec2 = boto3.client('ec2', region_name=region)

    # 使用 describe_instances 方法列出所有 EC2 实例
    response = ec2.describe_instances()

    print(response)
    # 提取所有实例的信息并整理为 JSON 格式     # 修改get的到字典的对象
    instances = []
    # for reservation in response['Reservations']:
    #     for instance in reservation['Instances']:
    #         # instance_info = {
    #         #     'region': region,
    #         #     'AvailabilityZone' : instance.get('Placement')['AvailabilityZone'],
    #         #     'instance_id': instance.get('InstanceId'),
    #         #     'instance_type': instance.get('InstanceType'),
    #         #     'state': instance.get('State')['Name'],
    #         #     'instance_platform': instance.get('PlatformDetails'),
    #         #     'instance_PublicIp': instance.get('PublicIpAddress'),
    #         #     'launch_time': instance.get('LaunchTime').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #         # }
    #         # instances.append(instance_info)
    #         print('1')
    # json_result = json.dumps(instances, indent=4)
    # return json_result
if __name__ == '__main__':
    list_ec2()