# RaDSH is a Rapid Designer for Static HTML.
# Visit the official repositiory at https://github.com/radialapps/radsh
#
# Copyright 2017 (C) RadialApps <radialapps@gmail.com>
#

import pandas as pd
import re
import sys
import os

# Check arguments
if len(sys.argv) != 4:
    print("Wrong number of arguments!\nUsage: python radsh.py <data-csv> <template> <extension>")
    quit()

for i in range(1,3):
    if not os.path.isfile(sys.argv[i]):
        print("File not found --", sys.argv[i])
        quit()

# Read our data into a pandas dataframe
print('Reading data')
df = pd.read_csv(sys.argv[1])

# Read the template file
print('Reading template')
with open(sys.argv[2]) as f:
    template = f.read()

# Just to be safe
rowno = 0

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
        if not col in df.columns:
            continue
        
        if df[col][rowno] == 1:
            # Answer if true
            if len(re.findall(regexdollar, com)) > 0:
                print(col, ' == true -- ', re.findall(regexdollar, com)[0])
                return re.findall(regexdollar, com)[0]

        elif df[col][rowno] == 0:
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
    if col in df.columns:
        # If a file is to be substituted
        # Throws an error if the file is not found
        if 'file=' in df[col][rowno]:
            print ('Inserting file', df[col][rowno][5:])
            with open(df[col][rowno][5:]) as fl:
                temp = fl.read()

            # Recursively process the file
            return re.sub(regexcurl,compile, re.sub(regexsquare, preprocess, temp))
        
        # Return the value of the requested cell
        print (col, ' -- ', df[col][rowno])
        
        # Look for http links and replace special characters
        # TODO: If necessary, replace special characters everywhere
        if df[col][rowno][:4] == 'http':
            print('Detected http link')
            return replace_special(df[col][rowno])
        
        return df[col][rowno]
    else:
        # No such column
        return match
    
# Regex to be used
regexsquare = r"\[(.*?)\]"
regexcurl = r"{{([^}]+)}}"
regexcaret = r"\^\^([^}]+)\^\^"
regexdollar = r"\$\$(.*?)\$\$"
regexnotdollar = r"\$!(.*?)!\$"

# Main loop
for index,row in df.iterrows():
    # Update index for other functions
    rowno = index
    
    if str(row['filename']) == 'nan':
        continue;
        
    # Get the file to save to
    filename = row['filename'] + '.' + sys.argv[3]
    print(' ------------ Now working on ', filename, '------------')
    
    # Start working
    final = re.sub(regexcurl, compile, re.sub(regexsquare, preprocess, template))
    
    # Write out everything when done
    with open(filename, 'w') as f:
        f.write(final)

print('Everything done')