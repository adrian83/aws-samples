# Cognito demo

## WORK IN PROGRESS


## Deployment:  

```
aws cloudformation deploy --template-file infrastructure.yml --stack-name cognito-demo --capabilities CAPABILITY_IAM
```


## Cleaning:  

```
aws cloudformation delete-stack --stack-name cognito-demo
```

## Testing

Knowing that our API Gateway is called `cognito-demo-gateway` and stage is called `cognito-demo` we can create url we can use for testing.

AWS region in which we operate can be found with this command:
```
REGION=`aws configure get region`
echo $REGION
```

... and API Gateway id 
```
API=`aws apigateway get-rest-apis | jq ".items[] | select(.name == \"cognito-demo-gateway\")"`
API_ID=`echo $API | jq ".id" | cut -d "\"" -f 2`
echo "API Gateway id: $API_ID"
```

... and the whole URL looks like this:
```
API_URL="https://$API_ID.execute-api.$REGION.amazonaws.com/cognito-demo"
echo "API Gateway URL: $API_URL"
```




### Register

```
curl -v --request POST \
  --url $API_URL/v1/auth/register \
  --header 'Content-Type: application/json' \
  --data '{
	"email":"<your-email-here>"
}'
```


### Set password
```
curl -v --request POST \
  --url $API_URL/v1/auth/setpassword \
  --header 'Content-Type: application/json' \
  --data '{
	"email":"<your-email-here>",
	"oldPassword":"<password-from-email>",
	"newPassword":"<your-password>"
}'
```

### Access 'secured' endpoint (without auth header)
```
curl -v --request GET \
  --url $API_URL/v1/secured
```

You should see response with status code 401 and body that looks something like that:
```
{
  "message": "Unauthorized"
}
```



### Sign in

```
curl -v --request POST \
  --url $API_URL/v1/auth/signin \
  --header 'Content-Type: application/json' \
  --data '{
	"email":"<your-email-here>",
	"password":"<your-password>"
}'
```


You should see response with status code 200 and body that looks something like that:
```
{
  "accessToken": "<access-token>",
  "idToken": "<id-token>",
  "refreshToken": "<refresh-token>"
}
```


### Access 'secured' endpoint (with valid auth header)

```
curl -v --request GET \
  --url $API_URL/v1/secured \
  --header 'Authorization: <id-token>'
```

You should see response with status code 200 and body that looks something like that:
```
{
  "message": "Hello <your-email-here>"
}
```


### Sign out (!!! doesn't work yet !!!)

```
curl -v --request POST \
  --url $API_URL/v1/auth/signout \
  --header 'Content-Type: application/json' \
  --data '{
	"token":"<access-token>"
}'
```


### Access 'secured' endpoint (with invalid auth header)

```
curl -v --request GET \
  --url $API_URL/v1/secured \
  --header 'Authorization: <id-token>'
```

You should see response with status code 401 and body that looks something like that:
```
{
  "message": "Unauthorized"
}
```

