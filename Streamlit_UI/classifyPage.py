import streamlit as st
import util
import os
import io
from PIL import Image
from datetime import datetime

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_image_and_result(uploaded_file):
    # Save image with timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    image_bytes = uploaded_file.read()
    with open(img_path, 'wb') as f:
        f.write(image_bytes)
    # Run deepfake detection
    result = util.classify_image(io.BytesIO(image_bytes))
    # Save result to a sidecar file
    with open(img_path + ".txt", 'w') as f:
        f.write(result['label'])
    return img_path, result['label']

def load_feed():
    # Get all image files sorted by latest
    files = sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
    posts = []
    for file in files:
        img_path = os.path.join(UPLOAD_FOLDER, file)
        txt_file = img_path + ".txt"
        label = "Unknown"
        if os.path.exists(txt_file):
            with open(txt_file, 'r') as f:
                label = f.read().strip().title()
        posts.append({"img_path": img_path, "label": label, "filename": file})
    return posts

def app():
    st.title("Social Media Clone: Deepfake Detector")

    # Upload Section
    st.header("Share a New Image")
    uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img_path, label = save_image_and_result(uploaded_file)
        st.success(f"Uploaded! The image was labeled: {label}")

    st.markdown("---")
    st.header("🔎 Public Timeline")
    posts = load_feed()
    if not posts:
        st.info("No images yet. Be the first to post!")
    else:
        for post in posts:
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(post["img_path"], width=150)
            with c2:
                st.markdown(f"**Classification:** {post['label']}")
                st.caption(f"Filename: {post['filename']}")
            st.markdown('---')

    st.write("Created by - Meryn, Nivedita")
