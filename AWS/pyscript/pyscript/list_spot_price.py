import boto3
import json
from datetime import datetime, timedelta

region = 'us-west-2'
start_time = datetime.utcnow() - timedelta(days=1)  # 查询过去一周的价格数据
end_time = datetime.utcnow()
InstanceTypes = 't3.micro'
# 创建 EC2 客户端
ec2 = boto3.client('ec2', region_name=region)

# 查询可用区域列表
response = ec2.describe_availability_zones(Filters=[{'Name': 'region-name', 'Values': [region]}])
az_list = [zone['ZoneName'] for zone in response['AvailabilityZones']]

# 查询每个可用区的 spot 实例价格
prices = []
for az in az_list:
    response = ec2.describe_spot_price_history(InstanceTypes=[InstanceTypes], StartTime=start_time, EndTime=end_time, AvailabilityZone=az)
    for spot_price in response['SpotPriceHistory']:
        print('Instance type: {0}, Availability Zone: {1}, Spot price: {2}, Time stamp: {3}'.format(
            spot_price['InstanceType'], spot_price['AvailabilityZone'], spot_price['SpotPrice'],
            spot_price['Timestamp']))
#   用json输出
#     for spot_price in response['SpotPriceHistory']:
#         price = {
#             'instance_type': spot_price['InstanceType'],
#             'availability_zone': spot_price['AvailabilityZone'],
#             'spot_price': spot_price['SpotPrice'],
#             'time_stamp': spot_price['Timestamp'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
#         }
#         prices.append(price)
# # 将结果整理为 JSON 格式并打印
# json_result = json.dumps(prices,indent=4)
# print(json_result)
