# 📊 AI Data Analyst Copilot

## 🚀 Overview
The **AI Data Analyst Copilot** is an AI-powered tool that enables users to analyze datasets using natural language queries instead of writing code.

Users can upload a CSV file and ask questions like:
- “Show data for houses younger than 5 years”
- “Which feature is most important?”
- “Plot average values by category”

The system converts these queries into Python (pandas/matplotlib) code, executes it safely, and returns results as tables or visualizations.

---

## 🧠 How It Works


User Query → LLM → Code Generation → Code Cleaning → Execution → Result


1. User inputs a query in plain English  
2. LLM (Gemini via LangChain) generates Python code  
3. Code is cleaned and formatted automatically  
4. If errors occur, the system attempts to fix the code  
5. Code is executed in a safe sandbox  
6. Results are displayed (table or visualization)  

---

## 🏗️ Architecture

- **Frontend**: Streamlit  
- **Backend**: Python  
- **LLM Integration**: LangChain + Gemini API  
- **Execution Engine**: Secure sandbox using `exec()`  
- **Data Processing**: pandas  
- **Visualization**: matplotlib  

---

## 🧩 Features

- ✅ Natural language querying  
- ✅ Automatic pandas code generation  
- ✅ Safe execution environment  
- ✅ Auto-correction of generated code  
- ✅ Supports data visualization  
- ✅ Works with any CSV dataset  

---

## 🛠️ Tech Stack

- Python  
- pandas  
- matplotlib  
- Streamlit  
- LangChain  
- Gemini API  

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/ai-data-analyst-copilot.git
cd ai-data-analyst-copilot
pip install -r requirements.txt

Create a .env file in the root directory:

GOOGLE_API_KEY=your_api_key_here

Run the application:

streamlit run app.py