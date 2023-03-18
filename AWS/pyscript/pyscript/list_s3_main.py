import boto3
import json

region = 'us-west-2'

# 创建 S3 客户端
s3 = boto3.client('s3', region_name=region)

# 使用 list_buckets 方法列出所有 S3 存储桶
response = s3.list_buckets()

# 遍历每个存储桶，获取其详细信息
buckets = []
for bucket in response['Buckets']:
    bucket_name = bucket['Name']
    location = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']


    bucket_info = {
        'name': bucket_name,
        'location': location,
        'creation_date': bucket['CreationDate'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }
    buckets.append(bucket_info)

json_result = json.dumps(buckets,indent=4)
print(json_result)
