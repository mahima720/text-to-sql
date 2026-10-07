import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize GenAI Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Define system prompt (include all columns: NAME, CLASS, SECTION, MARKS)
SYS_PROMPT = """
You are an expert SQL assistant for SQLite.
The database table is named STUDENT and has the following columns:
- NAME VARCHAR(25)
- CLASS VARCHAR(25)
- SECTION VARCHAR(25)
- MARKS INT

Rules:
1. Generate valid SQLite SQL queries only.
2. Return ONLY the raw SQL statement.
3. Do not include markdown code blocks, backticks, or explanatory text.
"""

def get_gemini_response(question: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYS_PROMPT,
            temperature=0.0
        )
    )
    
    # Robust cleanup of markdown backticks if returned
    sql_query = response.text.strip()
    if sql_query.startswith("```"):
        lines = sql_query.splitlines()
        # Drop opening fence (e.g. ```sql) and closing fence (```)
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        sql_query = "\n".join(lines).strip()
        
    return sql_query

import pandas as pd

def read_sql_query(sql: str, db: str):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        # Extract column names from the cursor description
        columns = [desc[0] for desc in cur.description] if cur.description else []
        return rows, columns, None
    except sqlite3.Error as e:
        return None, None, str(e)
    finally:
        conn.close()

# Streamlit App
st.set_page_config(page_title="Retrieve SQL Data with Gemini")
st.title("TalkToDB: Natural Language to SQL")
st.caption("Ask questions in plain English and query the database instantly.")

question = st.text_input("Enter your question in plain English:", key="input")
submit = st.button("Generate & Run Query")

if submit and question:
    generated_sql = get_gemini_response(question)
    st.subheader("Generated SQL Query:")
    st.code(generated_sql, language="sql")
    
    # Unpack all 3 returned values: rows, columns, err
    rows, columns, err = read_sql_query(generated_sql, "student.db")
    
    if err:
        st.error(f"SQL Execution Error: {err}")
    elif rows:
        st.subheader("Query Results:")
        import pandas as pd
        df = pd.DataFrame(rows, columns=columns)
        st.dataframe(df, width='content')
    else:
        st.info("Query executed successfully, but returned 0 rows.")