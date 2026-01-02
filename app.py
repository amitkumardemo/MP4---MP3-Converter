import streamlit as st
import tempfile
import os
import subprocess
import imageio_ffmpeg

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="MP4 Mobile Video Converter | TechieHelp",
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
    "Choose MP4 video (any ratio: 9:16, 16:9, 1:1)",
    type=["mp4"]
)

if uploaded:
    st.video(uploaded)

    st.subheader("⚙️ Select Output Quality (Aspect Ratio Preserved)")

    quality = st.selectbox(
        "Choose target height",
        ["360p", "480p", "720p"]
    )

    height_map = {
        "360p": "360",
        "480p": "480",
        "720p": "720"
    }

    target_height = height_map[quality]

    if st.button("🚀 Convert & Download Video", use_container_width=True):
        with st.spinner("Converting video (keeping original aspect ratio)..."):
            # Save uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(uploaded.read())
                input_path = tmp.name

            output_path = input_path.replace(".mp4", "_mobile.mp4")

            # Get FFmpeg path safely
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

            # 🔥 Aspect Ratio SAFE command
            command = [
                ffmpeg_path, "-y",
                "-i", input_path,
                "-vf", f"scale=-2:{target_height}",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "24",
                "-pix_fmt", "yuv420p",
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

        st.success("🎉 Video converted (aspect ratio preserved)")

        st.download_button(
            label="⬇️ Download MP4 Video",
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
