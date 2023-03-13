import boto3
region = 'us-west-2'
# 创建一个EC2客户端
ec2_client = boto3.client('ec2', region_name=region)

# 使用describe_regions方法获取所有可用区域信息
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
for region in regions:
    print(region)
# 打印所有可用区域
print(regions)
