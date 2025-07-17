import pandas as pd
import matplotlib.pyplot as plt
import os

def create_arr_and_growth_by_vertical_chart():
    # Load the data
    file_path = '../data/Verticals/verticals_summary.csv'
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please check the file path.")
        return

    # Calculate Ending ARR by multiplying Average Ending ARR by # Accounts
    df['Ending ARR'] = df['Average Ending ARR'] * df['# Accounts']

    # Extract relevant columns
    verticals = df['Vertical']
    ending_arr = df['Ending ARR']
    mrr_growth = df['Average % MRR Growth']

    # Create the figure and axis
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot Ending ARR on the primary axis with a single color
    bar_width = 0.4
    x = range(len(verticals))
    ax1.bar(x, ending_arr, width=bar_width, label='Ending ARR', color='#FF5733')

    # Multiply MRR Growth values by 100 before graphing as bars
    mrr_growth = mrr_growth * 100

    # Create a secondary axis for % MRR Growth as bars beside ARR
    ax2 = ax1.twinx()
    ax2.bar([i + bar_width for i in x], mrr_growth, width=bar_width, label='% MRR Growth', color='#3498DB')

    # Customize axes
    ax1.set_xlabel('Vertical', fontsize=12, color='black')
    ax1.set_ylabel('Ending ARR', fontsize=12, color='black')
    ax1.set_ylim(0, 30000000)  # Set y-axis limit to 30 million
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x/1e6)}M' if x >= 1e6 else f'{x/1000:.0f}K'))
    ax1.tick_params(axis='both', labelsize=10, labelcolor='black')

    ax2.set_ylabel('% MRR Growth', fontsize=12, color='black')
    ax2.set_ylim(0, 40)  # Adjusted to ensure all growth values fit
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))
    ax2.tick_params(axis='y', labelsize=10, labelcolor='black')

    # Add labels for Ending ARR with adjusted placement and font size
    max_arr = max(ending_arr)
    offset = max_arr * 0.02  # Dynamic offset based on max value
    for i, value in enumerate(ending_arr):
        if value > 0:
            label_y = min(value + offset, 29000000)  # Cap label below 29M to avoid overflow
            ax1.text(i, label_y, f'{value/1e6:.1f}M', ha='center', va='bottom', fontsize=8, color='black')

    # Add labels for % MRR Growth with adjusted placement and font size
    max_growth = max(mrr_growth)
    growth_offset = max_growth * 0.05
    for i, value in enumerate(mrr_growth):
        if value > 0:
            label_y = min(value + growth_offset, 38)  # Cap label below 38% to avoid overflow
            ax2.text(i + bar_width, label_y, f'{value:.1f}%', ha='center', va='bottom', fontsize=8, color='black')

    # Set x-axis labels to vertical names
    ax1.set_xticks(x)
    ax1.set_xticklabels(verticals, rotation=45, ha='right', color='black')

    # Add title and legend
    ax1.set_title('Ending ARR and Growth by Vertical', fontsize=14, color='black')
    # Adjust legend placement inside the main graph
    ax1.legend(loc='upper left', bbox_to_anchor=(0.02, 0.97))
    ax2.legend(loc='upper right', bbox_to_anchor=(0.97, 0.97))
    fig.subplots_adjust(top=0.85)  # Increase top padding for title and legends


    # Save the chart
    output_folder = '../charts'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'arr_and_growth_by_vertical_chart.png')
    plt.savefig(output_file, bbox_inches='tight', transparent=True, dpi=200)
    print(f"Chart saved to {output_file}")

    plt.close()  # Close the figure to free memory

if __name__ == '__main__':
    create_arr_and_growth_by_vertical_chart()