from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from utils.prompts import CODEGEN_PROMPT, FIX_PROMPT
from dotenv import load_dotenv
import os
import re

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key
)

# Prompts
prompt = PromptTemplate(
    input_variables=["columns", "query", "sample_data"],
    template=CODEGEN_PROMPT
)

fix_prompt = PromptTemplate(
    input_variables=["original_code", "error", "columns", "sample_data"],
    template=FIX_PROMPT
)

# Chains
chain = LLMChain(llm=llm, prompt=prompt)
fix_chain = LLMChain(llm=llm, prompt=fix_prompt)


# 🔥 INDENTATION FIXER (CORE)
def fix_indentation(code: str) -> str:
    lines = code.split("\n")
    fixed_lines = []
    indent_level = 0

    for line in lines:
        stripped = line.strip()

        if not stripped:
            fixed_lines.append("")
            continue

        # Reduce indent for else/elif/except/finally
        if stripped.startswith(("else:", "elif", "except", "finally")):
            indent_level = max(indent_level - 1, 0)

        # Apply indentation
        fixed_lines.append("    " * indent_level + stripped)

        # Increase indent after colon
        if stripped.endswith(":"):
            indent_level += 1

    return "\n".join(fixed_lines)


# 🔥 CLEANING FUNCTION
def clean_code(response: str) -> str:
    if not response:
        return ""

    # Remove markdown
    if response.startswith("```"):
        response = response.replace("```python", "").replace("```", "").strip()

    # Replace semicolons
    response = response.replace(";", "\n")

    # Add newline before assignments
    response = re.sub(r"(?<!\n)(\s)([a-zA-Z_]+\s*=)", r"\n\2", response)

    # Fix inline if-else
    response = re.sub(
        r"if (.*?): (.*?) else: (.*)",
        r"if \1:\n    \2\nelse:\n    \3",
        response
    )

    # Strip
    response = response.strip()

    # 🔥 APPLY INDENTATION FIX
    response = fix_indentation(response)

    return response


# 🔹 Generate code
def generate_code(columns, query, sample_data):
    response = chain.invoke({
        "columns": columns,
        "query": query,
        "sample_data": sample_data
    })

    if isinstance(response, dict):
        response = response.get("text", "").strip()
    elif hasattr(response, "content"):
        response = response.content.strip()
    else:
        response = str(response).strip()

    response = clean_code(response)

    return response


# 🔹 Fix broken code
def fix_code(original_code, error, columns, sample_data):
    response = fix_chain.invoke({
        "original_code": original_code,
        "error": error,
        "columns": columns,
        "sample_data": sample_data
    })

    if isinstance(response, dict):
        response = response.get("text", "").strip()
    elif hasattr(response, "content"):
        response = response.content.strip()
    else:
        response = str(response).strip()

    response = clean_code(response)

    return response