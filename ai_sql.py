import requests
from database import get_schema
from sql_tool import sql_tool


def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()


def format_schema(schema):
    lines = []

    for table, columns in schema.items():
        lines.append(f"{table}: {', '.join(columns)}")

    return "\n".join(lines)


def needs_database(question, schema_text):

    prompt = f"""
You are routing a user's question.

Database schema:
{schema_text}

Decide whether the question needs information from this database.

Answer YES if the question asks about:
- employees
- customers
- products
- orders
- salaries
- departments
- cities
- prices
- quantities
- order dates
- or any information that could come from the database.

Answer NO if it is general knowledge unrelated to this database.

Examples:

Who works in IT?
YES

Who has the highest salary?
YES

Which customers are from Chennai?
YES

What is the most expensive product?
YES

How many orders were placed?
YES

What is SQL?
NO

What is Python?
NO

What is machine learning?
NO

Return ONLY YES or NO.

Question:
{question}
"""

    answer = ask_ollama(prompt).upper()

    return answer.startswith("YES")


def generate_sql(question, schema_text):

    prompt = f"""
You are a MySQL SQL expert helping students learn SQL.

Actual database schema:

{schema_text}

Convert the user's English question into a MySQL SELECT query.

IMPORTANT:
- Use ONLY tables and columns that exist in the schema.
- Generate only SELECT queries.
- Return ONLY the SQL query.
- Do not explain anything.
- Do not use Markdown code fences.

Question:
{question}
"""

    return ask_ollama(prompt)


def generate_learning_explanation(question, sql, result):

    prompt = f"""
You are an SQL teacher helping a beginner student.

The student asked:

{question}

The SQL query generated was:

{sql}

The database result was:

{result}

Explain the query in very simple English.

Your response MUST have exactly these sections:

WHAT IT DOES:
Explain in one or two simple sentences what the query accomplishes.

SQL BREAKDOWN:
Explain the important SQL parts one by one.
For example:
- SELECT
- FROM
- WHERE
- GROUP BY
- ORDER BY
- MAX
- COUNT
- JOIN
Only explain the parts that actually appear in the query.

WHY THIS WORKS:
Explain the logic of the query in simple beginner-friendly language.

Keep it short and easy to understand.
Do not invent information.
"""


    return ask_ollama(prompt)


# ==========================================
# MAIN PROGRAM
# ==========================================

question = input("Ask your database a question: ")

# Get the REAL database schema
schema = get_schema()

schema_text = format_schema(schema)

print("\nDatabase Schema:")
print(schema_text)


# ==========================================
# STEP 1 — ROUTING
# ==========================================

if needs_database(question, schema_text):

    print("\nAgent decision: Use database")


    # ======================================
    # STEP 2 — GENERATE SQL
    # ======================================

    sql = generate_sql(question, schema_text)

    print("\n💻 Generated SQL:")
    print(sql)


    # ======================================
    # STEP 3 — EXECUTE SQL
    # ======================================

    result = sql_tool(sql)

    print("\n📊 Database Result:")
    print(result)


    # ======================================
    # STEP 4 — GENERATE ANSWER
    # ======================================

    answer = ask_ollama(
        f"""
Answer the user's question using ONLY the database result.

Question:
{question}

Database result:
{result}

Rules:
- Give the direct answer.
- Be concise.
- Do not mention SQL or database processing.
- Do not invent information.
"""
    )

    print("\n💬 Answer:")
    print(answer)


    # ======================================
    # STEP 5 — TEACH THE SQL
    # ======================================

    explanation = generate_learning_explanation(
        question,
        sql,
        result
    )

    print("\n📚 Learn:")
    print(explanation)


else:

    print("\nAgent decision: No database needed")

    answer = ask_ollama(
        f"""
Answer this question clearly and simply.

Question:
{question}
"""
    )

    print("\n💬 Answer:")
    print(answer)