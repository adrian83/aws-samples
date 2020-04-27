
STAGE="api-demo"

REGION=`aws configure get region`
echo "Region: $REGION"

API=`aws apigateway get-rest-apis | jq ".items[] | select(.name == \"users-api-gateway\")"`
API_ID=`echo $API | jq ".id" | cut -d "\"" -f 2`
echo "API Gateway id: $API_ID"

API_URL="https://$API_ID.execute-api.$REGION.amazonaws.com/$STAGE"
echo "API Gateway URL: $API_URL"



curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users