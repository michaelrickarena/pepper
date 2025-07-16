from arr_band import process_arr_band
from verticals import process_verticals
from segments import process_segments
from utils.utils import add_country_and_state, create_new_columns
from time import sleep
from visualizations.segment_count_revenue import create_segment_distribution_chart
from visualizations.MRR_ARR_Scatter import create_mrr_growth_vs_arr_scatter
from visualizations.segment_vertical import create_segment_mix_by_vertical_chart
from visualizations.arr_band_segment import create_arr_band_positioning_chart
from visualizations.accounts_vs_products import create_accounts_vs_products_chart
from visualizations.annual_sales_range_segment import create_annual_sales_range_chart
from visualizations.arr_mrr_vertical import create_arr_and_growth_by_vertical_chart


if __name__ == "__main__":

    # print("Starting the program...")

    # print("Creating new columns in the data...")
    # create_new_columns()
    # print("New columns created in the data.")

    # print("Updating Country, State, and City columns.")
    # add_country_and_state()
    # print("Country, State, and City columns updated.")

    # print("Starting Processing Verticals...")
    # process_verticals()
    # print("Finished Processing Verticals...")

    # print("Starting Processing Segments...")
    # process_segments()
    # print("Finished Processing Segments...")
    # sleep(2) # sleep for x seconds to ensure segments are processed before ARR Band

    # print("Starting Processing ARR Band...")
    # process_arr_band()
    # print("Finished Processing ARR Band...")

    # ### Build visualizations
    print("Starting to create visualizations...")
    create_segment_distribution_chart()
    create_mrr_growth_vs_arr_scatter()
    create_segment_mix_by_vertical_chart()
    create_arr_band_positioning_chart()
    create_accounts_vs_products_chart()
    create_annual_sales_range_chart()
    create_arr_and_growth_by_vertical_chart()
    print("Visualizations created successfully.")

    print("Program ended...")