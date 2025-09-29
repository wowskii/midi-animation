import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from midiutil import MIDIFile
from PIL import Image
import os

from utilities import *

image_to_midi("images_examples/notre-dame.jpg", "midi_files/notre-dame.mid")

# split_dir = "BadApple_frames_split"
# folders = sorted([f for f in os.listdir(split_dir) if os.path.isdir(os.path.join(split_dir, f))])

# for i, folder in enumerate(folders):
#     print(f"Processing folder {i+1}/{len(folders)}: {folder}")
#     frames_folder_to_midi(
#         os.path.join(split_dir, folder),
#         f"midi_files/bad_apple{i}.mid"
#     )

# frames_folder_to_long_midi("BadApple_specific/BadApple_frames/first/", "midi_files/non_batched/first.mid")

# frames_folder_to_long_midi("BadApple_specific/BadApple_frames/second/", "midi_files/non_batched/second.mid")

# frames_folder_to_midi("BadApple_frames", "midi_files/non_batched/bad_apple_full.mid")

video_to_midi("video_examples/bad_apple_short.mp4", "midi_examples/short_bad_apple.mid")