import boto3
import json
import pprint

def explore_lambda(lambda_arns_list):
    print('Server : ', 'client/connection to lambda')
    lamda = boto3.client('lambda')

    print('Server : ', 'getting details of all lambda functions using list_functions')
    lamda_functions_response = lamda.list_functions(
    )

    if (lamda_functions_response['ResponseMetadata']['HTTPStatusCode'] == 200):
        print('Server : ', 'Server respond OK, continuing..')
    else:
        print('Server : ', 'Server respond ', lamda_functions_response['ResponseMetadata']['HTTPStatusCode'],
              'closing..')

    print('Server : ', 'extracting function name, arn, and role from the lambda functions list')
    lambda_functions_namearnrole = []
    for function in lamda_functions_response['Functions']:
        wanted_keys = ['FunctionName', 'FunctionArn', 'Role', 'Handler']

        temp_dict = dict((key, function[key]) for key in wanted_keys if key in function)

        temp_dict['found_during_discovery'] = False
        for arn in lambda_arns_list:
            if (function['FunctionArn'] in arn) or (arn in function['FunctionArn']) or (arn == function['FunctionArn']):
                temp_dict['found_during_discovery'] = True

        lambda_functions_namearnrole.append(temp_dict)
    return lambda_functions_namearnrole