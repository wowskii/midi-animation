import sys
import os
from utilities import image_to_midi, video_to_midi

def print_usage():
    print("Usage:")
    print("  python convert.py <input_file> <output_midi> [--long]")
    print("    <input_file>: Path to image or video file")
    print("    <output_midi>: Path to output MIDI file")
    print("    --long: (optional) For images, output a long MIDI reel (horizontal scroll)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    long_mode = "--long" in sys.argv


    ext = os.path.splitext(input_file)[1].lower()
    image_exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
    video_exts = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

    if ext in image_exts:
        image_to_midi(input_file, output_file)
        print(f"Converted image '{input_file}' to MIDI '{output_file}'")
    elif ext in video_exts:
        video_to_midi(input_file, output_file)
        print(f"Converted video '{input_file}' to MIDI '{output_file}'")
    else:
        print(f"Unsupported file type: {ext}")
        print_usage()
        sys.exit(1)