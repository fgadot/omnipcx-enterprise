import sys

'''
This script extract lines from 8770 Exports. It keeps the 2 first lines which 8770 usually need for import. 
python script_name 8770_exported_file "keyword to look for (case sensitive)"
ex: python extract_data.py keys.tsv "Voice Mail Supervision"
-> This will create a new file with just the voicemail supervision keys. 
Useful if you want to restore something specific. 
'''

def extract_data(input_file, keyword):
    # Read the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Extract the first two lines
    first_two_lines = lines[:2]

    # Filter lines containing the keyword
    filtered_lines = [line for line in lines if keyword in line]

    # Write the extracted data to a new tab-separated file
    output_file = 'new_' + input_file
    with open(output_file, 'w') as f:
        # Write the first two lines
        for line in first_two_lines:
            f.write(line)
        # Write the filtered lines
        for line in filtered_lines:
            f.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_file> <keyword>")
        sys.exit(1)

    input_file = sys.argv[1]
    keyword = sys.argv[2]

    extract_data(input_file, keyword)
