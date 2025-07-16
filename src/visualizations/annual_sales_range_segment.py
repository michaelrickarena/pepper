import pandas as pd
import matplotlib.pyplot as plt
import os

def create_annual_sales_range_chart():
    # Load the data
    file_path = '../data/segments/segments_analysis.csv'
    df = pd.read_csv(file_path)

    # Extract relevant columns
    segments = df['Segment'].unique()
    annual_sales_ranges = ['$1bn+', '$500mm - $1bn', '$250mm - $500mm', '$100mm - $250mm', '$50mm - $100mm', '$25mm - $50mm', '$10mm - $25mm', '< $10mm']

    # Calculate percentages for each annual sales range within each segment
    percentages = pd.DataFrame(index=segments, columns=annual_sales_ranges)
    for segment in segments:
        segment_data = df[df['Segment'] == segment]
        total_rows = len(segment_data)
        for sales_range in annual_sales_ranges:
            count = len(segment_data[segment_data['Annual Sales Range'] == sales_range])
            percentages.loc[segment, sales_range] = count / total_rows if total_rows > 0 else 0

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Define colors for each annual sales range
    colors = {
        '$1bn+': "#D6AC23",
        '$500mm - $1bn': "#165e91",
        '$250mm - $500mm': "#0bac06",
        '$100mm - $250mm': "#BA55D3",
        '$50mm - $100mm': "#C0392B",
        '$25mm - $50mm': "#E67E22",
        '$10mm - $25mm': "#2980B9",
        '< $10mm': "#8E44AD"
    }

    # Plot each annual sales range as a stacked bar in reverse order (top to bottom: $1bn+ to < $10mm)
    bottom = pd.Series([0] * len(segments), index=segments)
    bar_width = 0.4
    for sales_range in reversed(annual_sales_ranges):  # Reverse order for stacking
        ax.bar(segments, percentages[sales_range], bottom=bottom, width=bar_width, color=colors.get(sales_range, 'gray'))
        bottom += percentages[sales_range]

    # Add data labels inside each stacked bar
    bottom = pd.Series([0] * len(segments), index=segments)
    for sales_range in reversed(annual_sales_ranges):  # Reverse order for labels
        for i, value in enumerate(percentages[sales_range]):
            if value >= 0.02:  # Only add labels for values 2% or higher
                ax.text(i, bottom.iloc[i] + value / 2, f'{value*100:.1f}%', ha='center', va='center', fontsize=10, color='white')
        bottom += percentages[sales_range]

    # Add labels and title
    ax.set_xlabel('Segment', fontsize=12, color='black')
    ax.set_ylabel('% of Segment within Annual Sales Range', fontsize=12, color='black')
    ax.set_title('Annual Sales Range by Segment', fontsize=14, color='black')

    # Format y-axis as percentages and set proper limits
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))  # Convert 0-1 to 0-100%
    ax.set_ylim(0, 1.10)  # Ensure y-axis goes from 0% to 100%

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', color='black')

    # Manually create legend in desired order with specified colors
    legend_patches = [plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=colors[sales_range], markersize=10, label=sales_range)
                     for sales_range in annual_sales_ranges]
    ax.legend(handles=legend_patches, title='Annual Sales Range', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the chart
    output_folder = '../charts'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'annual_sales_range_by_segment.png')
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Chart saved to {output_file}")

    plt.close()  # Close the figure to free memory

if __name__ == '__main__':
    create_annual_sales_range_chart()