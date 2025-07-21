import streamlit as st
import util
import os
import io
from PIL import Image
from datetime import datetime

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_image_and_result(uploaded_file, username, caption):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    image_bytes = uploaded_file.read()
    with open(img_path, 'wb') as f:
        f.write(image_bytes)
    result = util.classify_image(io.BytesIO(image_bytes))
    with open(img_path + ".txt", 'w') as f:
        f.write("|".join([
            result['label'],
            timestamp,
            username,
            caption
        ]))
    return img_path, result['label'], timestamp, username, caption

def load_feed():
    files = sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
    posts = []
    for file in files:
        img_path = os.path.join(UPLOAD_FOLDER, file)
        txt_file = img_path + ".txt"
        label, timestamp, username, caption = "Unknown", "", "anonymous", ""
        if os.path.exists(txt_file):
            with open(txt_file, 'r') as f:
                content = f.read().strip().split('|')
                label = content[0].title() if len(content) > 0 else label
                timestamp = content[1] if len(content) > 1 else timestamp
                username = content[2] if len(content) > 2 else username
                caption = content[3] if len(content) > 3 else caption
        posts.append({
            "img_path": img_path,
            "label": label,
            "timestamp": timestamp,
            "username": username,
            "caption": caption
        })
    return posts

def app():
    st.markdown("""
        <style>
            .post-card {
                background: #fff;
                border-radius: 20px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.08);
                margin-bottom: 2em;
                padding: 0 0 1em 0;
                max-width: 500px;
                margin-left: auto;
                margin-right: auto;
            }
            .avatar {
                width: 44px; height: 44px; border-radius: 50%;
                display: inline-block; background: linear-gradient(135deg,#ef4444,#8b5cf6); 
                color: #fff; text-align: center; font-weight: bold; font-size: 21px; line-height: 44px;
            }
            .badge-overlay {
                position: absolute; right: 24px; top: 24px;
                background: #38C172; color: #fff; padding: 6px 16px;
                border-radius: 20px; font-size: 16px; font-weight: bold; opacity: 0.97;
            }
            .badge-overlay.fake {background: #E3342F;}
            .caption {font-size: 16px; margin-top: 8px;}
            .insta-actions {color: #222; font-size: 18px; margin-top: 5px;}
        </style>
    """, unsafe_allow_html=True)
    st.title("InstaFake • Feed")

    with st.container():
        st.subheader("Share a New Post")

        c1, c2 = st.columns([1,5])
        with c1:
            username = st.text_input("Username", value="anonymous", key="usr")
        with c2:
            caption = st.text_input("Caption", max_chars=120, key="cap")

        uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            img_path, label, timestamp, username, caption = save_image_and_result(
                uploaded_file, username, caption
            )
            st.success(f"Your post was uploaded as {label.upper()}!")

    st.markdown("---")
    posts = load_feed()
    if not posts:
        st.info("No images yet. Start the feed with your post!")
    else:
        for post in posts:
            st.markdown('<div class="post-card">', unsafe_allow_html=True)
            # Top bar: avatar + username + time
            row = st.columns([1,6,3])
            with row[0]:
                st.markdown(
                    f'<div class="avatar">{post["username"][0:2].upper()}</div>',
                    unsafe_allow_html=True
                )
            with row[1]:
                st.markdown(f"<b>{post['username']}</b>", unsafe_allow_html=True)
            with row[2]:
                st.markdown(
                    f"<span style='color:#888;font-size:13px;'>{post['timestamp']}</span>",
                    unsafe_allow_html=True
                )
            # Image with detection badge
            st.image(post["img_path"], use_column_width=True)
            badge_class = "badge-overlay fake" if post["label"].lower() == "fake" else "badge-overlay"
            st.markdown(
                f"""
                <div style="position:relative;width:100%;text-align:right;">
                  <span class="{badge_class}">{post["label"].upper()}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Caption
            if post["caption"]:
                st.markdown(
                    f'<div class="caption">{post["caption"]}</div>', unsafe_allow_html=True
                )
            # Like/Comment icons
            st.markdown(
                '<div class="insta-actions">❤️ 0&nbsp;&nbsp;&nbsp;💬 0</div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
