# -*- coding: utf-8 -*-
import yaml
import io
import boto3


tags = [{"Key": "project", "Value": "edu"}]
params = []
template = ""


with open("parameters.yml", 'r') as params_file:
    params_dict = yaml.load(params_file)
    params = [{"ParameterKey": item[0], "ParameterValue": str(item[1])} for item in params_dict.items()]

with open('cloudformation.yml', 'r') as cfn_template:
    template=cfn_template.read()

client = boto3.client('cloudformation')

response = client.create_stack(
    StackName='EDU-MIGRATION-EXAMPLE',
    TemplateBody=template,
    TimeoutInMinutes=10,
    OnFailure='DELETE',
    Parameters=params,
    Tags=tags
)