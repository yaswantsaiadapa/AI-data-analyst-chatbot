import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re
import threading

def execute_code(code, df):
    dangerous_patterns = [
        r'\bos\b',
        r'\bsys\b',
        r'\bopen\b',
        r'\beval\b',
        r'\bexec\b',
        r'\bsubprocess\b',
        r'\b__import__\b',
        r'\bshutil\b',
        r'\bsocket\b'
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            return None, f"Error: Unsafe operation detected: '{pattern}'"

    safe_globals = {
        "__builtins__": __builtins__,
    }

    safe_locals = {
        "df": df,
        "pd": pd,
        "plt": plt,
        "prev_result": None,
    }

    result_container = {"result": None, "error": None}

    def run_code():
        try:
            if "memory" in globals() and memory:
                safe_locals["prev_result"] = memory[-1]["result"]
            exec(code, safe_globals, safe_locals)
            result_container["result"] = safe_locals.get("result", None)
        except Exception as e:
            result_container["error"] = str(e)

    try:
        plt.close("all")

        thread = threading.Thread(target=run_code)
        thread.start()
        thread.join(timeout=45)

        if thread.is_alive():
            return None, "Execution timed out"

        if result_container["error"]:
            return None, result_container["error"]

        fig = plt.gcf()
        if not fig.get_axes():
            fig = None

        return {"result": result_container["result"], "fig": fig}, None

    except Exception as e:
        return None, str(e)