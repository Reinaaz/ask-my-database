import streamlit as st
import requests
import pandas as pd
import html

from database import get_schema
from sql_tool import sql_tool
from playground import run_playground_query, get_playground_table


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ASK_DB",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CINEMATIC TERMINAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(0, 255, 100, 0.045),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 90%,
            rgba(0, 180, 255, 0.035),
            transparent 30%
        ),
        #050807;
    color: #d7ded9;
}

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: -1px;
}

h1 {
    color: #f1f5f2 !important;
}

h2, h3 {
    color: #b9c7bf !important;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #030504;
    border-right: 1px solid #18231d;
}

section[data-testid="stSidebar"] * {
    font-family: 'JetBrains Mono', monospace;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    color: #e9f4ec;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    color: #627068;
    font-size: 11px;
    margin-bottom: 28px;
}

.status-box {
    background: #080d0a;
    border: 1px solid #1b2921;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 10px;
}

.status-row {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 8px 0;
    font-size: 11px;
    color: #7d8c83;
}

.status-online {
    width: 7px;
    height: 7px;
    min-width: 7px;
    border-radius: 50%;
    background: #39ff88;
    box-shadow: 0 0 9px rgba(57,255,136,0.8);
}

.status-label {
    color: #b7c3bb;
}


/* TOP BAR */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #17221c;
    padding-bottom: 18px;
    margin-bottom: 30px;
}

.brand {
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #ecf5ef;
}

.brand-green {
    color: #39ff88;
}

.system-status {
    font-size: 11px;
    color: #6e7e74;
}

.system-status span {
    color: #39ff88;
}


/* HERO */

.hero {
    padding: 25px 0 30px 0;
}

.hero-title {
    font-size: 36px;
    font-weight: 700;
    color: #edf4ef;
    margin-bottom: 8px;
}

.hero-title span {
    color: #39ff88;
}

.hero-subtitle {
    color: #69776f;
    font-size: 13px;
    max-width: 720px;
    line-height: 1.8;
}


/* TERMINAL */

.terminal {
    background: #020403;
    border: 1px solid #1a2920;
    border-radius: 10px;
    overflow: hidden;
    box-shadow:
        0 0 30px rgba(0, 255, 100, 0.025),
        inset 0 0 30px rgba(0, 255, 100, 0.01);
}

.terminal-header {
    height: 40px;
    background: #080d0a;
    border-bottom: 1px solid #17231c;
    display: flex;
    align-items: center;
    padding: 0 15px;
    gap: 7px;
}

.terminal-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.terminal-dot.red {
    background: #593332;
}

.terminal-dot.yellow {
    background: #5c5431;
}

.terminal-dot.green {
    background: #315c3e;
}

.terminal-title {
    margin-left: 10px;
    color: #59675f;
    font-size: 10px;
}


/* INPUT */

.stTextInput input,
.stTextArea textarea {
    background: #030604 !important;
    color: #dce7df !important;
    border: 1px solid #1d2c23 !important;
    border-radius: 7px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #39a96b !important;
    box-shadow: 0 0 0 1px rgba(57,255,136,0.12) !important;
}


/* BUTTONS */

.stButton > button {
    background: #0b1510;
    color: #9ce9b7;
    border: 1px solid #23402e;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #102218;
    border-color: #39a96b;
    color: #caffd9;
    box-shadow: 0 0 14px rgba(57,255,136,0.08);
}

button[kind="primary"] {
    background: #12331f !important;
    border-color: #28683e !important;
    color: #a7ffbf !important;
}


/* CARDS */

.info-card {
    background: #070c09;
    border: 1px solid #18251d;
    border-radius: 9px;
    padding: 20px;
    margin: 15px 0;
}

.card-label {
    color: #526158;
    font-size: 10px;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

.card-value {
    color: #e5eee8;
    font-size: 17px;
    line-height: 1.7;
}


/* SECTION */

.section-label {
    color: #607067;
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: 28px;
    margin-bottom: 12px;
}


/* EXAMPLES */

.example-label {
    color: #59685f;
    font-size: 10px;
    margin-top: 14px;
    margin-bottom: 8px;
}

.example-box {
    background: #070c09;
    border: 1px solid #16231b;
    border-radius: 6px;
    padding: 10px 12px;
    color: #87968d;
    font-size: 10px;
}


/* PLAYGROUND */

.playground-title {
    color: #e7eee9;
    font-size: 24px;
    font-weight: 700;
}

.playground-subtitle {
    color: #65736a;
    font-size: 11px;
    margin-bottom: 25px;
}


/* LIVE DATABASE */

.live-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.live-title {
    color: #cbd6cf;
    font-size: 13px;
}

.live-status {
    color: #39ff88;
    font-size: 9px;
    letter-spacing: 1px;
}


/* DATAFRAME */

[data-testid="stDataFrame"] {
    border: 1px solid #1b2921;
    border-radius: 7px;
    overflow: hidden;
}


/* CODE */

.stCodeBlock {
    border: 1px solid #18271e !important;
    border-radius: 8px !important;
}


/* ALERTS */

div[data-testid="stAlert"] {
    background: #080e0a;
    border: 1px solid #1c2b22;
    color: #a9b6ad;
}


/* TABS */

button[data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: #58665e !important;
    font-size: 11px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #72d991 !important;
}

div[data-baseweb="tab-highlight"] {
    background: #39ff88 !important;
}


/* DIVIDER */

hr {
    border-color: #162119 !important;
}


/* FOOTER */

.footer {
    text-align: center;
    color: #303b34;
    font-size: 9px;
    margin-top: 60px;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# AI
# ============================================================

def ask_ollama(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"].strip()


# ============================================================
# SCHEMA
# ============================================================

def format_schema(schema):

    lines = []

    for table, columns in schema.items():
        lines.append(
            f"{table}: {', '.join(columns)}"
        )

    return "\n".join(lines)


# ============================================================
# ROUTER
# ============================================================

def needs_database(question, schema_text):

    prompt = f"""
You are routing a user's question.

Database schema:

{schema_text}

Answer YES if the question requires information
from the database.

Answer NO if it is unrelated general knowledge.

Return ONLY YES or NO.

Question:
{question}
"""

    answer = ask_ollama(prompt).upper()

    return answer.startswith("YES")


# ============================================================
# SQL GENERATOR
# ============================================================

def generate_sql(question, schema_text):

    prompt = f"""
You are a MySQL SQL expert helping students learn SQL.

Actual database schema:

{schema_text}

Convert the user's English question into a MySQL SELECT query.

Rules:
- Use ONLY tables and columns that exist.
- Generate ONLY SELECT.
- Return ONLY SQL.
- No Markdown.
- No explanation.

Question:
{question}
"""

    return ask_ollama(prompt)


# ============================================================
# ANSWER
# ============================================================

def generate_answer(question, result):

    prompt = f"""
Answer this question using ONLY the database result.

Question:
{question}

Result:
{result}

Rules:
- Direct answer.
- Concise.
- Do not mention SQL.
- Do not invent information.
- Use ₹ for money.
"""

    return ask_ollama(prompt)


# ============================================================
# SQL EXPLANATION
# ============================================================

def explain_sql(question, sql, result):

    prompt = f"""
You are teaching SQL to a beginner.

Question:
{question}

SQL:
{sql}

Result:
{result}

Use exactly these sections:

WHAT IT DOES:
Explain the query simply.

SQL BREAKDOWN:
Explain the important SQL keywords/functions.

WHY THIS WORKS:
Explain the logic simply.

Keep it short.
"""

    return ask_ollama(prompt)


# ============================================================
# DATABASE RESULT
# ============================================================

def display_result(result, sql):

    if not result:
        st.info("No rows returned.")
        return

    sql_upper = sql.upper()

    if "FROM EMPLOYEES" in sql_upper:
        possible = [
            "employee_id",
            "name",
            "department",
            "city",
            "salary"
        ]

    elif "FROM CUSTOMERS" in sql_upper:
        possible = [
            "customer_id",
            "name",
            "city",
            "email"
        ]

    elif "FROM PRODUCTS" in sql_upper:
        possible = [
            "product_id",
            "product_name",
            "category",
            "price"
        ]

    elif "FROM ORDERS" in sql_upper:
        possible = [
            "order_id",
            "customer_id",
            "product_id",
            "quantity",
            "order_date"
        ]

    else:
        possible = []

    columns = []

    for column in possible:

        if column.upper() in sql_upper:

            if column not in columns:
                columns.append(column)

    if len(columns) == len(result[0]):

        df = pd.DataFrame(
            result,
            columns=columns
        )

    else:

        df = pd.DataFrame(result)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PLAYGROUND TABLES
# ============================================================

def display_playground_tables():

    tables = get_playground_table()

    if not tables:

        st.html("""
        <div class="info-card">
            <div class="card-label">DATABASE</div>
            <div class="card-value">
                No tables found.
            </div>
        </div>
        """)

        return

    for table_name, table_data in tables.items():

        st.html(f"""
        <div class="live-header">
            <div class="live-title">
                ▣ {html.escape(table_name)}
            </div>
            <div class="live-status">
                ● LIVE
            </div>
        </div>
        """)

        df = pd.DataFrame(
            table_data["rows"],
            columns=table_data["columns"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-title">
        ASK<span style="color:#39ff88;">_DB</span>
    </div>

    <div class="sidebar-subtitle">
        SQL LEARNING ENVIRONMENT
    </div>
    """)

    st.html("""
    <div class="status-box">

        <div class="status-row">
            <div class="status-online"></div>
            <span class="status-label">OLLAMA</span>
            <span>ONLINE</span>
        </div>

        <div class="status-row">
            <div class="status-online"></div>
            <span class="status-label">MYSQL</span>
            <span>ONLINE</span>
        </div>

        <div class="status-row">
            <div class="status-online"></div>
            <span class="status-label">SQL ENGINE</span>
            <span>ONLINE</span>
        </div>

    </div>
    """)

    st.markdown("---")

    st.html("""
    <div style="
        color:#526158;
        font-size:10px;
        line-height:2;
    ">
        MODE<br>
        <span style="color:#8a978f;">
        AI DATABASE + SQL PLAYGROUND
        </span>
    </div>
    """)


# ============================================================
# TOP BAR
# ============================================================

st.html("""
<div class="topbar">

    <div class="brand">
        ASK<span class="brand-green">_DB</span>
    </div>

    <div class="system-status">
        SYSTEM <span>● OPERATIONAL</span>
    </div>

</div>
""")


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2 = st.tabs(
    [
        "◈ ASK MY DATABASE",
        "▣ SQL PLAYGROUND"
    ]
)


# ============================================================
# ASK MY DATABASE
# ============================================================

with tab1:

    st.html("""
    <div class="hero">

        <div class="hero-title">
            Ask your database<span>.</span>
        </div>

        <div class="hero-subtitle">
            Ask questions in normal English.
            Let AI generate the SQL, execute it,
            and explain exactly how it works.
        </div>

    </div>
    """)

    st.html("""
    <div class="section-label">
        DATABASE QUERY
    </div>
    """)

    question = st.text_input(
        "query",
        placeholder="who has the highest salary?",
        label_visibility="collapsed",
        key="database_question"
    )

    st.html("""
    <div class="example-label">
        TRY AN EXAMPLE
    </div>

    <div class="example-box">
        who works in IT? &nbsp;&nbsp; • &nbsp;&nbsp;
        most expensive product &nbsp;&nbsp; • &nbsp;&nbsp;
        customers from Chennai &nbsp;&nbsp; • &nbsp;&nbsp;
        how many orders?
    </div>
    """)

    st.write("")

    if st.button(
        "▶  EXECUTE QUERY",
        type="primary",
        use_container_width=True,
        key="ask_database"
    ):

        if not question.strip():

            st.warning("Enter a question first.")

        else:

            try:

                with st.spinner(
                    "[AI] inspecting database schema..."
                ):

                    schema = get_schema()
                    schema_text = format_schema(schema)

                with st.spinner(
                    "[AI] analyzing request..."
                ):

                    use_database = needs_database(
                        question,
                        schema_text
                    )

                if use_database:

                    with st.spinner(
                        "[AI] generating SQL..."
                    ):

                        sql = generate_sql(
                            question,
                            schema_text
                        )

                    with st.spinner(
                        "[MYSQL] executing query..."
                    ):

                        result = sql_tool(sql)

                    if (
                        isinstance(result, str)
                        and (
                            result.startswith("SQL Error")
                            or
                            result.startswith("Blocked")
                        )
                    ):

                        st.error(result)

                    else:

                        with st.spinner(
                            "[AI] preparing response..."
                        ):

                            answer = generate_answer(
                                question,
                                result
                            )

                        with st.spinner(
                            "[AI] preparing SQL explanation..."
                        ):

                            explanation = explain_sql(
                                question,
                                sql,
                                result
                            )

                        st.html("""
                        <div class="section-label">
                            QUERY COMPLETE
                        </div>
                        """)

                        safe_answer = html.escape(answer)

                        st.html(f"""
                        <div class="info-card">

                            <div class="card-label">
                                ANSWER
                            </div>

                            <div class="card-value">
                                {safe_answer}
                            </div>

                        </div>
                        """)

                        st.html("""
                        <div class="section-label">
                            GENERATED SQL
                        </div>
                        """)

                        st.code(
                            sql,
                            language="sql"
                        )

                        st.html("""
                        <div class="section-label">
                            DATABASE RESULT
                        </div>
                        """)

                        display_result(
                            result,
                            sql
                        )

                        st.html("""
                        <div class="section-label">
                            UNDERSTAND THE QUERY
                        </div>
                        """)

                        st.markdown(explanation)

                else:

                    with st.spinner(
                        "[AI] processing general question..."
                    ):

                        answer = ask_ollama(
                            f"""
Answer clearly and simply.

Question:
{question}
"""
                        )

                    st.info(
                        "This request does not require the database."
                    )

                    safe_answer = html.escape(answer)

                    st.html(f"""
                    <div class="info-card">

                        <div class="card-label">
                            AI RESPONSE
                        </div>

                        <div class="card-value">
                            {safe_answer}
                        </div>

                    </div>
                    """)

            except requests.exceptions.ConnectionError:

                st.error(
                    "[SYSTEM ERROR] Ollama is not running."
                )

            except Exception as e:

                st.error(
                    f"[SYSTEM ERROR] {e}"
                )


# ============================================================
# SQL PLAYGROUND
# ============================================================

with tab2:

    st.html("""
    <div class="hero">

        <div class="playground-title">
            SQL Playground
        </div>

        <div class="playground-subtitle">
            Write SQL. Execute it. Watch the database change.
        </div>

    </div>
    """)

    st.html("""
    <div class="section-label">
        QUICK START
    </div>
    """)

    example1, example2, example3, example4 = st.columns(4)

    # Initialize editor state
    if "playground_editor" not in st.session_state:

        st.session_state.playground_editor = (
            "SELECT * FROM students;"
        )


    # ========================================================
    # QUICK START BUTTONS
    # ========================================================

    with example1:

        if st.button(
            "SELECT",
            use_container_width=True,
            key="quick_select"
        ):

            st.session_state.playground_editor = (
                "SELECT * FROM students;"
            )

            st.rerun()


    with example2:

        if st.button(
            "INSERT",
            use_container_width=True,
            key="quick_insert"
        ):

            st.session_state.playground_editor = (
                "INSERT INTO students\n"
                "(id, name, age, department)\n"
                "VALUES (4, 'Sara', 23, 'IT');"
            )

            st.rerun()


    with example3:

        if st.button(
            "UPDATE",
            use_container_width=True,
            key="quick_update"
        ):

            st.session_state.playground_editor = (
                "UPDATE students\n"
                "SET age = 25\n"
                "WHERE name = 'Rahul';"
            )

            st.rerun()


    with example4:

        if st.button(
            "DELETE",
            use_container_width=True,
            key="quick_delete"
        ):

            st.session_state.playground_editor = (
                "DELETE FROM students\n"
                "WHERE name = 'Meera';"
            )

            st.rerun()


    # ========================================================
    # EDITOR + DATABASE
    # ========================================================

    editor_col, database_col = st.columns(
        [1, 1],
        gap="large"
    )


    # ========================================================
    # SQL EDITOR
    # ========================================================

    with editor_col:

        st.html("""
        <div class="terminal">

            <div class="terminal-header">

                <div class="terminal-dot red"></div>
                <div class="terminal-dot yellow"></div>
                <div class="terminal-dot green"></div>

                <div class="terminal-title">
                    user@askdb:~/playground
                </div>

            </div>

        </div>
        """)

        playground_sql = st.text_area(
            "SQL",
            height=270,
            label_visibility="collapsed",
            key="playground_editor"
        )

        st.html("""
        <div style="
            color:#4f5e55;
            font-size:9px;
            margin-top:5px;
        ">
            SQL MODE // SANDBOX
        </div>
        """)

        run_col, reset_col = st.columns(2)

        with run_col:

            run_sql = st.button(
                "▶  RUN SQL",
                type="primary",
                use_container_width=True,
                key="run_playground"
            )

        with reset_col:

            refresh = st.button(
                "↻  REFRESH",
                use_container_width=True,
                key="refresh_playground"
            )


    # ========================================================
    # DATABASE
    # ========================================================

    with database_col:

        st.html("""
        <div class="terminal">

            <div class="terminal-header">

                <div class="terminal-dot red"></div>
                <div class="terminal-dot yellow"></div>
                <div class="terminal-dot green"></div>

                <div class="terminal-title">
                    mysql://sql_playground
                </div>

            </div>

        </div>
        """)

        st.write("")

        display_playground_tables()


    # ========================================================
    # EXECUTE
    # ========================================================

    if run_sql:

        if not playground_sql.strip():

            st.warning(
                "Write some SQL first."
            )

        else:

            with st.spinner(
                "[MYSQL] executing..."
            ):

                result = run_playground_query(
                    playground_sql
                )

            if result["success"]:

                st.success(
                    "[MYSQL] query executed successfully"
                )

                if result["rows"]:

                    st.html("""
                    <div class="section-label">
                        QUERY OUTPUT
                    </div>
                    """)

                    df = pd.DataFrame(
                        result["rows"],
                        columns=result["columns"]
                    )

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

                st.html("""
                <div class="section-label">
                    DATABASE STATE
                </div>
                """)

                display_playground_tables()

            else:

                st.error(
                    f"[MYSQL ERROR] {result['message']}"
                )


    if refresh:

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    ASK_DB // SQL LEARNING ENVIRONMENT // LOCAL MODE
</div>
""")