import pandas as pd
import matplotlib.pyplot as plt
import os

def create_segment_mix_by_vertical_chart():
    # Load the data
    file_path = '../data/Segments/segments_verticals_summary.csv'
    df = pd.read_csv(file_path)

    # Extract relevant columns
    verticals = df['Vertical']
    segments = df.columns[1:]  # All columns except 'Vertical'

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Define colors for each segment
    colors = {
        'Strategic Accounts': "#D6AC23",
        'Key Accounts': "#165e91",
        'Growth Accounts': "#0bac06",
        'Standard Accounts': "#CE0EBE",
        'At Risk Accounts': "#d30d0d"
    }

    # Plot each segment as a stacked bar
    bottom = pd.Series([0] * len(verticals))
    for segment in segments:
        ax.bar(verticals, df[segment], bottom=bottom, label=segment, color=colors.get(segment, 'gray'))
        bottom += df[segment]

    # Add data labels inside each stacked bar
    bottom = pd.Series([0] * len(verticals))
    for segment in segments:
        for i, value in enumerate(df[segment]):
            if value > 0:  # Only add labels for non-zero values
                ax.text(i, bottom[i] + value / 2, f'{value*100:.1f}%', ha='center', va='center', fontsize=12, color='white')
        bottom += df[segment]

    # Add labels and title
    ax.set_xlabel('Verticals', fontsize=12)
    ax.set_ylabel('Segments as Percentage of Vertical', fontsize=12)
    ax.set_title('Segment Mix by Vertical', fontsize=14)
    ax.set_ylim(0, 1.10)

    # Format y-axis as percentages
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Format the legend with desired order and custom colors
    desired_order = ['Strategic Accounts', 'Key Accounts', 'Growth Accounts', 'Standard Accounts', 'At Risk Accounts']
    handles = [
        plt.Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor=colors[segment], markersize=10) 
        for segment in desired_order
    ]
    ax.legend(handles, desired_order, title='Segments', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the chart
    output_folder = '../charts'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'segment_mix_by_vertical.png')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Chart saved to {output_file}")

    plt.close()  # Close the figure to free memory

if __name__ == '__main__':
    create_segment_mix_by_vertical_chart()