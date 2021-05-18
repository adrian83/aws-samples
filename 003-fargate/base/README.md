# Fargate demo


aws cloudformation package --template-file base.yml --s3-bucket adrian-deployments --output-template-file packaged.yml

aws cloudformation deploy --template-file packaged.yml --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM --stack-name fargate-demo   



git clone https://github.com/adrian83/echo-service.git

docker build -t echo:0.0.1 .

docker images
REPOSITORY                           TAG                   IMAGE ID       CREATED          SIZE
echo                                 0.0.1                 38acf6dac93d   27 seconds ago   391MB




export DOCKER_IMAGE=38acf6dac93d
export VERSION=0.0.1
export APP='echo'
export ACCOUNT_ID=`aws sts get-caller-identity | jq '.Account' | cut -d "\"" -f 2`
export REGION=`aws configure get region`
export REPOSITORY=fargate-demo-repository

echo $DOCKER_IMAGE
echo $VERSION
echo $APP
echo $ACCOUNT_ID
echo $REGION
echo $REPOSITORY

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# tag Docker image
docker tag $DOCKER_IMAGE $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY

# push image into ECR registry
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY

# change tag to version number
MANIFEST=$(aws ecr batch-get-image --repository-name $REPOSITORY --image-ids imageTag=latest --query 'images[].imageManifest' --output text)
aws ecr put-image --repository-name $REPOSITORY --image-tag $VERSION --image-manifest "$MANIFEST"



