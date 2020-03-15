# Basic VPC

### An example of Virtual Private Cloud. It doesn't offer any functionality, but can be used as a base for building bigger infrastructure.

#### Prerequisites:
1. AWS account
2. Installed AWS Cli

#### Deployment:  

`aws cloudformation deploy --template-file infrastructure.yml --stack-name basic-vpc`


#### Cleaning:  

`aws cloudformation delete-stack --stack-name basic-vpc`

