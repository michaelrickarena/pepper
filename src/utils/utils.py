import pandas as pd

def clean_ending_arr(df, column_name='Ending ARR'):
    df[column_name] = df[column_name].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
    return df

def clean_mrr_growth(df, column_name='% MRR Growth'):
    df[column_name] = df[column_name].str.replace('%', '', regex=False).astype(float) / 100
    return df