# 📊 AI Data Analyst Copilot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-data-analyst-chatbot.streamlit.app/)

## 🚀 Overview
The **AI Data Analyst Copilot** is an AI-powered tool that enables users to analyze datasets using natural language queries instead of writing code. 

Users can upload a CSV file and ask questions like:
- “Show data for houses younger than 5 years”
- “Which feature is most important?”
- “Plot average values by category”
- "What is the general trend in the dataset?"

The system converts these queries into Python (pandas/matplotlib) code, executes it safely, and returns results as tables or visualizations. It also supports conversational reasoning to provide machine learning insights without needing explicit code execution.

---

## 🧩 Key Features

- **✅ Natural Language Querying**: Talk to your data in plain English.
- **✅ Automatic Code Generation**: Translates queries into pandas and matplotlib code.
- **✅ Self-Correcting Execution**: Automatically identifies errors during execution and attempts to fix the generated code.
- **✅ Conversational Reasoning & ML Insights**: Classifies queries to provide analytical insights and reasoning directly when code execution isn't required.
- **✅ Multi-Tab Results**: View the raw data result, generated visualizations, and an AI-generated explanation of the findings.
- **✅ Chat History Context**: Remembers your previous queries to maintain conversational context.
- **✅ Comprehensive Dataset Overview**: Instantly view dataset statistics including rows, columns, missing values, and a data preview.
- **✅ Safe Execution Environment**: Code is executed in a secure sandbox.
- **✅ Universal CSV Support**: Works seamlessly with any uploaded CSV dataset.

---

## 🧠 How It Works

User Query → Intent Classification → (Reasoning / Code Generation) → Code Cleaning → Execution → Explanation & Result

1. User uploads a dataset and inputs a query in plain English.
2. The system classifies the query intent (e.g., reasoning vs. data manipulation).
3. **If Reasoning**: The LLM generates analytical insights based on data summaries and samples.
4. **If Code Generation**: 
   - LLM (Gemini API) generates Python code.
   - Code is cleaned and formatted automatically.
   - If errors occur during execution, the system attempts to fix the code using error feedback.
   - Code is executed in a safe sandbox.
5. Results are displayed across three tabs: **Result**, **Visualization**, and **Explanation**.

---

## 🏗️ Architecture

- **Frontend**: Streamlit  
- **Backend**: Python  
- **LLM Integration**: LangChain + Gemini API  
- **Execution Engine**: Secure sandbox using `exec()`  
- **Data Processing**: pandas  
- **Visualization**: matplotlib  
- **Query Classification**: Custom rule-based and LLM classifiers

---

## 🛠️ Tech Stack

- **Python**
- **pandas**
- **matplotlib**
- **Streamlit**
- **LangChain**
- **Gemini API**

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/ai-data-analyst-copilot.git
cd ai-data-analyst-copilot
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```