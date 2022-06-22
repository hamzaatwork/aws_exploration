import boto3
import json

def explore_iam(roles_arn_list):
    print('Server : ', 'client/connection to IAM')
    iam = boto3.client('iam')

    print('Server : ', 'getting details of all roles using list_roles')
    list_roles_response = iam.list_roles(
    )

    if (list_roles_response['ResponseMetadata']['HTTPStatusCode'] == 200):
        print('Server : ', 'Server respond OK, continuing..')
    else:
        print('Server : ', 'Server respond ', list_roles_response['ResponseMetadata']['HTTPStatusCode'], 'closing..')

    all_roles_arns = []
    for role in list_roles_response['Roles']:
        wanted_keys = ['Arn']
        all_roles_arns.append(role['Arn'])

    print('Server : ', 'checking all roles collected are present in all_roles list')
    for role in roles_arn_list:
        if role not in all_roles_arns:
            print("Invalid role found")
            return
    print('Server : ', 'all collected roles are valid')

    print('Server : ', 'getting details of policies attached with lambda functions roles')
    roles_arn_associated_policies_details = []
    for role_arn in all_roles_arns:
        rolename = role_arn.rsplit('/', 1)[-1]  # extracting last piece of the url(arn)

        policy_response = iam.list_attached_role_policies(
            RoleName=rolename
        )

        if (policy_response['ResponseMetadata']['HTTPStatusCode'] == 200):
            print('Server : ', 'Server respond OK, continuing..')
        else:
            print('Server : ', 'Server respond ', policy_response['ResponseMetadata']['HTTPStatusCode'], 'closing..')

        arn_attached_policy_statement_list = []
        for policy in policy_response['AttachedPolicies']:
            print('Server : ', 'getting policy details using get_policy')
            get_policy_response = iam.get_policy(
                PolicyArn=policy['PolicyArn']
            )

            if (get_policy_response['ResponseMetadata']['HTTPStatusCode'] == 200):
                print('Server : ', 'Server respond OK, continuing..')
            else:
                print('Server : ', 'Server respond ', get_policy_response['ResponseMetadata']['HTTPStatusCode'],
                      'closing..')

            print('Server : ', 'getting policy document using get_policy_version')
            get_policy_version_response = iam.get_policy_version(
                PolicyArn=policy['PolicyArn'],
                VersionId=get_policy_response['Policy']['DefaultVersionId']
            )
            if (get_policy_version_response['ResponseMetadata']['HTTPStatusCode'] == 200):
                print('Server : ', 'Server respond OK, continuing..')
            else:
                print('Server : ', 'Server respond ', get_policy_version_response['ResponseMetadata']['HTTPStatusCode'],
                      'closing..')

            print('Server : ', 'extracting resource arns for the policy')
            policy_target_arns_list = []
            for policy_statement in get_policy_version_response['PolicyVersion']['Document']['Statement']:
                policy_target_arns_list.append(policy_statement['Resource'])

            policy_target_arns_list_clean = []
            print('Server : ', 'cleaning policy resource arn lists so only valid arns are present')
            for arn in policy_target_arns_list:
                if (type(arn) is list):
                    for unit_arn in arn:
                        if 'arn:aws:' in unit_arn:
                            if unit_arn[len(unit_arn)-1] == '*': #removing last * from arns
                                unit_arn = unit_arn[:len(unit_arn)-2]
                            policy_target_arns_list_clean.append(unit_arn)
                else:
                    if 'arn:aws:' in arn:
                        if arn[len(arn)-1] == '*': #removing last * from arns
                            arn = arn[:len(arn)-2]
                        policy_target_arns_list_clean.append(arn)

            if len(policy_target_arns_list_clean) == 0:
                policy_target_arns_list_clean.append('*')
            arn_attached_policy_statement_list.append({
                'PolicyArn' : policy['PolicyArn'],
                'PolicyResourceArns' : policy_target_arns_list_clean
            })

        roles_arn_associated_policies_details.append({
            'RoleArn': role_arn,
            'AttachedPolicies': arn_attached_policy_statement_list,
            'found_during_discovery': (True if role_arn in roles_arn_list else False)
        })

    return roles_arn_associated_policies_details