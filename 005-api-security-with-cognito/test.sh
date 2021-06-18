echo ""
echo "--- PARAMETERS ---"
echo ""

REGION=`aws configure get region`
echo "Region: $REGION"

API=`aws apigateway get-rest-apis | jq ".items[] | select(.name == \"users-api-gateway\")"`
API_ID=`echo $API | jq ".id" | cut -d "\"" -f 2`
echo "API Gateway id: $API_ID"

STAGE="api-demo"
echo "Stage: $STAGE"

API_URL="https://$API_ID.execute-api.$REGION.amazonaws.com/$STAGE"
echo "API Gateway URL: $API_URL"

echo ""
echo "--- CREATE USER ---"
echo ""

USER=`curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users`
echo $USER

USER_ID=`echo $USER | jq ".id" | cut -d "\"" -f 2`
echo $USER_ID

echo ""
echo "--- GET USER BY ID ---"
echo ""

curl $API_URL/v1/users/$USER_ID

echo ""
echo ""
echo "--- UPDATE USER ---"
echo ""

curl -d '{"firstName":"Jack","lastName":"Kowalsky"}' -X PUT $API_URL/v1/users/$USER_ID

echo ""
echo ""
echo "--- DELETE USER ---"

curl -X DELETE $API_URL/v1/users/$USER_ID

echo ""
echo "--- CREATE USERS ---"
echo ""

curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users

USER_10=`curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users`
echo $USER_10

USER_10_ID=`echo $USER_10 | jq ".id" | cut -d "\"" -f 2`
echo $USER_10_ID

curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users
curl -d '{"firstName":"John","lastName":"Smith"}' -X POST $API_URL/v1/users

echo ""
echo ""
echo "--- LIST USERS - 1ST PAGE---"
echo ""

curl $API_URL/v1/users

echo ""
echo ""
echo "--- LIST USERS - 2ND PAGE---"
echo ""

curl $API_URL/v1/users?lastKey=$USER_10_ID

echo ""