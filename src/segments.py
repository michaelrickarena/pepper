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

    # Calculate % US Accounts and % Canada Accounts
    country_summary = df.groupby(['Segment', 'Country'])['Distributor Name'].count().unstack(fill_value=0)
    total_accounts_per_segment = country_summary.sum(axis=1)
    country_summary['% US Accounts'] = (country_summary.get('US', 0) / total_accounts_per_segment).round(4)
    country_summary['% Canada Accounts'] = (country_summary.get('Canada', 0) / total_accounts_per_segment).round(4)

    # Merge the calculated columns into the summary DataFrame
    summary = summary.merge(country_summary[['% US Accounts', '% Canada Accounts']], on='Segment', how='left')

    # Calculate US Total ARR ($MM) and Canada Total ARR ($MM)
    arr_summary = df.groupby(['Segment', 'Country'])['Ending ARR'].sum().unstack(fill_value=0)
    arr_summary['US Total ARR ($MM)'] = (arr_summary.get('US', 0) / 1_000_000).round(2)  # Convert to millions
    arr_summary['Canada Total ARR ($MM)'] = (arr_summary.get('Canada', 0) / 1_000_000).round(2)  # Convert to millions

    # Merge the calculated columns into the summary DataFrame
    summary = summary.merge(arr_summary[['US Total ARR ($MM)', 'Canada Total ARR ($MM)']], on='Segment', how='left')

    # Export the updated summary table
    output_folder = '../data/Segments'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'segments_summary.csv')
    summary.to_csv(output_file, index=False)
    print(f"Updated segment summary exported to {output_file}")

    # Export detailed data with segments
    output_file_detailed = os.path.join(output_folder, 'segments_analysis.csv')
    df.to_csv(output_file_detailed, index=False)
    print(f"Segment analysis exported to {output_file_detailed}")



    # Create a pivot table to calculate the percentage of verticals in each segment
    vertical_summary = (
        df.groupby(['Segment', 'Vertical'])['Distributor Name']
        .count()
        .reset_index()
        .rename(columns={'Distributor Name': 'Count'})
    )

    # Calculate the total count of each vertical
    vertical_totals = vertical_summary.groupby('Vertical')['Count'].sum().reset_index()
    vertical_totals = vertical_totals.rename(columns={'Count': 'Vertical Total'})

    # Merge the totals back into the vertical summary
    vertical_summary = vertical_summary.merge(vertical_totals, on='Vertical')

    # Calculate the percentage of each segment in the vertical
    vertical_summary['% of Vertical'] = (vertical_summary['Count'] / vertical_summary['Vertical Total']).round(4)

    # Pivot the table to get the desired format
    pivot_table = vertical_summary.pivot(index='Vertical', columns='Segment', values='% of Vertical').fillna(0)

    # Export the pivot table
    output_file_verticals = os.path.join(output_folder, 'segments_verticals_summary.csv')
    pivot_table.to_csv(output_file_verticals)
    print(f"Verticals summary exported to {output_file_verticals}")