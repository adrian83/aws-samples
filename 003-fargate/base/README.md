# Fargate demo


aws cloudformation package --template-file fargate-echo.yml --s3-bucket adrian-deployments --output-template-file packaged.yml

aws cloudformation deploy --template-file packaged.yml --stack-name fargate-demo-echo