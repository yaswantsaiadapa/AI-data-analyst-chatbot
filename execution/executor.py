import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re

def execute_code(code, df):
    dangerous_patterns = [r'\bos\b', r'\bsys\b', r'\bopen\b', r'\beval\b', r'\bexec\b', r'\bsubprocess\b']
    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            return None, f"Error: Code contains potentially dangerous keyword: '{pattern}'"

    safe_globals = {
        "__builtins__": {},
    }
    safe_locals = {
        "df": df,
        "pd": pd,
        "plt": plt,
    }

    try:
        plt.close("all")
        exec(code, safe_globals, safe_locals)

        result = safe_locals.get("result", None)

        fig = plt.gcf()
        if not fig.get_axes():
            fig = None

        return {"result": result, "fig": fig}, None
    except Exception as e:
        return None, str(e)
