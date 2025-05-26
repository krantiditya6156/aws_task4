import json
import mysql.connector
import boto3
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "dbcredentials"
    region_name = "ap-south-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    return secret




def lambda_handler(event, context):

    secret = get_secret()
    secret = json.loads(secret)
    username = secret['username']
    password = secret['password']

    try:
        db = mysql.connector.connect(
            host="appstack-rdsdatabase-ru7myf9ohbne.cn6iyk20m27q.ap-south-1.rds.amazonaws.com",
            user=username,
            password=password,
            database="database01"

        )

        if db.is_connected():
            print("Connected to the database successfully!")
        else:
            print("Connection failed")

    except Exception as e:
        print("exception is")
        print(e)



    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
