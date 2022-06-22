import json
from pprint import pprint

data = []
with open('discovery_reports.json', 'r') as f:
    data = json.load(f)

visualizable_data = {}
nodes = []
links = []
counter = 1

already_included_arns_list = []
already_included_arns_names_list = {}

for data in data[0]['Mapping']:
    counter += 1

    data_keys = list(data.keys())

    source_name = str(data[data_keys[0]])
    source_icon = './images/'+str(data[data_keys[0]])+'.png'
    source_arn = str(data[data_keys[1]])
    target_name = str(data[data_keys[2]])
    target_icon = './images/'+str(data[data_keys[2]])+'.png'
    target_arn = str(data[data_keys[3]])

    #excluding results which point to generic resource
    if source_arn == '*' or target_arn == '*' or ':*:' in source_arn or ':*:' in target_arn:
        continue
    #excluding policies from mapping
    if ':policy/' in source_arn or ':policy/' in target_arn:
        continue

    #mapping resource names to images
    if 'arn:aws:s3:' in source_arn:
        source_icon = './images/s3.png'
        source_name = 's3'
    if 'arn:aws:s3:' in target_arn:
        target_icon = './images/s3.png'
        target_name = 's3'

    if ':apigateway:*' in source_arn:
        source_icon = './images/api.png'
        source_name = 'api'
    if ':apigateway:*' in target_arn:
        target_icon = './images/api.png'
        target_name = 'api'

    if 'arn:aws:lambda:' in source_arn:
        source_icon = './images/lamda.png'
        source_name = 'lamda'
    if 'arn:aws:lambda:' in target_arn:
        target_icon = './images/lamda.png'
        target_name = 'lamda'

    if 'arn:aws::ec2:' in source_arn:
        source_icon = './images/ec2.png'
        source_name = 'ec2'
    if 'arn:aws::ec2:' in target_arn:
        target_icon = './images/ec2.png'
        target_name = 'ec2'

    if 'arn:aws:states:' in source_arn:
        source_icon = './images/state.png'
        source_name = 'state'
    if 'arn:aws:states:' in target_arn:
        target_icon = './images/state.png'
        target_name = 'state'

    if 'arn:aws:iam:' in source_arn:
        source_icon = './images/iam.png'
        source_name = 'iam'
    if 'arn:aws:iam:' in target_arn:
        target_icon = './images/iam.png'
        target_name = 'iam'

    if ':policy/' in source_arn:
        source_icon = './images/policy.png'
        source_name = 'policy'
    if ':policy/' in target_arn:
        target_icon = './images/policy.png'
        target_name = 'policy'

    if 'arn:aws:ssm:' in source_arn:
        source_icon = './images/ssm.png'
        source_name = 'ssm'
    if 'arn:aws:ssm:' in target_arn:
        target_icon = './images/ssm.png'
        target_name = 'ssm'


    source_name = str(source_name + '-' + str(counter))
    target_name = str(target_name + '-' + str(counter))

    # merging duplicate resources
    sourceDuplicate = False
    targetDuplicate = False
    for arn in already_included_arns_list:
        if source_arn == arn:
            source_name = already_included_arns_names_list[str(source_arn)]
            sourceDuplicate = True
        if target_arn == arn:
            target_name = already_included_arns_names_list[str(target_arn)]
            targetDuplicate = True


    if sourceDuplicate == False:
        nodes.append({
            'name' : source_name,
            'meta' : {
                'description' : source_arn
            },
            'icon': source_icon
        })
    if targetDuplicate == False:
        nodes.append({
            'name' : target_name,
            'meta' : {
                'description' : target_arn
            },
            'icon': target_icon
        })
    links.append({
        'source' : source_name,
        'target' : target_name
    })


    already_included_arns_list.append(source_arn)
    already_included_arns_list.append(target_arn)
    already_included_arns_names_list[source_arn] = source_name
    already_included_arns_names_list[target_arn] = target_name

visualizable_data = {
    'nodes' : nodes,
    'links' : links
}

with open('node_modules/inet-henge/example/visualizable_data.json', 'w') as f:
    f.write(json.dumps(visualizable_data, indent=4, default=str))

# python -m http.server