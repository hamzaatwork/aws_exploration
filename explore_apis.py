import boto3
import json
import pprint

def get_apis_details():
    print('Server : ', 'client/connection to apigateway')
    api = boto3.client('apigateway')

    print('Server : ', 'getting all rest apis in api gateway')
    get_rest_apis_response = api.get_rest_apis(
    )

    if (get_rest_apis_response['ResponseMetadata']['HTTPStatusCode'] == 200):
        print('Server : ', 'Server respond OK, continuing..')
    else:
        print('Server : ', 'Server respond ', get_rest_apis_response['ResponseMetadata']['HTTPStatusCode'], 'closing..')

    list_of_apis = []
    for item in get_rest_apis_response['items']:
        wanted_keys = ['id', 'name', 'createdDate']
        list_of_apis.append(
            dict((key, item[key]) for key in wanted_keys if key in item))

    return list_of_apis