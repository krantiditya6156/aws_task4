import json
import os

import boto3
import mysql.connector
from botocore.exceptions import ClientError

DBNAME = os.environ["DBNAME"]
ENDPOINT = os.environ["ENDPOINT"]
REGION_NAME = os.environ["REGION_NAME"]
SECRET_NAME = os.environ["SECRET_NAME"]


def get_secret():

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=REGION_NAME)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)
    except ClientError as e:
        raise e

    secret = get_secret_value_response["SecretString"]
    secret = json.loads(secret)
    return secret


def lambda_handler(event, context):

    print("event: ", event)

    headers = event["headers"]
    customer_id = headers["customer_id"]

    secret = get_secret()

    try:
        db = mysql.connector.connect(
            host=ENDPOINT,
            user=secret["username"],
            password=secret["password"],
            database=DBNAME,
        )

        if db.is_connected():
            print("Connected to the database successfully!")
            query = f"""select count(*), sum(amount) 
                    from database01.Transaction 
                    where account_id in (select account_id 
                                        from database01.Account
                                        where customer_id={customer_id})"""

            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            db.close()

            return {"statusCode": 200, "body": json.dumps(str(result))}

        else:
            print("Connection failed")
            raise Exception("Connection failed")

    except Exception as e:
        raise e
