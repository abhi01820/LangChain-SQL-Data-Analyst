# LangChain-SQL-Data-Analyst 📊

### 🎥 Video Demo
[![Demo Video](https://drive.google.com/thumbnail?id=12kFJyT16Zd1Xrnrq7i295GKRfhthbHGV&sz=w800)](https://drive.google.com/file/d/12kFJyT16Zd1Xrnrq7i295GKRfhthbHGV/view?usp=sharing)

LangChain SQL Data Analyst is an interactive web application that allows you to chat with your data. Simply upload a CSV file and ask natural language questions. Powered by Open Source LLMs via LangChain and HuggingFace, it automatically converts your questions into SQL queries, executes them, and provides intelligent insights along with data visualizations.

## 🚀 Features
- **Natural Language to SQL:** Ask questions in plain English, and the agent translates them into valid SQL queries.
- **Dynamic Data Visualization:** Automatically generates interactive charts based on query results using Plotly.
- **Actionable Insights:** Provides AI-generated insights summarizing the queried data.
- **Security Check:** Validates SQL queries to prevent harmful operations (e.g., SQL injection, DROP/DELETE commands).
- **Export Data:** Download the resulting query data as a CSV file.

## 🛠️ Technology Stack
- **Frontend:** Streamlit
- **Data Manipulation:** Pandas
- **Visualization:** Plotly
- **Database:** SQLite & SQLAlchemy
- **AI / LLM Framework:** LangChain & HuggingFace Hub

## 🔄 Complete Workflow
1. **Upload Dataset:** The user uploads a CSV file via the Streamlit sidebar.
2. **Data Processing:** The app reads, cleans, and loads the CSV data into a temporary SQLite database.
3. **Schema Extraction:** The database schema (table structure, columns, and data types) is automatically extracted.
4. **Ask Questions:** The user enters a natural language question about the dataset.
5. **SQL Generation:** LangChain and an Open Source LLM analyze the question alongside the extracted schema to generate an accurate SQL query.
6. **Safety Validation:** The generated SQL query is validated to ensure only safe `SELECT` operations are executed.
7. **Query Execution:** The SQL query runs against the SQLite database to fetch the relevant records.
8. **Insights & Visualization:** 
   - An LLM analyzes the query results to generate a human-readable insight.
   - Plotly automatically creates a relevant chart/graph based on the resulting data.
9. **Display:** The user is presented with the insight, the data table, the visualization, and an option to view the generated SQL code or download the result as a CSV.



---

created by Abhi ❤️
