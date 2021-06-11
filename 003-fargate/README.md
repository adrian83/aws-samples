# Fargate demo

### Infrastructure - go to `base` dir and...

Let's package our base infrastructure 

```
aws cloudformation package --template-file base.yml --s3-bucket adrian-deployments --output-template-file packaged.yml
```

... and now we can deploy it 

```
aws cloudformation deploy --template-file packaged.yml --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM --stack-name fargate-demo
```

### Application - go to `app-echo` dir and...

If the basic infrastructure is build, lets deploy an app. I will use simple app called 'echo-service'.


Let's clone the repository

```
git clone https://github.com/adrian83/echo-service.git
```


Let's build a docker image 

```
docker build -t echo:0.0.1 .
```

If we list docker images (`docker images | grep echo`) we should see something like this:

```
REPOSITORY                           TAG                   IMAGE ID       CREATED          SIZE
...
echo                                 0.0.1                 38acf6dac93d   27 seconds ago   391MB
...
```

Now we will upload our newly created docker image to ECR

Let's define few consts
```
export DOCKER_IMAGE=38acf6dac93d
export VERSION=0.0.1
export APP='echo'
export ACCOUNT_ID=`aws sts get-caller-identity | jq '.Account' | cut -d "\"" -f 2`
export REGION=`aws configure get region`
export REPOSITORY=fargate-demo-repository
```

... and let's check them
```
echo $DOCKER_IMAGE
echo $VERSION
echo $APP
echo $ACCOUNT_ID
echo $REGION
echo $REPOSITORY
```

Now we can log in to ECR 

```
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```

Let's tag our docker image

```
docker tag $DOCKER_IMAGE $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY
```

... and push our image into ECR registry

```
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY
```

We can also change tag to version number

```
MANIFEST=$(aws ecr batch-get-image --repository-name $REPOSITORY --image-ids imageTag=latest --query 'images[].imageManifest' --output text)
aws ecr put-image --repository-name $REPOSITORY --image-tag $VERSION --image-manifest "$MANIFEST"
```

Now we can package our application stack and deploy it

```
aws cloudformation package --template-file fargate-echo.yml --s3-bucket <s3-bucket> --output-template-file packaged.yml
```

```
aws cloudformation deploy --template-file packaged.yml --stack-name fargate-demo-echo --parameter-overrides BaseStackName=fargate-demo --capabilities CAPABILITY_IAM
```

