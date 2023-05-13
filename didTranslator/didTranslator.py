"""
File: didTranslator.
Author: Frank Gadot <frank@hermes42.com.com>

Copyright © 2023 Frank Gadot. All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

DESCRIPTION:
This script was made in order to help OmniPCX Enterprise administrator to have a visualization of what external DID goes to what user.
It takes a DID Translation spead-sheet like in first argument, and a user list in 2nd argument. The result of this file are displayed
on the console put the output can be redirected toward a TSV (Tabulation Separated) file.

Description:
This script reads the data from 2 files passed in argument:
- The DID Translator table, with 4 columns only (external number, internal number, range, unique)
- The list of users, with 3 columns only (extension, lase name, first name)
- Both files must be in TSV Format (Tabulation Separated) and have headers in the files (headers can be named anything)
- TSV Files are the result of OmniVista 8770 export. You'll just need to clean up the files and remove any unwanted column.
"""

import csv
import sys

def read_and_process_files(file1_path, file2_path):
    # Create a dictionary to store data from the second file
    extension_dict = {}
    with open(file2_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip the header row

        for row in reader:
            extension = row[0]
            last_name = row[1]
            first_name = row[2]
            extension_dict[extension] = (last_name, first_name)

    # Process the first file
    with open(file1_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip the header row

        # Print the header row for the output
        print("\t".join(["External", "Internal", "Range", "Unique", "Last Name", "First Name"]))

        for row in reader:
            external = row[0]
            internal = row[1]
            range_val = int(row[2])
            unique = row[3]

            while range_val >= 1:
                # Get the matching last name and first name from the second file
                last_name, first_name = extension_dict.get(internal, ("", ""))
                print("\t".join([external, internal, str(range_val), unique, last_name, first_name]))
                if range_val > 1:
                    external = str(int(external) + 1).zfill(len(external))
                if unique.lower() != "yes":
                    internal = str(int(internal) + 1).zfill(len(internal))
                range_val -= 1

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1.txt> <file2.txt>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    read_and_process_files(file1_path, file2_path)

if __name__ == "__main__":
    main()
