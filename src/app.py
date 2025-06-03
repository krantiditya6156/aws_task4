import json
import os

import boto3
import mysql.connector
from botocore.exceptions import ClientError


class Database:
    def __init__(self):
        self.endpoint = os.environ["ENDPOINT"]
        self.dbname = os.environ["DBNAME"]
        self.region_name = os.environ["REGION_NAME"]
        self.secret_name = os.environ["SECRET_NAME"]
        self.static_website_url = os.environ["STATIC_WEBSITE_URL"]

    def get_secret(self):
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager", region_name=self.region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response["SecretString"]
        secret = json.loads(secret)
        return secret

    def connect_to_db(self):
        secret = self.get_secret()
        conn = mysql.connector.connect(
            host=self.endpoint,
            database=self.dbname,
            user=secret["username"],
            password=secret["password"],
        )
        return conn

    def run_db_script(self, db, cursor, filename):
        with open(filename, "r") as file:
            sql_commands = file.read().split(";")
            for command in sql_commands:
                if command.strip():
                    print(command)
                    print("-------------------")
                    cursor.execute(command)
        db.commit()

    def get_table_count(self, cursor):
        no_of_tables_query = f"""SELECT count(*)
                                FROM information_schema.tables
                                WHERE table_schema = '{self.dbname}'"""
        cursor.execute(no_of_tables_query)
        tables = cursor.fetchall()
        no_of_tables = tables[0][0]
        return no_of_tables

    def initialize_database(self, db, cursor):
        no_of_tables = self.get_table_count(cursor)
        if no_of_tables == 0:
            print("Database is empty, executing database_script.sql ....")
            self.run_db_script(db, cursor, "database_script.sql")
            no_of_tables = self.get_table_count(cursor)
            print("database_script.sql executed successfully!")
            print("no of tables in database are", no_of_tables)
        else:
            print("Tables in database are", no_of_tables)

    def get_transaction_data(self, customer_id):
        db = self.connect_to_db()
        cursor = db.cursor()
        query = f"""select count(*), sum(amount)
                from {self.dbname}.Transaction
                where account_id in (select account_id
                                    from {self.dbname}.Account
                                    where customer_id={customer_id})"""

        cursor.execute(query)
        result = cursor.fetchall()
        result = {"count": result[0][0], "sum": float(result[0][1])}
        return result

    def get_static_website_url(self):
        return self.static_website_url


def lambda_handler(event, context):

    print("event: ", event)
    try:
        headers = event["headers"]
        customer_id = headers["customer_id"]

        db_obj = Database()
        db = db_obj.connect_to_db()
        if db.is_connected():
            print("Connected to the database successfully!")

            cursor = db.cursor()
            db_obj.initialize_database(db, cursor)
            result = db_obj.get_transaction_data(customer_id)
            db.close()

            static_website_url = db_obj.get_static_website_url()

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": static_website_url,
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
