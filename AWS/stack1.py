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
        print('AWS堆栈存在，对YAML进行升级')
        try:
            response = cf.update_stack(
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
            # Wait for stack creation/update to complete
            print(f"-Waiting for CloudFormation stack '{stack_name}' to complete...")
            waiter.wait(StackName=stack_name)

            # Print stack events
            print(f" - Stack events for CloudFormation stack '{stack_name}':")
            events = cf.describe_stack_events(StackName=stack_name)
            for event in events['StackEvents']:
            #    print(f" - {event['ResourceType']} {event['LogicalResourceId']} {event['ResourceStatus']}")
                print(f" - {event['Timestamp'].isoformat()}  - {event['ResourceStatus']} - \
                {event['ResourceType']}  - {event['LogicalResourceId']}")

        except Exception as ex:
            print('YAML文件未更新，或者文件有错误！')
            print(ex)


    else:
        # Stack doesn't exist, create it
        print(f"创建  {stack_name}  堆栈")
        try:
            response = cf.create_stack(
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
            print(f" - Waiting for CloudFormation stack '{stack_name}' to complete...")
            waiter.wait(StackName=stack_name)

            # Print stack events
            print(f" - Stack events for CloudFormation stack '{stack_name}':")
            events = cf.describe_stack_events(StackName=stack_name)
            for event in events['StackEvents']:
                print(f" - {event['Timestamp'].isoformat()}  - {event['ResourceStatus']} - \
                {event['ResourceType']}  - {event['LogicalResourceId']}")
        except Exception as ex:
            print('YAML文件有错误！')
            print(ex)

    stack_status = response['StackId']
    exports = cf.list_exports()['Exports']

    if len(exports) > 0:
        print('Stack exports:')
        for export in exports:
            if export['ExportingStackId'] == stack_status:
                print(f" - {export['Name']}  -  {export['Value']}")
        # print(response)
    else:
        print('Stack has no exports.')

    if stack_exists:
        print('Stack updated successfully.')
    else:
        print('Stack created successfully.')

if __name__ == '__main__':
    stack_name = 'cfn-1vpc'
    stack_name = 'cfn-2ec2'
    template_file_path = 'YAML/1_EC2/ec2-full.yaml'
    # parameters = {
    #     # 'BucketName': 'my-bucket',
    #     'Environment': 'prod'
    # }
    # create_or_update_stack(stack_name, template_file_path)
    create_or_update_stack(stack_name, template_file_path, parameters=None, region_name='us-east-1')