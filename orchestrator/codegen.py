from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from utils.prompts import CODEGEN_PROMPT, FIX_PROMPT, CLASSIFIER_PROMPT, ML_INTENT_PROMPT
from utils.classifier import classify_query_rule
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=api_key
)

prompt = PromptTemplate(
    input_variables=["columns", "query", "sample_data", "memory"],
    template=CODEGEN_PROMPT
)

fix_prompt = PromptTemplate(
    input_variables=["original_code", "error", "columns", "sample_data", "memory", "query"],
    template=FIX_PROMPT
)

classifier_prompt = PromptTemplate(
    input_variables=["query"],
    template=CLASSIFIER_PROMPT
)

chain = LLMChain(llm=llm, prompt=prompt)
fix_chain = LLMChain(llm=llm, prompt=fix_prompt)
classifier_chain = LLMChain(llm=llm, prompt=classifier_prompt)

ml_intent_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["query"],
        template=ML_INTENT_PROMPT
    )
)

gemini_ml_intent_chain = LLMChain(
    llm=gemini_llm,
    prompt=PromptTemplate(
        input_variables=["query"],
        template=ML_INTENT_PROMPT
    )
)

gemini_chain = LLMChain(llm=gemini_llm, prompt=prompt)
gemini_fix_chain = LLMChain(llm=gemini_llm, prompt=fix_prompt)
gemini_classifier_chain = LLMChain(llm=gemini_llm, prompt=classifier_prompt)


def detect_ml_task_smart(query):
    try:
        response = ml_intent_chain.invoke({"query": query})
    except:
        try:
            response = gemini_ml_intent_chain.invoke({"query": query})
        except:
            return None

    if isinstance(response, dict):
        result = response.get("text", "").strip()
    elif hasattr(response, "content"):
        result = response.content.strip()
    else:
        result = str(response).strip()

    return result.lower()


def detect_ml_task(query):
    q = query.lower()

    if any(w in q for w in ["predict", "regression", "forecast"]):
        return "regression"

    if any(w in q for w in ["classify", "classification", "label"]):
        return "classification"

    if any(w in q for w in ["cluster", "group", "segmentation"]):
        return "clustering"

    return detect_ml_task_smart(query)


def fix_indentation(code):
    lines = code.split("\n")
    fixed_lines = []
    indent_level = 0

    for line in lines:
        stripped = line.strip()

        if not stripped:
            fixed_lines.append("")
            continue

        if stripped.startswith(("else:", "elif", "except", "finally")):
            indent_level = max(indent_level - 1, 0)

        fixed_lines.append("    " * indent_level + stripped)

        if stripped.endswith(":"):
            indent_level += 1

    return "\n".join(fixed_lines)


def clean_code(response: str) -> str:
    if not response:
        return ""

    if response.startswith("```"):
        response = response.replace("```python", "").replace("```", "").strip()

    response = response.replace(";", "\n")

    response = re.sub(r"(?<!\n)(?<!,)(\s)([a-zA-Z_]+\s*=[^=])", r"\n\2", response)

    response = re.sub(
        r"if (.*?): (.*?) else: (.*)",
        r"if \1:\n    \2\nelse:\n    \3",
        response
    )

    response = response.strip()
    response = fix_indentation(response)

    return response


def classify_query(query):
    rule_type = classify_query_rule(query)

    if rule_type == "general":
        try:
            response = classifier_chain.invoke({"query": query})
        except Exception:
            response = gemini_classifier_chain.invoke({"query": query})

        if isinstance(response, dict):
            result = response.get("text", "").strip()
        elif hasattr(response, "content"):
            result = response.content.strip()
        else:
            result = str(response).strip()

        return result.lower()

    return rule_type


def generate_code(columns, query, sample_data, memory):
    query_type = classify_query(query)
    ml_task = detect_ml_task(query)

    print("Query Type:", query_type)
    print("ML Task:", ml_task)

    try:
        response = chain.invoke({
            "columns": columns,
            "query": f"{query}\n\nML Task Hint: {ml_task}",
            "sample_data": sample_data,
            "memory": memory
        })
    except Exception as e:
        response = gemini_chain.invoke({
            "columns": columns,
            "query": f"{query}\n\nML Task Hint: {ml_task}",
            "sample_data": sample_data,
            "memory": memory
        })

    if isinstance(response, dict):
        response = response.get("text", "").strip()
    elif hasattr(response, "content"):
        response = response.content.strip()
    else:
        response = str(response).strip()

    return clean_code(response)


def fix_code(original_code, error, columns, sample_data, memory, query):
    ml_task = detect_ml_task(query)

    try:
        response = fix_chain.invoke({
            "original_code": original_code,
            "error": error,
            "columns": columns,
            "sample_data": sample_data,
            "memory": memory,
            "query": f"ML Task Hint: {ml_task}"
        })
    except Exception:
        response = gemini_fix_chain.invoke({
            "original_code": original_code,
            "error": error,
            "columns": columns,
            "sample_data": sample_data,
            "memory": memory,
            "query": f"ML Task Hint: {ml_task}"
        })

    if isinstance(response, dict):
        response = response.get("text", "").strip()
    elif hasattr(response, "content"):
        response = response.content.strip()
    else:
        response = str(response).strip()

    return clean_code(response)