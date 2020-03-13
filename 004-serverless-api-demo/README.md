# Serverless API Example 

Example build with: API Gateway, Lambda Functions and DynamoDB.



`aws cloudformation package --template-file infrastructure.yml --s3-bucket <existing s3 bucket> --output-template-file packaged.yml`

`aws cloudformation deploy --template-file packaged.yml --stack-name <stack name> --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM`


`aws cloudformation package --template-file infrastructure.yml --s3-bucket cloudformation-deployments-bucket --output-template-file packaged.yml`

`aws cloudformation deploy --template-file packaged.yml --stack-name api-demo --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM`

