from arr_band import process_arr_band
from verticals import process_verticals
from segments import process_segments
from utils.utils import add_country_and_state
from time import sleep

if __name__ == "__main__":
    print("Starting the program...")
    print("Updating Country, State, and City columns.")
    add_country_and_state()
    print("Country, State, and City columns updated.")
    print("Starting Processing Verticals...")
    process_verticals()
    print("Finished Processing Verticals...")
    print("Starting Processing Segments...")
    process_segments()
    print("Finished Processing Segments...")
    sleep(2) # sleep for x seconds to ensure segments are processed before ARR Band
    print("Starting Processing ARR Band...")
    process_arr_band()
    print("Finished Processing ARR Band...")
    print("Program ended...")