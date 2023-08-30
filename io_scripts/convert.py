"""
Convert _combined detection files to AVA format.
"""

import glob
import os
import get_segs

def find_csv_files(directory,hint):
    pattern = os.path.join(directory,hint)
    csv_file_dirs = glob.glob(pattern)
    csv_files = [os.path.basename(file_name) for file_name in csv_file_dirs]
    return csv_files, csv_file_dirs

data_dir = '//Singingmouse/data/usv_calls/usv_note_analysis/03_div_cage_group01_16-23/'
usv_detections_filepath = data_dir + '/combined detection files'

csv_files, csv_dirs = find_csv_files(usv_detections_filepath,"*combine.csv")

mask_usv_by_song = True

for filename, filedir in zip(csv_files,csv_dirs):
    
    l_segs_filepath = data_dir + 'segs/' + 'l_' + filename[:25] + '.txt'
    r_segs_filepath = data_dir + 'segs/' + 'r_' + filename[:25] + '.txt'

    get_segs.make_segs_from_usvseg_divcage(filedir, l_segs_filepath, r_segs_filepath, mask_usv_by_song)