import streamlit as st
import tempfile
import os
import subprocess
import imageio_ffmpeg

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="MP4 to Mobile Video Converter | TechieHelp",
    page_icon="📱",
    layout="centered"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.title {
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    color: #ff4b4b;
}
.box {
    background: #f8f9fb;
    padding: 1.5rem;
    border-radius: 12px;
    margin-top: 1.5rem;
}
.footer {
    text-align: center;
    font-size: 0.9rem;
    color: #666;
    margin-top: 2rem;
}
.footer a {
    color: #ff4b4b;
    text-decoration: none;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="title">📱 MP4 to Mobile Video Converter</div>', unsafe_allow_html=True)

# =========================
# UPLOAD
# =========================
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("📤 Upload MP4 Video")

uploaded = st.file_uploader(
    "Choose MP4 video",
    type=["mp4"]
)

if uploaded:
    st.video(uploaded)

    st.subheader("⚙️ Select Mobile Quality")

    quality = st.selectbox(
        "Choose resolution",
        ["360p (Small)", "480p (Medium)", "720p (HD)"]
    )

    scale_map = {
        "360p (Small)": "640:360",
        "480p (Medium)": "854:480",
        "720p (HD)": "1280:720"
    }

    scale = scale_map[quality]

    if st.button("🚀 Convert & Download Video", use_container_width=True):
        with st.spinner("Converting video for mobile..."):
            # Save uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(uploaded.read())
                input_path = tmp.name

            output_path = input_path.replace(".mp4", "_mobile.mp4")

            # Get FFmpeg path safely
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

            # FFmpeg command
            command = [
                ffmpeg_path, "-y",
                "-i", input_path,
                "-vf", f"scale={scale}",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "24",
                "-c:a", "aac",
                "-b:a", "128k",
                output_path
            ]

            subprocess.run(command, check=True)

            # Read output
            with open(output_path, "rb") as f:
                video_bytes = f.read()

            # Cleanup
            os.remove(input_path)
            os.remove(output_path)

        st.success("🎉 Video converted successfully!")

        st.download_button(
            label="⬇️ Download Mobile MP4",
            data=video_bytes,
            file_name="converted_mobile_video.mp4",
            mime="video/mp4",
            use_container_width=True
        )

        st.video(video_bytes)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown(
    """
    <div class="footer">
        Built with ❤️ by <a href="https://techiehelp.in" target="_blank">TechieHelp</a><br>
        AI • Automation • Software Solutions
    </div>
    """,
    unsafe_allow_html=True
)
