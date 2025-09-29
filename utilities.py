import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from midiutil import MIDIFile
from PIL import Image
import cv2


HORIZONTAL_RESOLUTION = 0

# ---------------- Image Utilities ----------------

def load_images_from_folder(folder_path):
    """
    Loads all images from a folder into a list of PIL Image objects.

    Args:
        folder_path (str): Path to the folder containing images.

    Returns:
        list[PIL.Image.Image]: List of loaded images.
    """
    image_list = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            image_list.append(img)
    return image_list

def load_image(image_path):
    """
    Loads a single image from a file path.

    Args:
        image_path (str): Path to the image file.

    Returns:
        PIL.Image.Image: Loaded image.
    """
    return Image.open(image_path)

def get_image_filter(image, threshold):
    """
    Applies a threshold filter to an image, returning a boolean mask.

    Args:
        image (PIL.Image.Image): Input image.
        threshold (int): Threshold value (0-255).

    Returns:
        np.ndarray: 2D boolean array where True indicates pixel < threshold.
    """
    M = np.array(image)
    G = np.min(M[:,:,0:3], axis=2)
    F = G < threshold
    return F

def divide_image_vertically(image, num_segments):
    """
    Divides an image into vertical segments.

    Args:
        image (PIL.Image.Image): Input image.
        num_segments (int): Number of vertical segments.

    Returns:
        list[PIL.Image.Image]: List of cropped image segments.
    """
    width, height = image.size
    segment_height = height // num_segments
    segments = []
    for i in range(num_segments):
        box = (0, i * segment_height, width, (i + 1) * segment_height if i < num_segments - 1 else height)
        segment = image.crop(box)
        segments.append(segment)
    return segments

def reduce_bool_image_columns(bool_image):
    """
    Reduces a 2D boolean image to a 1D boolean array by majority vote per column.

    Args:
        bool_image (np.ndarray): 2D boolean array.

    Returns:
        np.ndarray: 1D boolean array, True if more True than False in column.
    """
    true_counts = np.sum(bool_image, axis=0)
    false_counts = bool_image.shape[0] - true_counts
    reduced = true_counts > false_counts
    return reduced

def image_to_bool_array(image, num_segments=48, threshold=140):
    """
    Converts an image to a list of boolean arrays representing vertical segments.

    Args:
        image (PIL.Image.Image or str): Input image or path.
        num_segments (int): Number of vertical segments.
        threshold (int): Threshold for filtering.

    Returns:
        list[np.ndarray]: List of 1D boolean arrays for each segment.
    """
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    segments = divide_image_vertically(image, num_segments)
    bool_maps = [reduce_bool_image_columns(get_image_filter(seg, threshold)) for seg in segments]
    return bool_maps

# ---------------- MIDI Utilities ----------------

def add_bool_array_to_midi(mf, bool_array, track=0, channel=0, time_offset=0, volume=100):
    """
    Adds notes from a 2D boolean array to a MIDIFile object.

    Args:
        mf (MIDIFile): The MIDIFile object to add notes to.
        bool_array (list[np.ndarray]): 2D boolean array (segments x time).
        track (int): MIDI track number.
        channel (int): MIDI channel.
        time_offset (int): Time offset for note placement.
        volume (int): Note volume.
    """
    for i, line in enumerate(bool_array):
        in_note = False
        note_begin = None
        pitch = 60 + (len(bool_array) - i)
        for j, val in enumerate(line):
            abs_j = j + time_offset
            if val and not in_note:
                in_note = True
                note_begin = abs_j
            elif in_note and not val:
                length = abs_j - note_begin
                if length > 0:
                    mf.addNote(track, channel, pitch, note_begin, length, volume)
                in_note = False
        if in_note and note_begin is not None:
            length = time_offset + len(line) - note_begin
            if length > 0:
                mf.addNote(track, channel, pitch, note_begin, length, volume)

def midi_from_bool_array(bool_array, output_file, channel=0):
    """
    Creates a MIDI file from a 2D boolean array.

    Args:
        bool_array (list[np.ndarray]): 2D boolean array (segments x time).
        output_file (str): Output MIDI file path.
        channel (int): MIDI channel.
    """
    mf = MIDIFile(1)
    track = 0
    time = 0  # Start at the beginning
    mf.addTrackName(track, time, "Image Track")
    mf.addTempo(track, time, 120)
    volume = 100

    add_bool_array_to_midi(mf, bool_array, track, channel, time, volume)

    with open(output_file, 'wb') as outf:
        mf.writeFile(outf)

def midi_from_bool_arrays(list_of_bool_arrays, output_file):
    """
    Creates a multi-track MIDI file from a list of 2D boolean arrays (one per frame).

    Args:
        list_of_bool_arrays (list[list[np.ndarray]]): List of 2D boolean arrays.
        output_file (str): Output MIDI file path.
    """
    mf = MIDIFile(6600)
    channel = 0
    time = 0
    mf.addTrackName(0, time, "Video Track")
    mf.addTempo(0, time, 120)
    volume = 100
    for track, bool_array in enumerate(list_of_bool_arrays):
        print(f"Processing frame {track+1}/{len(list_of_bool_arrays)}")
        add_bool_array_to_midi(mf, bool_array, track, channel, time, volume)
    with open(output_file, 'wb') as outf:
        mf.writeFile(outf)



def image_to_midi(image, output_file, num_segments=48, threshold=140):
    """
    Converts an image to a MIDI file by thresholding and segmenting.

    Args:
        image (PIL.Image.Image or str): Input image or path.
        output_file (str): Output MIDI file path.
        num_segments (int): Number of vertical segments.
        threshold (int): Threshold for filtering.
    """
    bool_map = image_to_bool_array(image, num_segments, threshold)
    midi_from_bool_array(bool_map, output_file)


def frames_folder_to_bool_arrays(frames_folder, num_segments=48, threshold=140):
    """
    Loads all images from a folder and converts each to a boolean array.

    Args:
        frames_folder (str): Path to folder containing frames.
        num_segments (int): Number of vertical segments per image.
        threshold (int): Threshold for filtering.

    Returns:
        list[list[np.ndarray]]: List of boolean arrays (one per frame).
    """
    images = load_images_from_folder(frames_folder)
    bool_arrays = [image_to_bool_array(img, num_segments, threshold) for img in images]
    return bool_arrays

def frames_folder_to_midi(frames_folder, output_file, num_segments=48, threshold=140):
    """
    Converts all images in a folder to a multi-track MIDI file.

    Args:
        frames_folder (str): Path to folder containing frames.
        output_file (str): Output MIDI file path.
        num_segments (int): Number of vertical segments per image.
        threshold (int): Threshold for filtering.
    """
    bool_arrays = frames_folder_to_bool_arrays(frames_folder, num_segments, threshold)
    midi_from_bool_arrays(bool_arrays, output_file)


    
# ---------------- Long MIDI / scrollable MIDI videos ----------------

def midi_from_bool_arrays_long(list_of_bool_arrays, output_file):
    """
    Creates a single-track MIDI file from a list of 2D boolean arrays, concatenating them in time.

    Args:
        list_of_bool_arrays (list[list[np.ndarray]]): List of 2D boolean arrays.
        output_file (str): Output MIDI file path.
    """
    mf = MIDIFile(1)
    channel = 0
    track = 0
    time = 0
    mf.addTrackName(track, time, "Image Track")
    mf.addTempo(track, time, 120)
    volume = 100
    time_offset = 0
    for frame_index, bool_array in enumerate(list_of_bool_arrays):
        print(f"Processing frame {frame_index+1}/{len(list_of_bool_arrays)}")
        add_bool_array_to_midi(mf, bool_array, track, channel, time_offset, volume)
        time_offset += len(bool_array[0]) if bool_array else 0
    HORIZONTAL_RESOLUTION = len(list_of_bool_arrays[0][0]) if list_of_bool_arrays else 0
    with open("horizontal_resolution.txt", "w") as f:
        f.write(str(HORIZONTAL_RESOLUTION))
    with open(output_file, 'wb') as outf:
        mf.writeFile(outf)

def frames_folder_to_long_midi(frames_folder, output_file, num_segments=48, threshold=140):
    """
    Converts all images in a folder to a single-track, time-concatenated MIDI file.

    Args:
        frames_folder (str): Path to folder containing frames.
        output_file (str): Output MIDI file path.
        num_segments (int): Number of vertical segments per image.
        threshold (int): Threshold for filtering.
    """
    bool_arrays = frames_folder_to_bool_arrays(frames_folder, num_segments, threshold)
    midi_from_bool_arrays_long(bool_arrays, output_file)
    

def video_to_midi(video_path, output_file, num_segments=48, threshold=140):
    """
    Converts a video file to a single-track, time-concatenated MIDI file using OpenCV.

    Args:
        video_path (str): Path to the input video file.
        output_file (str): Output MIDI file path.
        num_segments (int): Number of vertical segments per frame.
        threshold (int): Threshold for filtering.
    """
    cap = cv2.VideoCapture(video_path)
    bool_arrays = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert BGR (OpenCV) to RGB (PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        bool_arrays.append(image_to_bool_array(img, num_segments, threshold))
        frame_count += 1

    cap.release()
    midi_from_bool_arrays_long(bool_arrays, output_file)