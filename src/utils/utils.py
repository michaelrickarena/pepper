import pandas as pd

def create_new_columns():
    df = pd.read_csv('../Account Segmentation & Revenue Team Structuring Exercise - Data.csv')

    # Clean 'Starting MRR' and 'Ending MRR' columns
    df['Starting MRR'] = df['Starting MRR'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
    df['Ending MRR'] = df['Ending MRR'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)

    df['MRR Growth'] = df['Ending MRR'] - df['Starting MRR']
    df['MRR Growth'] = df['MRR Growth'].apply(lambda x: f"${x:,.0f}" if x < 0 else f"${x:,.0f}")

    # Calculate % MRR Growth
    df['% MRR Growth'] = (df['Ending MRR'] - df['Starting MRR']) / df['Starting MRR']
    df['% MRR Growth'] = df['% MRR Growth'].apply(lambda x: f"{x:.2%}")

    # Calculate Starting ARR
    df['Starting ARR'] = df['Starting MRR'] * 12
    df['Starting ARR'] = df['Starting ARR'].apply(lambda x: f"${x:,.0f}")

    # Calculate Ending ARR
    df['Ending ARR'] = df['Ending MRR'] * 12
    df['Ending ARR'] = df['Ending ARR'].apply(lambda x: f"${x:,.0f}")

    df['Starting MRR'] = df['Starting MRR'].apply(lambda x: f"${x:,.0f}")
    df['Ending MRR'] = df['Ending MRR'].apply(lambda x: f"${x:,.0f}")


    # Export to CSV
    df.to_csv("../cleaned_csv.csv", index=False)
    print("Data exported to test.csv")

    return df

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

    df = pd.read_csv('../cleaned_csv.csv')
    df = clean_ending_arr(df)
    df = clean_mrr_growth(df)
    return df

def add_country_and_state():
    # Load the CSV file
    file_path = '../cleaned_csv.csv'
    df = pd.read_csv(file_path)

    # Update the Country, State, and City columns
    df['Country'] = df['Location'].apply(lambda x: x.split(',')[-1].strip() if pd.notna(x) else None)
    df['State'] = df['Location'].apply(lambda x: x.split(',')[1].strip() if pd.notna(x) else None)
    df['City'] = df['Location'].apply(lambda x: x.split(',')[0].strip() if pd.notna(x) else None)

    # Overwrite only the updated columns in the CSV
    df.to_csv(file_path, index=False)
    print(f"Updated Country, State, and City columns in {file_path}")