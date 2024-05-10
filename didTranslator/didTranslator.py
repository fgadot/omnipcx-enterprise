"""
File: didTranslator.py  VERSION 2.0
Author: Frank Gadot <frank@hermes42.com>

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
- The DID Translator table
- The list of users
- Both files must be in TSV Format (Tabulation Separated)
- TSV Files are the result of OmniVista 8770 export.

Ex: python didTranslator.py didTable.txt userList.txt
"""

import csv
import sys


def process_did_file(filename):
    headers = ["First External Number", "First Internal Number", "Range Size", "Unique Internal Number"]
    header_indices = {header: None for header in headers}
    data = []

    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')

        # Locate headers
        for row in reader:
            for i, header in enumerate(row):
                if header in header_indices:
                    header_indices[header] = i
            if None not in header_indices.values():
                break

        # Process data
        for row in reader:
            if len(row) < max(header_indices.values()) + 1:
                continue
            data.append([sanitize_field(row[header_indices[header]]) for header in headers])

    return data


def process_users_file(filename):
    headers = ["Directory Number", "Directory name", "Directory First Name"]
    header_indices = {header: None for header in headers}
    directory = {}

    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')

        # Locate headers
        for row in reader:
            for i, header in enumerate(row):
                if header in header_indices:
                    header_indices[header] = i
            if None not in header_indices.values():
                break

        # Process data
        for row in reader:
            if len(row) < max(header_indices.values()) + 1:
                continue
            key = sanitize_field(row[header_indices["Directory Number"]])
            first_name = sanitize_field(row[header_indices["Directory First Name"]])
            last_name = sanitize_field(row[header_indices["Directory name"]])
            directory[key] = (first_name, last_name)

    return directory


def sanitize_field(field):
    """ Trims whitespace and maintains internal spaces only if there are multiple words in the field. """
    return ' '.join(field.split())


def read_and_process_files(file1_path, file2_path):
    did_data = process_did_file(file1_path)
    user_data = process_users_file(file2_path)

    print("\t".join(["DID", "Extension", "First Name", "Last Name"]))

    for external, internal, range_size, unique in did_data:
        range_size = int(range_size)
        initial_internal = internal
        for i in range(range_size):
            first_name, last_name = user_data.get(internal, ("", ""))
            # Prepare the output by ensuring no extra tabs are introduced
            output = [external, internal, first_name if first_name else "", last_name if last_name else ""]
            print("\t".join(output))
            external = str(int(external) + 1).zfill(len(external)) if i < range_size - 1 else external
            internal = str(int(initial_internal) + i + 1).zfill(
                len(initial_internal)) if unique.lower() != "yes" else initial_internal


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1_path> <file2_path>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    read_and_process_files(file1_path, file2_path)


if __name__ == "__main__":
    main()
