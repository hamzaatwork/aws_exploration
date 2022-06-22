import boto3
import json
import pprint

def explore_api(api_id):
    print('Server : ', 'client/connection to apigateway')
    api = boto3.client('apigateway')

    print('Server : ', 'getting all resources in api gateway')
    api_resources_response = api.get_resources(
        restApiId=api_id
    )

    if (api_resources_response['ResponseMetadata']['HTTPStatusCode'] == 200):
        print('Server : ', 'Server respond OK, continuing..')
    else:
        print('Server : ', 'Server respond ', api_resources_response['ResponseMetadata']['HTTPStatusCode'], 'closing..')

    print('Server : ', 'extracting just the resources details from get_resources response, stored in items key')
    api_resources_details = []
    for item in api_resources_response['items']:
        api_resources_details.append(item)

    print('Server : ', 'extracting only those api resources for which some methods exist')
    api_resources_with_methods = []
    for resource in api_resources_details:
        if 'resourceMethods' in resource.keys():
            api_resources_with_methods.append(resource)

    print('Server : ', 'getting details of methods in api resources using get_method')
    resource_methods_details = []
    for resource in api_resources_with_methods:
        for method in resource['resourceMethods'].keys():
            get_method_response = api.get_method(
                restApiId=api_id,
                resourceId=resource['id'],
                httpMethod=method
            )
            resource_methods_details.append(get_method_response)

    print('Server : ', 'extracting the key methodIntegration from method details')
    resource_methods_methodIntegration_details = []
    for method in resource_methods_details:
        resource_methods_methodIntegration_details.append(method['methodIntegration'])

    print('Server : ', 'extracting arns from all methods integration types except MOCK')
    resource_methods_except_mock = []
    for method in resource_methods_methodIntegration_details:
        if method['type'] != 'MOCK':
            resource_methods_except_mock.append(method)

    print('Server : ', 'extracting uris and credentials pairs from all methods except MOCK')
    api_methods_uris_credentials = []
    for method in resource_methods_except_mock:

        method_type = ''
        if ':lambda:' in method['uri']:
            method_type = 'lambda'
        elif ':states:' in method['uri']:
            method_type = 'state'
        else:
            method_type = 'unknown'

        print('Server : ', 'reducing method uri to contain only relavent arn')
        uri = method['uri']
        if uri.count('arn:aws:') > 1:
            uri_last_portion = uri.rsplit('/', 1)[-1]  # extracting last piece of the url(arn)
            uri = uri[:len(uri)-len(uri_last_portion)-1] #extra -1 to remove the slash at the end as well
            while 'arn:aws:' not in uri_last_portion:
                uri_last_portion = uri.rsplit('/', 1)[-1]  # extracting last piece of the url(arn)
            method['uri'] = uri_last_portion

        if 'credentials' in method.keys():
            api_methods_uris_credentials.append({
                'method_type': method_type,
                'uri': method['uri'],
                'credentials': method['credentials']
            })
        else:
            api_methods_uris_credentials.append({
                'method_type': method_type,
                'uri': method['uri'],
                'credentials': 'no_credentials'
            })

    return api_methods_uris_credentials