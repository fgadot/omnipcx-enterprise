"""
Made for www.AlcatelUnleashed.com
Test script to analyze DID Tranlator extract
Will simply read it and dump the data on the screen
"""

import csv
def process_did_file(filename):
    # Specify the headers of interest, accounting for possible variations
    headers_of_interest = {
        "First External Number": None,
        "First Internal Number": None,
        "Range Size": None,
        "Unique Internal Number": None
    }
    data_of_interest = []

    with open(filename, 'r', newline='') as file:
        # Read the file as a tab-delimited file
        reader = csv.reader(file, delimiter='\t')

        # Search for headers until found
        for row in reader:
            for i, header in enumerate(row):
                clean_header = header.strip()
                if clean_header in headers_of_interest:
                    headers_of_interest[clean_header] = i
            # Break loop if all headers are found
            if all(value is not None for value in headers_of_interest.values()):
                break

        # Check if any header was not found
        if None in headers_of_interest.values():
            print("Error: Not all headers were found in the file.")
            return []

        # Read the remaining data lines
        for row in reader:
            if len(row) < max(headers_of_interest.values()) + 1:  # Ensure row has enough columns
                continue
            filtered_row = [row[headers_of_interest[header]] for header in headers_of_interest if
                            headers_of_interest[header] is not None]
            data_of_interest.append(filtered_row)

    return data_of_interest


# Replace 'yourfile.tsv' with the path to your actual file
processed_data = process_did_file('dids.txt')
for row in processed_data:
    print(row)
