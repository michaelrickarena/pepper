import pandas as pd
import matplotlib.pyplot as plt
import os

def create_arr_band_positioning_chart():
    # Load the data
    file_path = '../data/ARR Band/arr_band_summary.csv'
    df = pd.read_csv(file_path)

    # Skip the first row if it's a placeholder (e.g., [0, 0, 0, 0, 1])
    if df.iloc[0].tolist() == [0, 0, 0, 0, 1]:
        df = df.iloc[1:].reset_index(drop=True)

    # Extract relevant columns
    groups = df['Group']
    segments = ['Strategic Accounts', 'Key Accounts', 'Growth Accounts', 'Standard Accounts', 'At Risk Accounts']

    # Reorder the bars to match the desired order
    desired_order = ['Strategic Accounts', 'Key Accounts', 'Growth Accounts', 'Standard Accounts', 'At Risk Accounts']
    df = df[['Group'] + desired_order]  # Reorder columns in the DataFrame

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

    # Plot each segment as a stacked bar in reverse order
    bottom = pd.Series([0] * len(groups))
    handles = []
    labels = []
    for segment in reversed(segments):  # Reverse for plotting (Strategic at bottom)
        bar = ax.bar(groups, df[segment], bottom=bottom, width=0.4, label=segment, color=colors.get(segment, 'gray'))
        bottom = bottom + df[segment]  # Update bottom for next segment
        handles.append(bar[0])  # Store handle for legend
        labels.append(segment)   # Store label for legend

    # Add data labels inside each stacked bar
    bottom = pd.Series([0] * len(groups))
    for segment in reversed(segments):  # Use same reverse order for labels
        for i, value in enumerate(df[segment]):
            if value > 0:  # Only add labels for non-zero values
                percentage = int((value / df[segments].sum(axis=1).iloc[i]) * 100)
                ax.text(i, bottom[i] + value / 2, f'{int(value)} ({percentage}%)', ha='center', va='center', fontsize=10, color='white')
        bottom += df[segment]

    # Add labels and title
    ax.set_xlabel('ARR Band Range', fontsize=12, color='black')
    ax.set_ylabel('Number of Accounts by Segment', fontsize=12, color='black')
    ax.set_title('ARR Band Positioning by Segment', fontsize=14, color='black')

    # Format y-axis ticks as absolute values
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', color='black')

    # Add legend with original segment order
    ax.legend(handles=handles[::-1], labels=labels[::-1], title='Segments', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the chart
    output_folder = '../charts'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'arr_band_positioning_by_segment.png')
    plt.savefig(output_file, bbox_inches='tight', transparent=True)
    print(f"Chart saved to {output_file}")

    plt.close()  # Close the figure to free memory

if __name__ == '__main__':
    create_arr_band_positioning_chart()