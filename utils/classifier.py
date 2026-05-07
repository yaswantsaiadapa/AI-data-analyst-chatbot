import pandas as pd
def classify_query_rule(query):
    query=query.lower()
    if any(word in query for word in ["plot","chart","graph","visulaize"]):
        return "plot"
    if "group by" in query or "per" in query or "by" in query:
        return "groupby"
    if any(word in query for word in ["average", "mean", "sum", "total", "count", "max", "min"]):
        return "aggregation"
    if any(word in query for word in ["compare", "difference", "vs", "versus"]):
        return "comparison"
    if any(word in query for word in ["show", "filter", "where", "less than", "greater than", "<", ">"]):
        return "filter"
    if any(word in query for word in ["why","best","explain","reason","insight","significance","important","better"]):
        return "reasoning"
    return "general"


def compress_result(res):
    try:
        if isinstance(res, pd.DataFrame):
            if len(res) > 50:
                return res.sample(50).to_dict()
            return res.to_dict()

        elif isinstance(res, pd.Series):
            if len(res) > 50:
                return res.sample(50).to_dict()
            return res.to_dict()
        return res
    except:
        return str(res)


def summarize_dataframe(df):

    try:

        summary = {}

        summary["columns"] = df.columns.tolist()

        summary["shape"] = df.shape

        numeric_df = df.select_dtypes(include="number")

        if not numeric_df.empty:

            summary["statistics"] = (
                numeric_df.describe()
                .round(2)
                .to_dict()
            )

        summary["sample_rows"] = (
            df.sample(min(20, len(df)))
            .to_dict()
        )

        return str(summary)[:5000]

    except Exception:

        return str(df.head(20).to_dict())
        