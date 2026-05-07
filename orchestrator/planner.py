## file not in usage maybe used in future for agentic planning 


from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from utils.prompts import PLANNER_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from utils.prompts import PLANNER_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=groq_key
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=api_key
)

planner_prompt=PromptTemplate(
    input_variables=["query"],
    template=PLANNER_PROMPT
)

planner_chain=LLMChain(
    llm=llm,
    prompt=planner_prompt
)

gemini_planner_chain = LLMChain(
    llm=gemini_llm,
    prompt=planner_prompt
)


def generate_plan(query):
    try:
        response = planner_chain.invoke({
            "query": query
        })
    except Exception:
        response = gemini_planner_chain.invoke({
            "query": query
        })

    if isinstance(response, dict):
        response = response.get("text", "").strip()
    elif hasattr(response, "content"):
        response = response.content.strip()
    else:
        response = str(response).strip()

    return response