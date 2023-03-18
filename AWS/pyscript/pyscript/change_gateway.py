import boto3
import json
region = 'us-east-1'
ec2 = boto3.client('ec2',region_name=region)

route_table_id = 'rtb-0be06408c402a9185'
# new_gateway_id = 'eni-02101d5460aaa74d6'
new_gateway_id = 'eni-0676607edac0dab2b'

response = ec2.describe_route_tables(
    RouteTableIds=[route_table_id]
)
# print(json.dumps(response, indent=4))
# get the default route of the route table

for route in response['RouteTables'][0].get('Routes'):
    if route.get('DestinationCidrBlock') == '0.0.0.0/0':
        old_gateway_id = route.get('NetworkInterfaceId')
        break
response = ec2.describe_route_tables(
    RouteTableIds=[route_table_id]
)


# replace the default route with the new gateway
response = ec2.replace_route(
    RouteTableId=route_table_id,
    DestinationCidrBlock='0.0.0.0/0',
    NetworkInterfaceId=new_gateway_id
)
print(f"The old gateway is {old_gateway_id}.")
print(f"change the new gateway is {new_gateway_id}.")
