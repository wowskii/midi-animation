# Video to MIDI Animation

This project allows you to turn video files into a MIDI animation. The animation is basically a long reel of midi "frames" of equal length, that you can scroll through using `scroll.py` to create an animation. Here's a [demo video](https://youtu.be/la5YD5i3txY).

Who wants to read the README? I've made a simple [Video to MIDI Animation converter](https://midi-animation.streamlit.app) page to try out this project.

Seriously though...

## How to Use `convert_any.py`

This script converts an image or video file into a MIDI file.

### Usage

```bash
python convert.py <input_file> <output_midi>
```

- `<input_file>`: Path to your image (e.g., `.png`, `.jpg`) or video (e.g., `.mp4`, `.avi`) file.
- `<output_midi>`: Path where the generated MIDI file will be saved.

### Example

Convert an image:
```bash
python convert_any.py my_image.png output.mid
```

Convert a video:
```bash
python convert_any.py my_video.mp4 output.mid
```

### Notes

- For images, the script creates a MIDI file representing the image.
- For videos, the script creates a "scrollable" MIDI reel, where each frame is mapped to a segment of the MIDI file.
- Make sure you have all dependencies installed (`midiutil`, `Pillow`, `opencv-python`).



it's late, and i gotta go to sleep, but i promise i'll update this file tomorrow!