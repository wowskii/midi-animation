import streamlit as st
from utilities import video_to_midi
import cv2
import tempfile
from utilities import image_to_midi

st.title("Video to MIDI Converter 🎹")

uploaded_file = st.file_uploader("Upload an image or a video", type=["mp4", "mov", "avi", "mkv", "webm", "png", "jpg", "jpeg", "bmp", "gif"])
num_segments = st.slider("Number of segments (higher = more detail)", min_value=10, max_value=100, value=48, step=1)
threshold = st.slider("Brightness threshold (how the algorithm differentiates the foreground and background of the video)", min_value=0, max_value=255, value=140, step=1)
invert_colors = st.checkbox("Invert colors", value=False)
if uploaded_file:
    if uploaded_file.type.startswith("image/"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(uploaded_file.read())
            temp_image_path = tmp.name

        with st.spinner("Converting image to MIDI..."):
            output_path = "output.mid"
            image_to_midi(temp_image_path, output_path, num_segments=num_segments, threshold=threshold, invert=invert_colors)
        with open(output_path, "rb") as f:
            st.download_button("Download MIDI", f, file_name="output.mid")
    else:
        # Save uploaded video to a temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded_file.read())
            temp_video_path = tmp.name

        # Check video duration
        cap = cv2.VideoCapture(temp_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps else 0
        cap.release()

        if duration > 60:
            st.error("Video is longer than 1 minute. Please upload a shorter video.")
        else:
            with st.spinner("Converting video to MIDI..."):
                output_path = "output.mid"
                video_to_midi(temp_video_path, output_path, num_segments=num_segments, threshold=threshold, invert=invert_colors)
            with open(output_path, "rb") as f:
                st.download_button("Download MIDI", f, file_name="output.mid")


"""You might wanna know:
The MIDI output is a long reel of "frames" where each frame corresponds to a frame in the video.
You can go through these frames by scrolling horizontally in your MIDI viewer. For FL Studio users, it helps to turn off animations in Settings > General, to avoid lag when scrolling.
I personally use this python script to scroll automatically: """
st.download_button("Download scroll.py", data=open("scroll.py", "rb"), file_name="scroll.py")
"""here's how to use it (you need to install `pynput` first):"""
st.code("""scroll.py [HORIZONTAL_RESOLUTION]"""
        #HORIZONTAL_RESOLUTION is optional, if not provided it will be read from horizontal_resolution.txt
)
"""More details will be available in the README of the GitHub repo soon!
Here's a preview of the MIDI output for the video I uploaded:
https://youtu.be/la5YD5i3txY?si=fWyBKqsTSn4V7-pU"""
