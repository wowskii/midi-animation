import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import MIDI
from PIL import Image


# Image loading utility

def load_images(directory):
	image_list = []
	for filename in os.listdir(directory):
		if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
			img_path = os.path.join(directory, filename)
			img = Image.open(img_path)
			image_list.append(img)
	return image_list

def get_filter(image, threshold):
    M = np.array(image)
    G = np.min(M[:,:,0:3], axis=2)
    F = G < threshold
    return F

def divide_image(image, num_segments):
    width, height = image.size
    segment_height = height // num_segments
    segments = []
    for i in range(num_segments):
        box = (0, i * segment_height, width, (i + 1) * segment_height if i < num_segments - 1 else height)
        segment = image.crop(box)
        segments.append(segment)
    return segments

def reduce_filtered_image(image):
    reduced = np.zeros(image.shape[1], dtype=bool)
    true_counts = np.sum(image, axis=0)
    false_counts = image.shape[0] - true_counts
    reduced = true_counts > false_counts
    return reduced

def image_to_bool_map(image, num_segments = 48, threshold = 140):
    segments = divide_image(image, num_segments)
    bool_maps = [reduce_filtered_image(get_filter(seg, threshold)) for seg in segments]
    return bool_maps

# MIDI utilities

def create_midi_from_bool_array(bool_array, output_file):
    MIDI_file = MIDI.MIDIFile()
    for line in bool_array:
        noteline = MIDI.Track(line, False)
        MIDI_file.addTrack(noteline)
    MIDI_file.parse()