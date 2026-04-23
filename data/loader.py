import pandas as pd
def load_csv(file):
    try:
        df=pd.read_csv(file)
        return df
    except Exception as e:
        return None,str(e)
    
