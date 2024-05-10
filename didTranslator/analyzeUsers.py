"""
Made for www.AlcatelUnleashed.com
Test script to analyze USERS extract
Will simply read it and dump Extension, Last name, First name  on the screen
"""

import csv

def process_users_file(filename):
    # Specify the headers of interest
    headers_of_interest = ["Directory Number", "Directory name", "Directory First Name"]
    indices = {header: None for header in headers_of_interest}
    data_of_interest = []

    with open(filename, 'r', newline='') as file:
        # Read the file as a tab-delimited file
        reader = csv.reader(file, delimiter='\t')

        # Search for headers until found
        for row in reader:
            row = [cell.strip() for cell in row]  # Clean whitespace around each cell
            for i, header in enumerate(row):
                if header in indices:
                    indices[header] = i
            # Break loop if all headers are found
            if all(value is not None for value in indices.values()):
                break

        # Check if any header was not found
        if None in indices.values():
            print("Error: Not all headers were found in the file.")
            return []

        # Read the remaining data lines and extract relevant data
        for row in reader:
            if len(row) < max(indices.values()) + 1:  # Ensure row has enough columns
                continue
            filtered_row = [row[indices[header]] for header in headers_of_interest if indices[header] is not None]
            data_of_interest.append(filtered_row)

    return data_of_interest


# Replace 'users.txt' with the path to your actual file
processed_data = process_users_file('users.txt')
for row in processed_data:
    print(row)

