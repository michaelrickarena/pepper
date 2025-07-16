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

def add_country_and_state():
    # Load the CSV file
    file_path = '../Account Segmentation & Revenue Team Structuring Exercise - Data.csv'
    df = pd.read_csv(file_path)

    # Update the Country, State, and City columns
    df['Country'] = df['Location'].apply(lambda x: x.split(',')[-1].strip() if pd.notna(x) else None)
    df['State'] = df['Location'].apply(lambda x: x.split(',')[1].strip() if pd.notna(x) else None)
    df['City'] = df['Location'].apply(lambda x: x.split(',')[0].strip() if pd.notna(x) else None)

    # Overwrite only the updated columns in the CSV
    df.to_csv(file_path, index=False)
    print(f"Updated Country, State, and City columns in {file_path}")