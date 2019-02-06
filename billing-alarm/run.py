# -*- coding: utf-8 -*-
import yaml
import io

tags = ""
params = ""

with open("tags.yml", 'r') as tags_file:
    tags_dict = yaml.load(tags_file)
    tags = " ".join(["Key={0},Value={1}".format(item[0], item[1]) for item in tags_dict.items()])

with open("parameters.yml", 'r') as params_file:
    params_dict = yaml.load(params_file)
    params = " ".join(["ParameterKey={0},ParameterValue={1}".format(item[0], item[1]) for item in params_dict.items()])

print(tags)
print(params)

