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