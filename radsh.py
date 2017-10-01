# RaDSH is a Rapid Designer for Static HTML.
# Visit the official repositiory at https://github.com/radialapps/radsh
#
# Copyright 2017 (C) RadialApps <radialapps@gmail.com>
#

import re
import sys
import os
import csv

# Regex to be used
regexsquare = r"\[(.*?)\]"
regexcurl = r"{{([^}]+)}}"
regexcaret = r"\^\^([^}]+)\^\^"
regexdollar = r"\$\$(.*?)\$\$"
regexnotdollar = r"\$!(.*?)!\$"

current_row = {}

# Check arguments
if len(sys.argv) != 4:
    print("Wrong number of arguments!\nUsage: python radsh.py <data-csv> <template> <extension>")
    quit()

for i in range(1,3):
    if not os.path.isfile(sys.argv[i]):
        print("File not found --", sys.argv[i])
        quit()

# Read the data
print('Reading data')
with open(sys.argv[1], 'r') as csvfile:
    data_rows = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
    data_columns = data_rows[0]
    del data_rows[0]

# Read the template file
print('Reading template')
with open(sys.argv[2]) as template_file:
    template = template_file.read()

# Replace any unsafe characters for http links
# TODO: expand this to replace other special characters
def replace_special(input):
    return input.replace('&', '&amp;')

# Preprocessing
def preprocess(match):
    match = match.group()

    # Get the string to be processed
    com = match.strip("[]")
    if com[:1]!="#":
        return match

    # Look for conditions
    for col in re.findall(regexcaret, com):
        # Check if such a column exists
        if not col in data_columns:
            continue

        if current_row[col] == "1":
            # Answer if true
            if len(re.findall(regexdollar, com)) > 0:
                print(col, ' == true -- ', re.findall(regexdollar, com)[0])
                return re.findall(regexdollar, com)[0]

        elif current_row[col] == "0":
            # Answer if false
            if len(re.findall(regexnotdollar, com)) > 0:
                print(col, ' == false -- ', re.findall(regexnotdollar, com)[0])
                return re.findall(regexnotdollar, com)[0]

    print(com, " -- no match")
    return ""

# Actual compilation
def compile(match):
    match = match.group()

    # Get the string to be processed
    col = match.strip("{}")

    # Look for things to do
    if col in data_columns:
        # If a file is to be substituted
        # Throws an error if the file is not found
        if 'file=' in current_row[col]:
            print ('Inserting file', current_row[col][5:])
            with open(current_row[col][5:]) as fl:
                temp = fl.read()

            # Recursively process the file
            return re.sub(regexcurl,compile, re.sub(regexsquare, preprocess, temp))

        # Return the value of the requested cell
        print (col, ' -- ', current_row[col])

        # Look for http links and replace special characters
        # TODO: If necessary, replace special characters everywhere
        if current_row[col][:4] == 'http':
            print('Detected http link')
            return replace_special(current_row[col])

        return current_row[col]
    else:
        # No such column
        return match

# Main loop
for index, raw_row in enumerate(data_rows):

    # Get the current row
    for i, col in enumerate(data_columns):
        current_row[col] = raw_row[i]

    # Check if something is bad
    if str(current_row['filename']) == 'nan':
        continue;

    # Get the file to save to
    filename = current_row['filename'] + '.' + sys.argv[3]
    print(' ------------ Now working on ', filename, '------------')

    # Start working
    final = re.sub(regexcurl, compile, re.sub(regexsquare, preprocess, template))

    # Write out everything when done
    with open(filename, 'w') as output_file:
        output_file.write(final)

print('Everything done')