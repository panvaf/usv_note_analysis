"""
Convert song files to AVA format
"""

import pandas as pd

data_dir = '//Singingmouse/data/usv_calls/usv_note_analysis/03_div_cage_group01_18_song/song detection files/'
# Replace 'input_file.csv' with the path to your CSV file
input_filename = 'T221208125757_0000111_030'
# Replace 'output_file.txt' with the path where you want to save the text file
output_filename = 's_' + input_filename + '.txt'

# List the two columns you want to extract (replace 'column1' and 'column2' with the actual column names)
column1_name = 'start'
column2_name = 'end'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(data_dir+input_filename+'.csv')

# Extract the two columns from the DataFrame and save them to a text file
df[[column1_name, column2_name]].round(5).to_csv(data_dir+output_filename, sep=' ', index=False, header=False)

print("Extraction and writing to the text file completed.")