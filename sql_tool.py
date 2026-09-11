from database import run_query


def sql_tool(query):
    query = query.strip()

    # Remove Markdown code fences from AI-generated SQL
    query = query.replace("```sql", "").replace("```", "").strip()

    # Convert to uppercase for checking
    query_upper = query.upper()

    # Allow only read-only SQL
    allowed = ("SELECT", "SHOW", "DESCRIBE")

    if not query_upper.startswith(allowed):
        return "Blocked: Only read-only SQL queries are allowed."

    # Block multiple SQL statements
    if ";" in query[:-1]:
        return "Blocked: Multiple SQL statements are not allowed."

    try:
        result = run_query(query)
        return result

    except Exception as e:
        return f"SQL Error: {e}"