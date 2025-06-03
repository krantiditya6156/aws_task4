import json
import os

import boto3
import mysql.connector
from botocore.exceptions import ClientError

DBNAME = os.environ["DBNAME"]
ENDPOINT = os.environ["ENDPOINT"]
REGION_NAME = os.environ["REGION_NAME"]
SECRET_NAME = os.environ["SECRET_NAME"]
STATIC_WEBSITE_URL = os.environ["STATIC_WEBSITE_URL"]


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


def run_db_script(db, cursor, filename):
    with open(filename, "r") as file:
        sql_commands = file.read().split(";")
        for command in sql_commands:
            if command.strip():
                print(command)
                print("-------------------")
                cursor.execute(command)
    db.commit()


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
            cursor = db.cursor()

            no_of_tables_query = f"""SELECT count(*)
                                    FROM information_schema.tables
                                    WHERE table_schema = '{DBNAME}'"""
            cursor.execute(no_of_tables_query)
            tables = cursor.fetchall()
            no_of_tables = tables[0][0]

            if no_of_tables == 0:
                print("Database is empty, executing database_script.sql ....")
                run_db_script(db, cursor, "database_script.sql")
                cursor.execute(no_of_tables_query)
                tables = cursor.fetchall()
                no_of_tables = tables[0][0]
                print("database_script.sql executed successfully!")
                print("no of tables in database are", no_of_tables)
            else:
                print("Tables in database are", tables)

            query = f"""select count(*), sum(amount) 
                    from {DBNAME}.Transaction 
                    where account_id in (select account_id 
                                        from {DBNAME}.Account
                                        where customer_id={customer_id})"""

            cursor.execute(query)
            result = cursor.fetchall()
            result = {"count": result[0][0], "sum": float(result[0][1])}

            db.close()

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": STATIC_WEBSITE_URL,
                    "Access-Control-Allow-Methods": "GET,OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization,auth-token,customer_id",
                },
                "body": json.dumps(result),
            }

        else:
            print("Connection failed")
            raise Exception("Connection failed")

    except Exception as e:
        raise e
