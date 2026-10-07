# TalkToDB: Natural Language to SQL Assistant

A Streamlit web application that converts plain English questions into SQLite database queries using Google's Gemini LLM, executes them in real time, and presents the results cleanly in the browser.

---

## 🔗 Live Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://text-to-sql-gemini.streamlit.app/)


![UI](/images/image1.png)
![UI](/images/image2.png)

## 📌 Features

* **Natural Language Querying:** Ask questions about your data without writing manual SQL syntax.
* **Powered by Google Gemini:** Uses Gemini models via the latest `google-genai` SDK with strict system prompt conditioning for zero-shot SQL generation.
* **Live SQLite Execution:** Executes generated queries against a local SQLite database (`student.db`) and renders results dynamically.
* **Interactive UI:** Built with Streamlit, showing the plain English prompt, the exact generated SQL query, and the output dataset.

---

## 📂 Project Structure

```text
Text to Sql/
│
├── sql.py              # Main Streamlit application (LLM prompt + DB query engine)
├── sqlite.py           # Database setup script (creates student.db and seeds initial data)
├── student.db          # SQLite database file (created upon running sqlite.py)
├── .env                # Environment file containing your Gemini API key (excluded from Git)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 🗄️ Database Schema

The sample database contains a single table named **`STUDENT`**:

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `NAME` | `VARCHAR(25)` | Student's name |
| `CLASS` | `VARCHAR(25)` | Enrolled course/class |
| `SECTION` | `VARCHAR(25)` | Class section identifier |
| `MARKS` | `INT` | Total score / marks |

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.10+
* A Google Gemini API key (obtainable via [Google AI Studio](https://aistudio.google.com/))

### 2. Clone the Repository

```bash
git clone https://github.com/<your-username>/text-to-sql-gemini.git
cd text-to-sql-gemini
```

### 3. Create and Activate a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install streamlit google-genai python-dotenv pandas
```

### 5. Configure API Key

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY="your_gemini_api_key_here"
```

### 6. Initialize the Database

Run `sqlite.py` once to build the table and insert sample records:

```bash
python sqlite.py
```

### 7. Run the Application

Launch the Streamlit interface:

```bash
streamlit run sql.py
```

Open `http://localhost:8501` in your browser.

---

## 💡 Example Queries

Try asking the following questions in the input field:

| English Prompt | Expected SQL Output |
| :--- | :--- |
| *"Show all student records"* | `SELECT * FROM STUDENT;` |
| *"Tell me all students studying in Data Science"* | `SELECT * FROM STUDENT WHERE CLASS = 'Data Science';` |
| *"Who scored more than 80 marks?"* | `SELECT NAME FROM STUDENT WHERE MARKS > 80;` |
| *"How many total students are in the database?"* | `SELECT COUNT(*) FROM STUDENT;` |
| *"Which student got the highest marks?"* | `SELECT NAME FROM STUDENT ORDER BY MARKS DESC LIMIT 1;` |
| *"List the names and sections of all students in DEVOPS"* | `SELECT NAME, SECTION FROM STUDENT WHERE CLASS = 'DEVOPS';` |

---

![UI](/images/image3.png)
![UI](/images/image4.png)

## 🧠 Key Learnings & Takeaways

* **System Prompt Guardrails & Formatting:** Learned that LLMs by default wrap code outputs in Markdown code blocks (```` ```sql ... ``` ````). Setting zero temperature and applying clean parsing logic is essential before passing AI output directly into an execution engine.
* **Separating System Instructions:** Discovered that utilizing `GenerateContentConfig(system_instruction=...)` instead of concatenating instructions directly into the user message significantly improves prompt adherence and output consistency.
* **Handling Database Paths:** Learned how working directories affect SQLite file discovery in Streamlit applications, and how resolving database paths dynamically with `os.path` avoids `no such table` runtime exceptions.
* **Virtual Environment Relocation:** Experienced firsthand how moved Python virtual environments cause broken shims due to hardcoded executable paths, and how rebuilding the virtual environment cleanly resolves launcher errors.

---

## 🔒 Security Notes

* **Read-Only Recommended:** For production deployments, configure your SQLite connection or database user with read-only permissions to prevent unwanted `DROP`, `DELETE`, or `UPDATE` commands.
* **Keep Secrets Safe:** Never commit your `.env` file to version control. Add `.env` and `student.db` to your `.gitignore`.

---

## 🎯 Conclusion

This project demonstrates the practical potential of LLM-powered natural language database interfaces. By combining Google's Gemini Flash model with Streamlit and SQLite, the application successfully bridges the technical gap between business users and relational databases—allowing non-technical stakeholders to query complex data effortlessly without writing a single line of SQL.