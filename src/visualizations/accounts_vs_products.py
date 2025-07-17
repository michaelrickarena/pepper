import pandas as pd
import matplotlib.pyplot as plt
import os

def create_accounts_vs_products_chart():
    # Load the data
    file_path = '../data/Segments/segments_summary.csv'
    df = pd.read_csv(file_path)

    # Reorder the segments based on the desired order
    desired_order = ['Strategic Accounts', 'Key Accounts', 'Growth Accounts', 'Standard Accounts', 'At Risk Accounts']
    df = df.set_index('Segment').loc[desired_order].reset_index()

    # Extract relevant columns after reordering
    segments = df['Segment']
    accounts = df['# Accounts']
    one_product_percentage = df['% of Customers in Segment With 1 Product']

    # Create the figure and axis
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot # of accounts on the primary axis
    bar_width = 0.4
    x = range(len(segments))
    ax1.bar(x, accounts, width=bar_width, label='# Accounts', color='#3498DB')
    ax1.set_xlabel('Segments', fontsize=12, color='black')
    ax1.set_ylabel('# Accounts', fontsize=12, color='black')
    ax1.tick_params(axis='x', labelcolor='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Add labels for # of accounts
    for i, value in enumerate(accounts):
        ax1.text(i, value + (0.05 * value), f"{value}", ha='center', color='black')

    # Create a secondary axis for % of accounts with 1 product
    ax2 = ax1.twinx()
    ax2.bar([p + bar_width for p in x], one_product_percentage, width=bar_width, label='% with 1 Product', color='#FF5733')
    ax2.set_ylabel('% with 1 Product', fontsize=12, color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Format y-axis for percentages
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))

    # Add labels for % of accounts with 1 product
    for i, value in enumerate(one_product_percentage):
        ax2.text(i + bar_width, value + (0.05 * value), f"{value*100:.1f}%", ha='center', color='black')

    # Set x-axis labels to segment names
    ax1.set_xticks([p + bar_width / 2 for p in x])
    ax1.set_xticklabels(segments, rotation=45, ha='right')

    # Set y-axis limits
    ax1.set_ylim(0, 400)  # Max for # Accounts
    ax2.set_ylim(0, 1)  # Max for % of Accounts with 1 Product

    # Add title and legend
    ax1.set_title('Segment Analysis: Total Accounts and Percentage with One Product', fontsize=14, color='black')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    fig.tight_layout()

    # Save the chart
    output_folder = '../charts'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, 'accounts_vs_products_chart.png')
    plt.savefig(output_file, bbox_inches='tight', transparent=True)
    print(f"Chart saved to {output_file}")

    plt.close()  # Close the figure to free memory

if __name__ == '__main__':
    create_accounts_vs_products_chart()