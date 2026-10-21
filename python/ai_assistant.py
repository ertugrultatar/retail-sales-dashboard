"""Answer plain-English questions about the retail sales data with SQL."""

import sqlite3
from pathlib import Path
import pandas as pd
import ollama

DB_PATH = Path(__file__).parent.parent / "sql" / "retail_sales.db"
TABLE_NAME = "retail_sales"
MODEL = "hf.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF:Q4_K_M"


def get_schema() -> str:
    conn = sqlite3.connect(DB_PATH)
    columns = conn.execute(f"PRAGMA table_info({TABLE_NAME})").fetchall()
    conn.close()

    return "".join(f"{name} ({col_type})\n" for _, name, col_type, *_ in columns)


def build_prompt(question: str) -> str:
    return f"""You are a data analyst. Write a SQLite query that answers the question.

The table is called {TABLE_NAME}. Its columns are:
{get_schema()}
Rules:
- Only write SELECT queries.
- Return only the SQL, nothing else.

Question: {question}"""


def ask_llm(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content

def clean_sql(text: str) -> str:
    return text.replace("```sql", "").replace("```", "").strip()


def is_safe(sql: str) -> bool:
    return sql.strip().upper().startswith("SELECT")


def run_sql(sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    result = pd.read_sql_query(sql, conn)
    conn.close()
    return result


def main():
    question = input("Ask a question: ")
    sql = clean_sql(ask_llm(build_prompt(question)))
    print("AI wrote:", sql)


    if not is_safe(sql):
        print("Blocked: only SELECT queries are allowed.")
        return

    print(run_sql(sql))


if __name__ == "__main__":
    main()
