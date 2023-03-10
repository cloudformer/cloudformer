import boto3

def create_or_update_stack(stack_name, template_file_path, parameters=None, region_name='us-east-1'):
    cf = boto3.client('cloudformation', region_name=region_name)
    with open(template_file_path, 'r',encoding='UTF-8') as f:
        template_body = f.read()

    # Check if stack already exists
    stack_exists = False
    try:
        cf.describe_stacks(StackName=stack_name)
        stack_exists = True
    except:
        pass

    if stack_exists:
        # Stack exists, update it
        cf.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters if parameters else [],
            # [{
            #     'ParameterKey': key,
            #     'ParameterValue': value
            # } for key, value in parameters.items()],
            Capabilities=['CAPABILITY_AUTO_EXPAND',
                          'CAPABILITY_NAMED_IAM',
                          'CAPABILITY_IAM']
        )
        waiter = cf.get_waiter('stack_update_complete')
    else:
        # Stack doesn't exist, create it
        cf.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters if parameters else [],
            # [{
            #     'ParameterKey': key,
            #     'ParameterValue': value
            # } for key, value in parameters.items()],
            Capabilities=['CAPABILITY_AUTO_EXPAND',
                          'CAPABILITY_NAMED_IAM',
                          'CAPABILITY_IAM']
        )
        waiter = cf.get_waiter('stack_create_complete')

    # Wait for stack creation/update to complete
    print(f"Waiting for CloudFormation stack '{stack_name}' to complete...")
    waiter.wait(StackName=stack_name)

    # Print stack events
    print(f"Stack events for CloudFormation stack '{stack_name}':")
    events = cf.describe_stack_events(StackName=stack_name)
    for event in events['StackEvents']:
        print(f"  {event['ResourceType']} {event['LogicalResourceId']} {event['ResourceStatus']}")

if __name__ == '__main__':
    stack_name = 'MyStack'
    template_file_path = 'YAML/vpc-2azs.yaml'
    # parameters = {
    #     # 'BucketName': 'my-bucket',
    #     'Environment': 'prod'
    # }
    create_or_update_stack(stack_name, template_file_path)
