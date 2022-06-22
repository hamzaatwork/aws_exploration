import boto3
import json
import pprint

from modules import explore_apis as APIS, explore_api as API, explore_lambda as LAMBDA, explore_state as STATE, explore_iam as IAM

print('Server : ', 'Starting...')

print('Server : ', 'function to comfirm object type of dictionary')

def generate_report(api):
    discovery_report = {}

    discovery_report['ApplicationName'] = api['name']

    api_data = API.explore_api(api['id'])
    discovery_report['ApiData'] = api_data

    sfn_data = STATE.explore_step_functions()
    discovery_report['StateFunctionsData'] = sfn_data

    lambda_arns_list = []
    for data in api_data:
        if 'lambda' in data['method_type']:
            lambda_arns_list.append(data['uri'])
    for data in sfn_data:
        for arn in data['resource_arns']:
            if ':lambda:' in arn:
                lambda_arns_list.append(arn)
    lambda_data = LAMBDA.explore_lambda(lambda_arns_list)
    discovery_report['LambdaData'] = lambda_data

    roles_arn_list = []
    for data in api_data:
        if 'arn' in data['credentials']:
            roles_arn_list.append(data['credentials'])
    for data in lambda_data:
        roles_arn_list.append(data['Role'])
    for data in sfn_data:
        roles_arn_list.append(data['roleArn'])
    iam_data = IAM.explore_iam(roles_arn_list)
    discovery_report['IamData'] = iam_data

    resource_mapping = []
    for data in api_data:
        resource_mapping.append({
            'source_name': 'api',
            'source_id': api['id'],
            'target_name': data['method_type'],
            'target_arn': data['uri']
        })
    for data in lambda_data:
        resource_mapping.append({
            'source_name': 'lambda',
            'source_id': data['FunctionArn'],
            'target_name': 'role',
            'target_arn': data['Role']
        })
    for data in sfn_data:
        for arn in data['resource_arns']:
            resource_mapping.append({
                'source_name': 'state',
                'source_arn': data['roleArn'],
                'target_name': 'target_arn',
                'target_arn': arn
            })
    for data in iam_data:
        for policy in data['AttachedPolicies']:
            resource_mapping.append({
                'source_name': 'role',
                'source_arn': data['RoleArn'],
                'target_name': 'policy',
                'target_arn': policy['PolicyArn']
            })
    for data in iam_data:
        for policy in data['AttachedPolicies']:
            for resource_arn in policy['PolicyResourceArns']:
                resource_mapping.append({
                    'source_name': 'policy',
                    'source_arn': data['RoleArn'],
                    'target_name': 'target_arn',
                    'target_arn': resource_arn
                })
    discovery_report['Mapping'] = resource_mapping

    return discovery_report

all_api_discovery_reports = []

apis_details = APIS.get_apis_details()
for api in apis_details:
    all_api_discovery_reports.append(generate_report(api))

with open('discovery_reports.json', 'w') as f:
    f.write(json.dumps(all_api_discovery_reports, indent=4, default=str))


print('Server : ', 'stopped')