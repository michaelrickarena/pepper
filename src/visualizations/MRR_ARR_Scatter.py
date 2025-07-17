import pandas as pd
import matplotlib.pyplot as plt
import os

def create_mrr_growth_vs_arr_scatter():
    # Load the data
    file_path = '../data/Segments/segments_analysis.csv'
    df = pd.read_csv(file_path)

    # Filter out rows with Ending ARR above 300,000
    df = df[df['Ending ARR'] <= 300000]

    # Extract relevant columns
    ending_arr = df['Ending ARR']
    mrr_growth = df['% MRR Growth']
    segments = df['Segment']

    # Define desired segment order and custom color for Strategic
    desired_order = ['Strategic Accounts', 'Key Accounts', 'Growth Accounts', 'Standard Accounts', 'At Risk Accounts']
    custom_colors = {
        'Strategic Accounts': "#D6AC23",
        'Key Accounts': "#165e91",
        'Growth Accounts': "#0bac06",
        'Standard Accounts': "#CE0EBE",
        'At Risk Accounts': "#d30d0d"
    }

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create scatter plots for each segment with custom colors
    for segment in desired_order:
        segment_data = df[df['Segment'] == segment]
        ax.scatter(segment_data['Ending ARR'], segment_data['% MRR Growth'],
                   c=custom_colors[segment], label=segment, alpha=0.8, edgecolors='w', s=100)

    # Add labels and title
    ax.set_xlabel('Ending ARR', fontsize=12, color='black')
    ax.set_ylabel('% MRR Growth', fontsize=12, color='black')
    ax.set_title('% MRR Growth vs. Ending ARR by Segment', fontsize=14, color='black')

    # Add legend in desired order
    ax.legend(title='Segments', loc='upper left', bbox_to_anchor=(1, 1))

    # Format the x-axis and y-axis
    ax.tick_params(axis='both', which='major', labelsize=10, colors='black')
    ax.grid(True, linestyle='--', alpha=0.6)

    # Format x-axis ticks as currency
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    # Format y-axis ticks as percentages
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))

    # Save the chart
    output_folder = '../charts'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'mrr_growth_vs_arr_scatter.png')
    plt.savefig(output_file, bbox_inches='tight', transparent=True)
    print(f"Chart saved to {output_file}")

    plt.close()  # Close the figure to free memory

if __name__ == '__main__':
    create_mrr_growth_vs_arr_scatter()