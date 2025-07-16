import pandas as pd
import os
import numpy as np
from utils.utils import clean_ending_arr, clean_mrr_growth, load_and_clean_data

def process_segments():
    # Load and clean the data
    df = load_and_clean_data()

    # Define segmentation logic
    conditions = [
        (df['Ending ARR'] >= 100000) & (df['% MRR Growth'] >= 0.10),
        (df['Ending ARR'] >= 100000) & (df['% MRR Growth'] >= 0) & (df['% MRR Growth'] < 0.10),
        (df['Ending ARR'] < 100000) & (df['% MRR Growth'] >= 0.10),
        (df['Ending ARR'] < 100000) & (df['% MRR Growth'] >= 0) & (df['% MRR Growth'] < 0.10),
        (df['% MRR Growth'] < 0)
    ]
    segment_names = [
        'Strategic Accounts',
        'Key Accounts',
        'Growth Accounts',
        'Standard Accounts',
        'At Risk Accounts'
    ]

    df['Segment'] = np.select(conditions, segment_names, default='Uncategorized')

    # Create summary table with median metrics
    summary = df.groupby('Segment').agg({
        'Distributor Name': 'count',  # Count of accounts
        'Ending ARR': ['sum', 'median', 'mean'],  # Total and median Ending ARR
        '% MRR Growth': ['mean', 'median'],  # Average and median % MRR Growth
        '# of Products': ['mean', lambda x: (x == 1).sum()]  # Average and % of rows with 1 product
    }).reset_index()

    # Flatten multi-level columns
    summary.columns = ['Segment', '# Accounts', 'Total Ending ARR', 'Median Ending ARR','Average Ending ARR',
                       'Average % MRR Growth', 'Median % MRR Growth',
                       'Average # of Products', '# of Rows with 1 Product']

    # Add % of Total Accounts
    total_accounts = summary['# Accounts'].sum()
    summary['% of Total Accounts'] = (summary['# Accounts'] / total_accounts).round(4)

    # Add % of Total ARR
    total_arr = summary['Total Ending ARR'].sum()
    summary['% of Total ARR'] = (summary['Total Ending ARR'] / total_arr * 100).round(4)

    # Convert '% of Total ARR' to a percentage
    summary['% of Total ARR'] = (summary['% of Total ARR'] / 100).round(4)

    # Add 'Average Ending ARR' column
    summary['Average Ending ARR'] = (summary['Total Ending ARR'] / summary['# Accounts']).round(2)

    # Round specific columns to 2 decimals
    summary['Average % MRR Growth'] = summary['Average % MRR Growth'].round(4)
    summary['Median % MRR Growth'] = summary['Median % MRR Growth'].round(4)
    summary['Average # of Products'] = summary['Average # of Products'].round(2)
    summary['% of Customers in Segment With 1 Product'] = (summary['# of Rows with 1 Product'] / summary['# Accounts']).round(4)
    summary.drop(columns=['# of Rows with 1 Product'], inplace=True)

    # Export summary table
    output_folder = '../data/Segments'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'segments_summary.csv')
    summary.to_csv(output_file, index=False)
    print(f"Segment summary exported to {output_file}")

    # Export detailed data with segments
    output_file_detailed = os.path.join(output_folder, 'segments_analysis.csv')
    df.to_csv(output_file_detailed, index=False)
    print(f"Segment analysis exported to {output_file_detailed}")