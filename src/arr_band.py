import pandas as pd

def process_arr_band():
    df = pd.read_csv('../Account Segmentation & Revenue Team Structuring Exercise - Data.csv')

    df['Ending ARR'] = df['Ending ARR'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)

    # Map ARR Band ranges to numerical ranges
    arr_band_ranges = {
        '< $10k': (0, 10000),
        '$10k - $25k': (10000, 25000),
        '$25k - $50k': (25000, 50000),
        '$50k - $75k': (50000, 75000),
        '$50 - $75k': (50000, 75000),
        '$75k - $100k': (75000, 100000),
        '$100k - $250k': (100000, 250000),
        '$250k+': (250000, float('inf'))
    }

    # Apply the mapping to the ARR Band column
    df['ARR Band Range'] = df['ARR Band'].map(arr_band_ranges)
    # Filter rows where Ending ARR is lower than the lower bound of the ARR Band Range
    df['Lower Bound'] = df['ARR Band Range'].apply(lambda x: x[0] if pd.notna(x) else None)
    df['Upper Bound'] = df['ARR Band Range'].apply(lambda x: x[1] if pd.notna(x) else None)
    df['Middle'] = df.apply(lambda row: (row['Lower Bound'] + row['Upper Bound']) / 2 if pd.notna(row['Lower Bound']) and pd.notna(row['Upper Bound']) else None, axis=1)

    # Filter customers based on Ending ARR
    below_lower = df[df['Ending ARR'] < df['Lower Bound']]
    middle_to_lower = df[(df['Ending ARR'] >= df['Lower Bound']) & (df['Ending ARR'] < df['Middle'])]
    middle_to_upper = df[(df['Ending ARR'] >= df['Middle']) & (df['Ending ARR'] <= df['Upper Bound'])]
    above_upper = df[df['Ending ARR'] > df['Upper Bound']]

    # Print results
    print("Below Lower Bound:")
    print(len(below_lower))
    print(below_lower[['ARR Band', 'ARR Band Range', 'Ending ARR']])

    print("\nMiddle to Lower Bound:")
    print(len(middle_to_lower))
    print(middle_to_lower[['ARR Band', 'ARR Band Range', 'Ending ARR']])

    print("\nMiddle to Upper Bound:")
    print(len(middle_to_upper))
    print(middle_to_upper[['ARR Band', 'ARR Band Range', 'Ending ARR']])

    print("\nAbove Upper Bound:")
    print(len(above_upper))
    print(above_upper[['ARR Band', 'ARR Band Range', 'Ending ARR']])


# How far Ending ARR is from the ARR band range