"""
    io.py
    io util functions for usv note analysis

"""

import numpy as np
import pandas as pd

import audio_utils.io

def make_segs_from_usvseg_homecage(usv_detections_filepath, segs_filepath, mask_usv_by_song, margin=0.015):
    """ load homecage (1 source) usvseg detections, export to ava segs format
    https://github.com/singingmicelab/autoencoded-vocal-analysis/blob/master/ava/segmenting/segment.py
    
    """
    
    # load usv
    usv_detections = audio_utils.io.read_usv_detections(usv_detections_filepath)
    # mask usv detections by song detections
    if mask_usv_by_song:
        usv_detections = usv_detections[usv_detections['in_song'] == False]

    print(f'writing segs file to: {segs_filepath}')

    # write the usv detections to seg folder with new format
    segs = usv_detections[['start', 'end']].copy()
    segs['start'] = segs['start'] - margin
    segs['end'] = segs['end'] + margin

    header=f'usv_detections_filepath: {usv_detections_filepath}\nmask_usv_by_song: {mask_usv_by_song}'
    np.savetxt(segs_filepath, segs.values, fmt='%.5f', header=header)


def make_segs_from_usvseg_divcage(usv_detections_filepath, l_segs_filepath, r_segs_filepath, mask_usv_by_song, l_code=[0,2,4], r_code=[1,3,5], margin=0.015):
    """ load divcage (2 source) usvseg detections by code, export to ava segs format
    https://github.com/singingmicelab/autoencoded-vocal-analysis/blob/master/ava/segmenting/segment.py
    
    """
    
    # load usv
    usv_detections = audio_utils.io.read_usv_detections(usv_detections_filepath, dropna=False)
    # mask usv detections by song detections
    if mask_usv_by_song:
        usv_detections = usv_detections[usv_detections['in_song'] == False]

    # write the usv detections to seg folder with new format
    l_usv_detections = usv_detections[usv_detections['code'].isin(l_code)]
    r_usv_detections = usv_detections[usv_detections['code'].isin(r_code)]

    l_segs = l_usv_detections[['start', 'end']].copy()
    l_segs['start'] = l_segs['start'] - margin
    l_segs['end'] = l_segs['end'] + margin

    r_segs = r_usv_detections[['start', 'end']].copy()
    r_segs['start'] = r_segs['start'] - margin
    r_segs['end'] = r_segs['end'] + margin

    print(f'left - writing segs file to: {l_segs_filepath}')
    print(f'right - writing segs file to: {r_segs_filepath}')

    l_header=f'usv_detections_filepath: {usv_detections_filepath}\nmask_usv_by_song: {mask_usv_by_song}\ncode: {l_code}'
    r_header=f'usv_detections_filepath: {usv_detections_filepath}\nmask_usv_by_song: {mask_usv_by_song}\ncode: {r_code}'
    
    np.savetxt(l_segs_filepath, l_segs.values, fmt='%.5f', header=l_header)
    np.savetxt(r_segs_filepath, r_segs.values, fmt='%.5f', header=r_header)


def copy_usvseg_homecage(usv_detections_filepath, usvseg_filepath, mask_usv_by_song):
    """ copy usvseg file to ava folder

    """    
    # load usv
    usv_detections = audio_utils.io.read_usv_detections(usv_detections_filepath)
    # mask usv detections by song detections
    if mask_usv_by_song:
        usv_detections = usv_detections[usv_detections['in_song'] == False]

    usv_detections.to_csv(usvseg_filepath)