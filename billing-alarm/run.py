#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import io
import boto3
import sys

create_cmd = "create"
update_cmd = "update"
delete_cmd = "delete"

stack_name = 'EDU-BILLING-ALARM'
stack_tags = [{"Key": "project", "Value": "edu"}]


def to_param(item):
    return {"ParameterKey": item[0], "ParameterValue": str(item[1])}


def params():
    with open("parameters.yml", 'r') as params_file:
        params_dict = yaml.load(params_file)
        return [to_param(item) for item in params_dict.items()]
    raise ValueError("Couldn't read parameters")


def template():
    with open('cloudformation.yml', 'r') as cfn_template:
        return cfn_template.read()
    raise ValueError("Couldn't read template")


def create_stack(cf_client):
    cf_client.create_stack(
        StackName=stack_name,
        TemplateBody=template(),
        TimeoutInMinutes=10,
        OnFailure='DELETE',
        Parameters=params(),
        Tags=stack_tags
    )
    waiter = cf_client.get_waiter('stack_create_complete')
    waiter.wait(StackName=stack_name)
    print(cf_client.describe_stacks(StackName=stack_name))


def update_stack(cf_client):
    cf_client.update_stack(
        StackName=stack_name,
        TemplateBody=template(),
        Parameters=params(),
        Tags=stack_tags
    )
    waiter = cf_client.get_waiter('stack_update_complete')
    waiter.wait(StackName=stack_name)
    print(cf_client.describe_stacks(StackName=stack_name))


def delete_stack(cf_client):
    return cf_client.delete_stack(
        StackName=stack_name,
    )
    waiter = cf_client.get_waiter('stack_delete_complete')
    waiter.wait(StackName=stack_name)
    print(cf_client.describe_stacks(StackName=stack_name))


def print_menu():
    print("Usage: ./run.py <command>")
    print("possible commands:")
    print("\t{0} - creates cloudformation stack".format(create_cmd))
    print("\t{0} - updates existing stack".format(update_cmd))
    print("\t{0} - removes stack".format(delete_cmd))
    print("\tmenu - prints menu")


if __name__ == "__main__":

    client = boto3.client('cloudformation')

    if len(sys.argv) < 2:
        print("provide command: '{0}', '{1}' or '{2}'".format(create_cmd,
              update_cmd, delete_cmd))
        exit(1)

    command = sys.argv[1].lower()
    if command == create_cmd:
        create_stack(client)
    elif command == update_cmd:
        update_stack(client)
    elif command == delete_cmd:
        delete_stack(client)
    else:
        print("\nunknown command: '{0}'\n".format(command))
        print_menu()
        print()
        exit(1)

    exit(0)
