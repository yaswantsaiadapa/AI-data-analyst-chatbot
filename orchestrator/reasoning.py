from utils.prompts import REASONING_PROMPT
import pandas as pd
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = PromptTemplate(
    input_variables=[
        "query",
        "columns",
        "sample_data",
        "memory"
    ],
    template=REASONING_PROMPT
)

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

gemini_chain = LLMChain(
    llm=gemini_llm,
    prompt=prompt
)

def generative_reasoning(query,columns,sample_data,dataset_summary, memory):
    try:
        response=chain.invoke({
            "query": query,
            "columns": columns,
            "sample_data": sample_data,
            "dataset_summary": dataset_summary,
            "memory": memory
        })
    except Exception:
        response=gemini_chain.invoke(
            {
                "query":query,
                "columns":columns,
                "sample_data":sample_data,
                "dataset_summary": dataset_summary,
                "memory": memory,
            }
        )
    print("using generative reasoning")
    if isinstance(response, dict):
        return response.get("text","").strip()
    elif hasattr(response, "content"):
        return response.content.strip()
    return str(response).strip()

