import pandas as pd

def fetch_dj_as_pd(table):
    return pd.DataFrame(table.fetch(as_dict=True))
