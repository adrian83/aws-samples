# Serverless API on AWS  

### An Example of CRUD application for managing Users. Listing with pagination (or more precisely - lazy loading) is also implemented.

#### Warning! Deploying this application may cost some money.

#### Used AWS services:
1. API Gateway
2. Lambda
3. DynamoDB
4. CloudFormation and S3 (for deployment)


#### Prerequisites:
1. AWS account
2. Installed AWS Cli


#### Deployment:  

`aws cloudformation deploy --template-file infrastructure.yml --stack-name api-demo --capabilities CAPABILITY_IAM`


#### Cleaning:  

`aws cloudformation delete-stack --stack-name api-demo`


### Usage

##### Before you start:
1. Check your Region, by executing this command: `aws configure get region`
2. Remeber Id of API Gateway with name 'users-api-gateway'. List of API Gateways can be fetched by executing this command: `aws apigateway get-rest-apis`


Generic URL to API Gateways is `https://<REST-API-ID>.execute-api.<AWS-REGION>.amazonaws.com/<STAGE>`
Knowing, that our Stage is called 'api-demo' and having region name and API Gateway Id, we can create URL to Users API.

In my case it's: `https://kyyvk41jk7.execute-api.eu-west-1.amazonaws.com/api-demo`

##### Creating users:  

`curl -d '{"firstName":"John","lastName":"Smith"}' -X POST <API-URL>/v1/users`

Example: `curl -d '{"firstName":"John","lastName":"Smith"}' -X POST https://kyyvk41jk7.execute-api.eu-west-1.amazonaws.com/api-demo/v1/users`


##### Getting users by Id:

`curl <API-URL>/v1/users/<USER-ID>`

Example: `curl https://kyyvk41jk7.execute-api.eu-west-1.amazonaws.com/api-demo/v1/users/576ed3f8-c03c-4f86-88b8-ecd06b3e9893`

##### Updating users:

`curl -d '{"firstName":"Jack","lastName":"Kowalsky"}' -X PUT <API-URL>/v1/users/<USER-ID>`

Example: `curl -d '{"firstName":"Jack","lastName":"Kowalsky"}' -X PUT https://kyyvk41jk7.execute-api.eu-west-1.amazonaws.com/api-demo/v1/users/cb576886-5c3c-448f-b9f2-00b58130d18e`


##### Deleting users: 

`curl -X DELETE <API-URL>/v1/users/<USER-ID>`

Example: `curl -X DELETE https://kyyvk41jk7.execute-api.eu-west-1.amazonaws.com/api-demo/v1/users/576ed3f8-c03c-4f86-88b8-ecd06b3e9893`


##### Listing users:

`curl <API-URL>/api-demo/v1/users`

or  

`curl <API-URL>/api-demo/v1/users?lastKey=<LAST-USER-ID-FROM-PREV-PAGE>`


Examples: `curl https://kyyvk41jk7.execute-api.eu-west-1.amazonaws.com/api-demo/v1/users` or `curl https://kyyvk41jk7.execute-api.eu-west-1.amazonaws.com/api-demo/v1/users?lastKey=c09e008d-e510-4bb4-9851-dc425bf35088`

