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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    image_bytes = uploaded_file.read()
    with open(img_path, 'wb') as f:
        f.write(image_bytes)
    result = util.classify_image(io.BytesIO(image_bytes))
    with open(img_path + ".txt", 'w') as f:
        f.write(result['label'] + "|" + timestamp)
    return img_path, result['label'], timestamp

def load_feed():
    files = sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
    posts = []
    for file in files:
        img_path = os.path.join(UPLOAD_FOLDER, file)
        txt_file = img_path + ".txt"
        label, timestamp = "Unknown", ""
        if os.path.exists(txt_file):
            with open(txt_file, 'r') as f:
                content = f.read().strip().split('|')
                label = content[0].title()
                if len(content) > 1:
                    timestamp = content[1]
        posts.append({"img_path": img_path, "label": label, "filename": file, "timestamp": timestamp})
    return posts

def app():
    st.markdown("""
        <style>
            .post-card {
                background: #fff; border-radius: 15px; box-shadow: 0 2px 7px rgba(0,0,0,0.05);
                margin-bottom: 2em; padding: 1em;
            }
            .avatar {width: 40px; height: 40px; border-radius: 50%; background: #eee; display: inline-block;}
            .insta-label {display: inline-block; background: #38C172; color: #fff;
                border-radius: 7px; padding: 2px 10px; margin-left: 7px; font-size: 14px;}
            .insta-label.fake {background: #E3342F;}
        </style>""", unsafe_allow_html=True)
    st.title("InstaFake • Feed")

    with st.container():
        st.subheader("Share a New Post")
        uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            img_path, label, timestamp = save_image_and_result(uploaded_file)
            st.success(f"Posted! This image was detected as: {label}")

    st.markdown("---")
    posts = load_feed()
    if not posts:
        st.info("No images yet. Start the feed with your post!")
    else:
        for post in posts:
            st.markdown('<div class="post-card">', unsafe_allow_html=True)
            cols = st.columns([1, 8])
            with cols[0]:
                st.markdown('<div class="avatar"></div>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"<b>anonymous</b> <span style='color:#888;font-size:13px;'>{post['timestamp']}</span>", unsafe_allow_html=True)
                st.image(post["img_path"], use_column_width=True)
                label_class = "insta-label fake" if post['label'].lower() == 'fake' else "insta-label"
                st.markdown(f"<span class='{label_class}'>{post['label']}</span>", unsafe_allow_html=True)
                st.markdown("❤️ 0 &nbsp; 💬 0", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
