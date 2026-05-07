import streamlit as st
import matplotlib.pyplot as plt

from data.loader import load_csv
from orchestrator.codegen import generate_code, fix_code
from execution.executor import execute_code

from utils.classifier import (
    compress_result,
    classify_query_rule,
    summarize_dataframe
)

from orchestrator.explainer import generate_explanation
from orchestrator.reasoning import generative_reasoning


st.set_page_config(
    page_title="AI Data Analyst Bot",
    layout="wide"
)

if "memory" not in st.session_state:
    st.session_state.memory = []


st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    max-width:1100px;
}

[data-testid="stSidebar"]{
    background-color:#0e1117;
}

.chat-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-bottom:10px;
}

.chat-subtitle{
    text-align:center;
    font-size:18px;
    color:#9ca3af;
    margin-bottom:35px;
    max-width:700px;
    margin-left:auto;
    margin-right:auto;
}

.query-box{
    padding:10px;
    border-radius:14px;
    background-color:#111827;
    margin-bottom:25px;
}

.history-card{
    padding:14px;
    border-radius:12px;
    background-color:#161b22;
    margin-bottom:12px;
    border:1px solid #232a36;
}

.small-text{
    font-size:13px;
    color:#9ca3af;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div class="chat-title">
        AI Data Analyst Bot
    </div>

    <div class="chat-subtitle">
        Analyze datasets using natural language queries, generate visualizations,
        perform machine learning analysis and receive conversational insights instantly.
    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:

    st.header("History")

    if len(st.session_state.memory) == 0:

        st.info("No previous queries")

    else:

        for item in st.session_state.memory[::-1]:

            st.markdown(
                f"""
                <div class="history-card">
                    <b>{item['query']}</b>
                    <div class="small-text">
                        {str(item['result'])[:70]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    if st.button("Clear History"):

        st.session_state.memory = []

        st.rerun()


uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


if uploaded_file is None:

    st.info(
        "Upload a CSV dataset to begin analysis"
    )

else:

    df = load_csv(uploaded_file)

    sample_data = df.sample(
        min(10, len(df))
    ).to_dict()

    dataset_summary = summarize_dataframe(df)

    columns = df.columns.to_list()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="query-box">',
        unsafe_allow_html=True
    )

    query = st.text_input(
        "Ask Your Question",
        placeholder="Ask questions about your dataset...",
        label_visibility="collapsed"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    with st.expander("Dataset Details"):

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "Rows",
                df.shape[0]
            )

        with metric2:

            st.metric(
                "Columns",
                df.shape[1]
            )

        with metric3:

            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        st.markdown("### Columns")

        st.write(columns)

        st.markdown("### Dataset Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

    if query:

        query_type = classify_query_rule(query)

        if query_type == "reasoning":

            with st.spinner(
                "Generating analytical insight..."
            ):

                response = generative_reasoning(
                    query,
                    columns,
                    sample_data,
                    dataset_summary,
                    st.session_state.memory
                )

            st.session_state.memory.append({
                "query": query,
                "result": response
            })

            st.session_state.memory = (
                st.session_state.memory[-5:]
            )

            st.markdown("## Response")

            st.write(response)

            st.stop()

        try:

            with st.spinner(
                "Generating analysis..."
            ):

                code = generate_code(
                    columns,
                    query,
                    sample_data,
                    st.session_state.memory
                )

        except Exception as e:

            if (
                "503" in str(e)
                or "UNAVAILABLE" in str(e)
            ):

                st.warning(
                    "Model is busy right now. Please try again."
                )

                st.stop()

            else:

                st.error(
                    f"Unexpected Error: {e}"
                )

                st.stop()

        with st.expander("Generated Code"):

            st.code(
                code,
                language="python"
            )

        output, error = execute_code(
            code,
            df
        )

        if error:

            count = 0

            while error and count < 1:

                st.warning(
                    "Trying to fix generated code..."
                )

                fixed_code = fix_code(
                    code,
                    error,
                    columns,
                    sample_data,
                    st.session_state.memory,
                    query
                )

                with st.expander("Fixed Code"):

                    st.code(
                        fixed_code,
                        language="python"
                    )

                output, error = execute_code(
                    fixed_code,
                    df
                )

                if error:

                    st.error(
                        f"Fix Failed: {error}"
                    )

                    count += 1

                else:

                    code = fixed_code

                    break

        if (
            output
            and output["result"] is not None
        ):

            compressed = compress_result(
                output["result"]
            )

            st.session_state.memory.append({
                "query": query,
                "code": code,
                "result": compressed
            })

            st.session_state.memory = (
                st.session_state.memory[-5:]
            )

            tab1, tab2, tab3 = st.tabs([
                "Result",
                "Visualization",
                "Explanation"
            ])

            with tab1:

                st.write(
                    output["result"]
                )

            with tab2:

                if (
                    output["fig"]
                    and len(
                        plt.get_fignums()
                    ) > 0
                ):

                    st.pyplot(
                        output["fig"],
                        clear_figure=True
                    )

                else:

                    st.info(
                        "No visualization generated"
                    )

            with tab3:

                try:

                    with st.spinner(
                        "Generating explanation..."
                    ):

                        explanation = (
                            generate_explanation(
                                query,
                                output["result"]
                            )
                        )

                    st.write(
                        explanation
                    )

                except Exception as e:

                    st.warning(
                        f"Explanation failed: {e}"
                    )