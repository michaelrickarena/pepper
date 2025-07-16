import pandas as pd

def clean_ending_arr(df, column_name='Ending ARR'):
    df[column_name] = df[column_name].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
    return df

def clean_mrr_growth(df, column_name='% MRR Growth'):
    df[column_name] = df[column_name].str.replace('%', '', regex=False).astype(float) / 100
    return df

def load_and_clean_data():
    """
    Load the CSV file and clean the data by applying necessary transformations.
    """

    df = pd.read_csv('../Account Segmentation & Revenue Team Structuring Exercise - Data.csv')
    df = clean_ending_arr(df)
    df = clean_mrr_growth(df)
    return df