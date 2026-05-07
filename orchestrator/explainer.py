from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from utils.prompts import EXPLAIN_PROMPT
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import pandas as pd


load_dotenv()



llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)



prompt = PromptTemplate(
    input_variables=["query", "result"],
    template=EXPLAIN_PROMPT
)

chain = LLMChain(llm=llm, prompt=prompt)
gemini_chain=LLMChain(llm=gemini_llm,prompt=prompt)




def compress_result_for_explanation(result):
    try:
        if isinstance(result, pd.DataFrame):
            return result.head(10).to_string()

        if isinstance(result, pd.Series):
            return result.head(10).to_string()

        return str(result)[:2000]

    except Exception:
        return str(result)[:2000]


def generate_explanation(query, result):
    compressed_result = compress_result_for_explanation(result)

    try:
        response = chain.invoke({
            "query": query,
            "result": compressed_result
        })
    except Exception:
        response = gemini_chain.invoke({
            "query": query,
            "result": compressed_result
        })

    if isinstance(response, dict):
        explanation = response.get("text", "").strip()
    elif hasattr(response, "content"):
        explanation = response.content.strip()
    else:
        explanation = str(response).strip()

    return explanation



