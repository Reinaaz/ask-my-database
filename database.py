import mysql.connector


def run_query(sql):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rei1809#",
        database="ask_my_database"
    )

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


def get_schema():
    connection = mysql.connector.connect(
        host= os.getenv("DB_HOST"),
        user= os.getenv("DB_HOST"),
        password= os.getenv("DB_HOST"),
        database= os.getenv("DB_HOST")
    )

    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    schema = {}

    for table in tables:
        table_name = table[0]

        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        schema[table_name] = [column[0] for column in columns]

    cursor.close()
    connection.close()

    return schema