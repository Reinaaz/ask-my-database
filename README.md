# ASK_DB — Ask My Database 🤖

ASK_DB is an AI-powered SQL assistant that allows users to interact with a MySQL database using natural language.

Instead of writing SQL queries manually, users can simply ask questions such as:

> "Show me all employees"

or

> "Which department has the highest number of employees?"

The application uses an AI model to understand the question, generate SQL, execute the query, and present the results.

---

## 🚀 Features

- 💬 Ask database questions using natural language
- 🤖 AI-powered SQL generation using Ollama
- 🗄️ MySQL database integration
- 🔍 Automatic database schema detection
- 📊 Results displayed using Pandas
- 🧠 AI-generated explanations for SQL queries
- 🛡️ SELECT-only protection for AI-generated database queries
- 🧪 Built-in SQL Playground
- 💻 Streamlit-based user interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- MySQL
- Ollama
- Qwen2.5:7b
- Pandas
- Requests
- mysql-connector-python
- python-dotenv

---

## 📂 Project Structure

```text
ask_my_database/
│
├── app.py
├── ai_sql.py
├── database.py
├── sql_tool.py
├── ollama_test.py
├── playground.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env