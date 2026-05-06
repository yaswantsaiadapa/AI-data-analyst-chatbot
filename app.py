import streamlit as st
import matplotlib.pyplot as plt
from data.loader import load_csv
from orchestrator.codegen import generate_code, fix_code
from execution.executor import execute_code
from utils.classifier import compress_result
if "memory" not in st.session_state:
    st.session_state.memory = []



st.title("Data Analysis Bot")
uploaded_file=st.file_uploader("Upload CSV file",type=["csv"])
if uploaded_file is not None:
    df=load_csv(uploaded_file)
    sample_data = df.sample(min(10, len(df))).to_dict()
    if df is not None:
        st.success("File Loaded Successfully")

        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.subheader("Columns")
        st.write(df.columns.tolist())

        st.subheader("Basic Info")
        st.write(f"Rows:{df.shape[0]} , Columns:{df.shape[1]}")

    else:
        st.error("Error loading file")

st.subheader("Ask a question")
query=st.text_input("Enter your query about the data")
if query and uploaded_file is not None:
    columns=df.columns.to_list()
    try:
        code=generate_code(columns,query,sample_data,st.session_state.memory)
    except Exception as e:
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            st.warning(" Model is very busy right now. Please wait a moment and try again.")
            st.stop()
        else:
            st.error(f"Unexpected error: {e}")
            st.stop()
    st.write("Raw LLM Output:")
    st.code(code, language="python")


    output,error=execute_code(code,df)
    if error:
        count=0
        while(error and count<1):
            st.warning("Error Detected. Trying to Fix.....")
            fixed_code=fix_code(code,error,columns,sample_data,st.session_state.memory,query)
            st.write("Fixed Code:")
            st.code(fixed_code, language="python")
            output,error=execute_code(fixed_code, df)
            if error:
                st.error(f"Fixing Failed: {error}")
                count=count+1
            else:
                st.subheader("Result")
                if output["result"] is not None:
                    compressed = compress_result(output["result"])
                    st.session_state.memory.append({
                        "query": query,
                        "code": code,
                        "result": compressed
                    })

                    st.session_state.memory = st.session_state.memory[-5:]
                    st.write(output["result"])
                    if output["fig"] and len(plt.get_fignums()) > 0:
                        st.pyplot(output["fig"])
                break
    else:
        st.subheader("Result")
        if output["result"] is not None:
            compressed = compress_result(output["result"])
            st.session_state.memory.append({
                        "query": query,
                        "code": code,
                        "result": compressed
                    })

            st.session_state.memory = st.session_state.memory[-5:]
            st.write(output["result"])
            if output["fig"] and len(plt.get_fignums()) > 0:
                st.pyplot(output["fig"])

    st.subheader("History")
    for item in st.session_state.memory[::-1]:
        st.write("Query:", item["query"])
        st.write("Result:", item["result"])