import os
import mysql.connector
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


def create_connection():
    """
    Create and return a connection to the MySQL database.
    """

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def run_query(sql):
    """
    Execute a SQL query and return the results.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        return results

    finally:
        cursor.close()
        connection.close()


def get_schema():
    """
    Get all tables and their columns from the database.
    """

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        schema = {}

        for table in tables:
            table_name = table[0]

            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()

            schema[table_name] = [
                column[0]
                for column in columns
            ]

        return schema

    finally:
        cursor.close()
        connection.close()