import mysql.connector
import re


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="askdb",
        password="AskDB@2026!",
        database="sql_playground"
    )


# ============================================================
# SQL SAFETY CHECK
# ============================================================

def check_sql_safety(sql):

    sql_clean = sql.strip()

    if not sql_clean:
        return False, "Please enter some SQL."

    sql_upper = sql_clean.upper()

    # Remove trailing semicolon for checking
    if sql_upper.endswith(";"):
        sql_upper = sql_upper[:-1].strip()

    # --------------------------------------------------------
    # Block multiple SQL statements
    # --------------------------------------------------------

    statements = [
        statement.strip()
        for statement in sql_clean.split(";")
        if statement.strip()
    ]

    if len(statements) > 1:

        return (
            False,
            "Multiple SQL statements are not allowed. "
            "Run one query at a time."
        )

    # --------------------------------------------------------
    # Allowed SQL commands
    # --------------------------------------------------------

    allowed_commands = (
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "CREATE TABLE",
        "ALTER TABLE",
        "SHOW",
        "DESCRIBE"
    )

    if not sql_upper.startswith(allowed_commands):

        return (
            False,
            "This SQL command is not allowed in the playground."
        )

    # --------------------------------------------------------
    # Dangerous commands
    # --------------------------------------------------------

    blocked_patterns = [

        r"\bDROP\s+DATABASE\b",
        r"\bDROP\s+TABLE\b",
        r"\bDROP\s+USER\b",

        r"\bCREATE\s+DATABASE\b",
        r"\bCREATE\s+USER\b",

        r"\bGRANT\b",
        r"\bREVOKE\b",

        r"\bFLUSH\b",

        r"\bSHUTDOWN\b",

        r"\bLOAD\s+DATA\b",

        r"\bINTO\s+OUTFILE\b",
        r"\bINTO\s+DUMPFILE\b"
    ]

    for pattern in blocked_patterns:

        if re.search(pattern, sql_upper):

            return (
                False,
                "🚫 This command is blocked because it "
                "could affect the database system."
            )

    # --------------------------------------------------------
    # Prevent access to the main database
    # --------------------------------------------------------

    if "ASK_MY_DATABASE" in sql_upper:

        return (
            False,
            "🚫 Access to the main database is blocked. "
            "The Playground only uses sql_playground."
        )

    # --------------------------------------------------------
    # Prevent switching databases
    # --------------------------------------------------------

    if re.search(r"\bUSE\s+", sql_upper):

        return (
            False,
            "🚫 Changing databases is not allowed."
        )

    return True, "SQL is allowed."


# ============================================================
# RUN PLAYGROUND SQL
# ============================================================

def run_playground_query(sql):

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    allowed, message = check_sql_safety(sql)

    if not allowed:

        return {
            "success": False,
            "columns": [],
            "rows": [],
            "message": message
        }

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(sql)

        # ----------------------------------------------------
        # SELECT / SHOW / DESCRIBE
        # ----------------------------------------------------

        if cursor.description:

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = cursor.fetchall()

            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "message": "Query executed successfully."
            }

        # ----------------------------------------------------
        # INSERT / UPDATE / DELETE / CREATE / ALTER
        # ----------------------------------------------------

        connection.commit()

        affected_rows = cursor.rowcount

        return {
            "success": True,
            "columns": [],
            "rows": [],
            "message": (
                f"Query executed successfully. "
                f"{affected_rows} row(s) affected."
            )
        }

    except Exception as e:

        if connection:
            connection.rollback()

        return {
            "success": False,
            "columns": [],
            "rows": [],
            "message": str(e)
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# GET CURRENT PLAYGROUND TABLES
# ============================================================

def get_playground_table():

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("SHOW TABLES")

        tables = cursor.fetchall()

        result = {}

        for table in tables:

            table_name = table[0]

            cursor.execute(
                f"SELECT * FROM `{table_name}`"
            )

            columns = [
                column[0]
                for column in cursor.description
            ]

            rows = cursor.fetchall()

            result[table_name] = {
                "columns": columns,
                "rows": rows
            }

        return result

    finally:

        cursor.close()
        connection.close()