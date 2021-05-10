# Fargate demo


aws cloudformation package --template-file base.yml --s3-bucket adrian-deployments --output-template-file packaged.yml

aws cloudformation deploy --template-file packaged.yml --capabilities CAPABILITY_AUTO_EXPAND --stack-name fargate-demo   