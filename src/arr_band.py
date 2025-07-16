import pandas as pd
import os
from utils.utils import clean_ending_arr, clean_mrr_growth, load_and_clean_data

def process_arr_band():
    df = load_and_clean_data()
    # Map ARR Band ranges to numerical ranges
    arr_band_ranges = {
        '< $10k': (0, 10000),
        '$10k - $25k': (10000, 25000),
        '$25k - $50k': (25000, 50000),
        '$50k - $75k': (50000, 75000),
        '$50 - $75k': (50000, 75000),
        '$75k - $100k': (75000, 100000),
        '$100k - $250k': (100000, 250000),
        '$250k+': (250000, float('inf'))
    }

    # Apply the mapping to the ARR Band column
    df['ARR Band Range'] = df['ARR Band'].map(arr_band_ranges)
    # Filter rows where Ending ARR is lower than the lower bound of the ARR Band Range
    df['Lower Bound'] = df['ARR Band Range'].apply(lambda x: x[0] if pd.notna(x) else None)
    df['Upper Bound'] = df['ARR Band Range'].apply(lambda x: x[1] if pd.notna(x) else None)
    df['Middle'] = df.apply(lambda row: (row['Lower Bound'] + row['Upper Bound']) / 2 if pd.notna(row['Lower Bound']) and pd.notna(row['Upper Bound']) else None, axis=1)

    # Filter customers based on which range they fall into
    below_lower = df[df['Ending ARR'] < df['Lower Bound']]
    middle_to_lower = df[(df['Ending ARR'] >= df['Lower Bound']) & (df['Ending ARR'] < df['Middle'])]
    middle_to_upper = df[(df['Ending ARR'] >= df['Middle']) & (df['Ending ARR'] <= df['Upper Bound'])]
    above_upper = df[df['Ending ARR'] > df['Upper Bound']]


    # Create summary tables
    def create_summary_table(group_name, group_df):
        return {
            'Group': group_name,
            '# Accounts': len(group_df),
            '% of Total': len(group_df) / 1000,
            'Average Ending ARR': int(group_df['Ending ARR'].mean()),
            'Average % MRR Growth': group_df['% MRR Growth'].mean(),
            'Average # of Products': group_df['# of Products'].mean()
        }

    # Generate summary tables
    summary_tables = [
        create_summary_table('Below Lower Bound', below_lower),
        create_summary_table('Middle to Lower Bound', middle_to_lower),
        create_summary_table('Middle to Upper Bound', middle_to_upper),
        create_summary_table('Above Upper Bound', above_upper)
    ]

    summary_df = pd.DataFrame(summary_tables)
    summary_df = summary_df.round({
        '% of Total': 2,
        'Average % MRR Growth': 2,
        'Average # of Products': 2
    })
    # Create ARR band folder if it doesn't exist
    output_folder = '../data/ARR Band'
    os.makedirs(output_folder, exist_ok=True)

    # Export to CSV
    output_file = os.path.join(output_folder, 'arr_band_summary.csv')
    summary_df.to_csv(output_file, index=False)
    print(f"Summary table exported to {output_file}")
