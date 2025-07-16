import pandas as pd
import os

def process_arr_band():
    df = pd.read_csv('../data/Segments/segments_analysis.csv')
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


    # Create summary tables with detailed segment alignment
    def create_detailed_summary_table(group_name, group_df):
        total_accounts = len(df)
        # Calculate count makeup for each segment
        segment_counts = group_df['Segment'].value_counts().reindex(
            ['Strategic Accounts', 'Key Accounts', 'Growth Accounts', 'Standard Accounts', 'At Risk Accounts'],
            fill_value=0
        )

        return {
            'Group': group_name,
            '# Accounts': len(group_df),
            '% of Total': round(len(group_df) / total_accounts * 100, 2),
            'Avg Ending ARR': round(group_df['Ending ARR'].mean(), 2),
            'Avg % MRR Growth': round(group_df['% MRR Growth'].mean(), 2),
            'Avg # Products': round(group_df['# of Products'].mean(), 2),
            'Strategic Accounts': segment_counts['Strategic Accounts'],
            'Key Accounts': segment_counts['Key Accounts'],
            'Growth Accounts': segment_counts['Growth Accounts'],
            'Standard Accounts': segment_counts['Standard Accounts'],
            'At Risk Accounts': segment_counts['At Risk Accounts']
        }

    # Generate detailed summary tables
    detailed_summary_tables = [
        create_detailed_summary_table('Below Lower Bound', below_lower),
        create_detailed_summary_table('Middle to Lower Bound', middle_to_lower),
        create_detailed_summary_table('Middle to Upper Bound', middle_to_upper),
        create_detailed_summary_table('Above Upper Bound', above_upper)
    ]

    detailed_summary_df = pd.DataFrame(detailed_summary_tables)

    # Create ARR band folder if it doesn't exist
    output_folder = '../data/ARR Band'
    os.makedirs(output_folder, exist_ok=True)

    # Export the detailed summary table to CSV
    output_file = os.path.join(output_folder, 'arr_band_summary.csv')
    detailed_summary_df.to_csv(output_file, index=False)
    print(f"Detailed summary table exported to {output_file}")
