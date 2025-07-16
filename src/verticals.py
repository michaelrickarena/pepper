import pandas as pd
import os
from utils.utils import clean_ending_arr, clean_mrr_growth, load_and_clean_data

def process_verticals():
    # Load and clean the data
    df = load_and_clean_data()

    # Example: Group by a 'Vertical' column and calculate summary statistics
    if 'Vertical' in df.columns:
        vertical_summary = df.groupby('Vertical').agg({
            'Ending ARR': 'mean',
            '% MRR Growth': 'mean',
            '# of Products': 'mean'
        }).reset_index()

        vertical_summary['# Accounts'] = df.groupby('Vertical').size().values
        vertical_summary['% of Accounts'] = (vertical_summary['# Accounts'] / 1000).round(2)

        # Round columns to 2 decimals
        vertical_summary[['% MRR Growth', '# of Products']] = vertical_summary[['% MRR Growth', '# of Products']].round(2)
        vertical_summary[['Ending ARR']] = vertical_summary[['Ending ARR']].round(0).astype(int)

        # Rename 'Ending ARR' to 'Average Ending ARR'
        vertical_summary = vertical_summary.rename(columns={'Ending ARR': 'Average Ending ARR', 
                                                           '% MRR Growth': 'Average % MRR Growth',
                                                           '# of Products': 'Average # of Products'})

        # Create output folder if it doesn't exist
        output_folder = '../data/Verticals'
        os.makedirs(output_folder, exist_ok=True)

        # Export to CSV
        output_file = os.path.join(output_folder, 'verticals_summary.csv')
        vertical_summary.to_csv(output_file, index=False)
        print(f"Verticals summary exported to {output_file}")
    else:
        print("No 'Vertical' column found in the data.")