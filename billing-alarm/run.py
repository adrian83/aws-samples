# -*- coding: utf-8 -*-
import yaml
import io
import boto3


tags = []
params = []
template = ""

with open("tags.yml", 'r') as tags_file:
    tags_dict = yaml.load(tags_file)
    tags = [{"Key": item[0], "Value": item[1]} for item in tags_dict.items()]

with open("parameters.yml", 'r') as params_file:
    params_dict = yaml.load(params_file)
    params = [{"ParameterKey": item[0], "ParameterValue": str(item[1])} for item in params_dict.items()]

with open('cloudformation.yml', 'r') as cfn_template:
    template=cfn_template.read()

print(tags)
print(params)

client = boto3.client('cloudformation')

response = client.create_stack(
    StackName='BILLING-ALARM',
    #TemplateURL='cloudformation.yml',
    TemplateBody=template,
    TimeoutInMinutes=10,
    OnFailure='DELETE',
    Parameters=params,
    Tags=tags
)