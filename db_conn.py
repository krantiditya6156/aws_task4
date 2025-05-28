import json

import boto3
import mysql.connector
from botocore.exceptions import ClientError

FILE_NAME = "database_script.sql"
REGION_NAME = "ap-south-1"
SECRET_ID = "dbcredentials"
ENDPOINT = "appstack2-rdsdatabase-ajsqbdacxul9.cn6iyk20m27q.ap-south-1.rds.amazonaws.com"
DBNAME = "database01"


def get_secret(secret_id):

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=REGION_NAME)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        raise e

    secret = get_secret_value_response["SecretString"]
    secret = json.loads(secret)
    return secret


def create_connection(endpoint, user, password, dbname):
    db = mysql.connector.connect(
        host=endpoint, user=user, password=password, database=dbname
    )
    return db


def run_db_script(db, filename):
    cursor = db.cursor()
    with open(filename, "r") as file:
        sql_commands = file.read().split(";")

        for command in sql_commands:
            if command.strip():
                print(command)
                print("-------------------")
                cursor.execute(command)

    db.commit()
    cursor.close()


if __name__ == "__main__":

    try:

        secrets = get_secret(SECRET_ID)
        db = create_connection(
            ENDPOINT, secrets["username"], secrets["password"], DBNAME
        )

        if db.is_connected():
            print("Connected to the database successfully!")
            run_db_script(db, FILE_NAME)
            db.close()
            print("database_script.sql executed successfully!")

    except Exception as e:
        raise e
