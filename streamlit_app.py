import streamlit as st
from utilities import video_to_midi  # your function

st.title("Video to MIDI Converter 🎹")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
if uploaded_file:
    with open("temp.mp4", "wb") as f:
        f.write(uploaded_file.read())
    output_path = "output.mid"
    video_to_midi("temp.mp4", output_path)
    with open(output_path, "rb") as f:
        st.download_button("Download MIDI", f, file_name="output.mid")
