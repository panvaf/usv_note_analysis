"""
Preprocessing viewer for USVs.
"""

import numpy as np
import os
import matplotlib.pyplot as plt

from ava.models.vae import X_SHAPE
from ava.preprocessing.utils import get_spec
from ava.preprocessing.preprocess import get_audio_seg_filenames, read_onsets_offsets_from_file, get_syll_specs

# ava object path

root = '//SingingMouse/data/usv_calls/usv_note_analysis/03_16_01_test'
audio_dirs = [os.path.join(root, 'audio')]
seg_dirs = [os.path.join(root, 'segs')]


# preprocess params
preprocess_params = {
    'get_spec': get_spec,
    'max_dur': 0.25, # maximum syllable duration
    'min_freq': 15e3, # minimum frequency
    'max_freq': 100e3, # maximum frequency
    'num_freq_bins': X_SHAPE[0], # hard-coded
    'num_time_bins': X_SHAPE[1], # hard-coded
    'nperseg': 1024, # FFT
    'noverlap': 512, # FFT
    'spec_min_val': 2.0, # minimum log-spectrogram value
    'spec_max_val': 5.4, # maximum log-spectrogram value
    'fs': 250000, # audio samplerate
    'mel': False, # frequency spacing, mel or linear
    'time_stretch': True, # stretch short syllables?
    'within_syll_normalize': False, # normalize spectrogram values on a
                                    # spectrogram-by-spectrogram basis
    'max_num_syllables': None, # maximum number of syllables per directory
    'sylls_per_file': 20, # syllable per file
    'real_preprocess_params': ('min_freq', 'max_freq', 'spec_min_val', \
            'spec_max_val', 'max_dur'), # tunable parameters
    'int_preprocess_params': ('nperseg','noverlap'), # tunable parameters
    'binary_preprocess_params': ('time_stretch', 'mel', \
            'within_syll_normalize'), # tunable parameters
}

# tune params

# FROM: tune_syll_preprocessing_params in preprocess.py
# Collect all the relevant filenames.
audio_filenames, seg_filenames = [], []
for audio_dir, seg_dir in zip(audio_dirs, seg_dirs):
    temp_audio, temp_seg = get_audio_seg_filenames(audio_dir, seg_dir, preprocess_params)
    audio_filenames += temp_audio
    seg_filenames += temp_seg
audio_filenames = np.array(audio_filenames)
seg_filenames = np.array(seg_filenames)
assert len(audio_filenames) > 0, "Didn't find any audio files!"

n_rows=6
n_cols=6

for file_index in range(len(audio_filenames)):
    # pick a file
    audio_filename = audio_filenames[file_index]
    seg_filename = seg_filenames[file_index]
    print(audio_filename)
    print(seg_filename)
    # load segmentations
    onsets, offsets = read_onsets_offsets_from_file(seg_filename, preprocess_params)
    print(len(onsets))
    # Grab some random syllable from within the file.
    np.random.seed(42)
    syll_index = np.random.randint(len(onsets), size=n_rows*n_cols)
    example_onsets, example_offsets = onsets[syll_index], offsets[syll_index]
    # Get the preprocessed spectrogram.
    specs, good_sylls = get_syll_specs(example_onsets, example_offsets, audio_filename, preprocess_params)
    specs = [specs[i] for i in good_sylls]
    
    # plot
    fig, axes = plt.subplots(figsize=(10,10), nrows=n_rows, ncols=n_cols)
    for j in range(n_rows):
        for k in range(n_cols):
            i_note = j*n_cols+k
            if i_note < len(specs):
                spec = specs[i_note]
                axes[j,k].imshow(spec, aspect='equal', origin='lower', vmin=0, vmax=1)
            axes[j,k].axis('off')
            
    plt.show()