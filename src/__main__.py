from arr_band import process_arr_band
from verticals import process_verticals
from segments import process_segments


if __name__ == "__main__":
    print("Starting the program...")
    
    print("Starting Processing ARR Band...")
    process_arr_band()
    print("Finished Processing ARR Band...")
    
    print("Starting Processing Verticals...")
    process_verticals()
    print("Finished Processing Verticals...")

    print("Starting Processing Segments...")
    process_segments()
    print("Finished Processing Segments...")
    
    print("Program ended...")