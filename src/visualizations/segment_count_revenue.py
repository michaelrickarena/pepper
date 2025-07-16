import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

def create_segment_distribution_chart():
    # Load the data
    file_path = '../data/Segments/segments_summary.csv'
    df = pd.read_csv(file_path)

    # Sort the data by Total Ending ARR
    df = df.sort_values(by='Total Ending ARR', ascending=False)

    # Extract relevant columns
    segments = df['Segment']
    account_counts = df['# Accounts']
    total_ending_arr = df['Total Ending ARR']

    # Create the figure and axis
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot Total Ending ARR on the primary axis
    bar_width = 0.4
    x = range(len(segments))
    ax1.bar([p + bar_width for p in x], total_ending_arr, width=bar_width, label='Total Ending ARR', color='#FF5733')
    ax1.set_xlabel('Segments', color='black')
    ax1.set_ylabel('Total Ending ARR', color='black')
    ax1.tick_params(axis='x', labelcolor='black')
    ax1.tick_params(axis='y', labelcolor='black')  # Override orange

    # Add labels for Total Ending ARR
    for i, value in enumerate(total_ending_arr):
        ax1.text(i + bar_width, value + (0.05 * value), f"{value/1e6:.1f}M", ha='center', color='black')

    # Create a secondary axis for # Accounts
    ax2 = ax1.twinx()
    ax2.bar(x, account_counts, width=bar_width, label='# Accounts', color='#3498DB')
    ax2.set_ylabel('# Accounts', color='black')
    ax2.tick_params(axis='y', labelcolor='black')  # Override skyblue

    # Add labels for # Accounts
    for i, value in enumerate(account_counts):
        ax2.text(i, value + (0.05 * value), f"{value}", ha='center', color='black')

    # Set limits for the primary axis (Total Ending ARR)
    ax1.set_ylim(0, total_ending_arr.max() * 1.2)

    # Set limits for the secondary axis (# Accounts)
    ax2.set_ylim(0, account_counts.max() * 1.4)

    # Set x-axis labels to segment names
    ax1.set_xticks([p + bar_width / 2 for p in x])
    ax1.set_xticklabels(segments, rotation=45, ha='right', color='black')

    # Format y-axis labels (Total Ending ARR) in millions
    
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1e6)}M'))

    # Add title and legend
    ax1.set_title('Segment Distribution by Count and Ending ARR')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    fig.tight_layout()

    # Save the chart
    output_folder = '../charts'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'segment_distribution_chart.png')
    plt.savefig(output_file)
    print(f"Chart saved to {output_file}")

    plt.close()  # Close the figure to free memory

if __name__ == '__main__':
    create_segment_distribution_chart()