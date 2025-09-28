import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image

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