#!/bin/bash

# ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION_NAME="ap-northeast-1"
BUCKET_NAME="code-bucket-sam-${REGION_NAME}-123456"
STACK_NAME="AppStack2"
Username="admin"


if aws s3 ls "s3://${BUCKET_NAME}" 2>&1 | grep -q 'NoSuchBucket'; then
    echo "Bucket does not exist. Creating..."
    aws s3 mb s3://${BUCKET_NAME} --region ${REGION_NAME}
else
    echo "Bucket ${BUCKET_NAME} already exists."
fi


aws s3 cp ./mysql-layer/mysql-layer.zip s3://${BUCKET_NAME}

aws cloudformation package --s3-bucket ${BUCKET_NAME} \
    --template-file template.yaml \
    --output-template-file gen/template-generated.yaml

aws cloudformation deploy --template-file gen/template-generated.yaml \
    --stack-name ${STACK_NAME} \
    --capabilities CAPABILITY_IAM \
    --region ${REGION_NAME} \
    --parameter-overrides DBUsername=${Username}
