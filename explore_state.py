import boto3
import json
import pprint

def explore_step_functions():
    print('Server : ', 'client/connection to step functions')
    sfn = boto3.client('stepfunctions')

    state_machines_details = []

    print('Server : ', 'getting details of all state machines using list_state_machines')
    state_machines_response = sfn.list_state_machines(
    )

    if (state_machines_response['ResponseMetadata']['HTTPStatusCode'] == 200):
        print('Server : ', 'Server respond OK, continuing..')
    else:
        print('Server : ', 'Server respond ', state_machines_response['ResponseMetadata']['HTTPStatusCode'],
              'closing..')

    list_of_state_machines = []
    for machine in state_machines_response['stateMachines']:
        wanted_keys = ['stateMachineArn', 'name', 'type']
        list_of_state_machines.append(
            dict((key, machine[key]) for key in wanted_keys if key in machine))

    for machine in list_of_state_machines:
        print('Server : ', 'getting state machine definition')
        describe_state_machine_response = sfn.describe_state_machine(
            stateMachineArn=machine['stateMachineArn']
        )
        if (describe_state_machine_response['ResponseMetadata']['HTTPStatusCode'] == 200):
            print('Server : ', 'Server respond OK, continuing..')
        else:
            print('Server : ', 'Server respond ', describe_state_machine_response['ResponseMetadata']['HTTPStatusCode'],
                  'closing..')

        print('Server : ', 'getting state machine execution history')
        list_executions_response = sfn.list_executions(
            stateMachineArn=machine['stateMachineArn']
        )
        if (list_executions_response['ResponseMetadata']['HTTPStatusCode'] == 200):
            print('Server : ', 'Server respond OK, continuing..')
        else:
            print('Server : ', 'Server respond ', list_executions_response['ResponseMetadata']['HTTPStatusCode'],
                  'closing..')

        print('Server : ', 'extracting execution arns from machine execution history')
        machine_execution_arns = []
        for execution in list_executions_response['executions']:
            machine_execution_arns.append(execution['executionArn'])

        resource_arns = []
        definition = json.loads(describe_state_machine_response['definition'])
        definition = definition['States']
        definition_keys = definition.keys()
        for key in definition_keys:
            state_keys = definition[key].keys()
            if 'Resource' in state_keys:
                resource_arns.append(definition[key]['Resource'])

        state_machines_details.append({
            'stateMachineArn': describe_state_machine_response['stateMachineArn'],
            'roleArn': describe_state_machine_response['roleArn'],
            'definition': describe_state_machine_response['definition'],
            'resource_arns': resource_arns,
            'executions': machine_execution_arns
        })

    return state_machines_details