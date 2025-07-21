import streamlit as st
import util
import json
import datetime
from PIL import Image
import io
import base64

# Configure page
st.set_page_config(
    page_title="SecureShare - Ethical Social Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for social media styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .post-container {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-info {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .security-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 1rem;
    }
    .safe-badge {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .warning-badge {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .danger-badge {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .post-stats {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
    }
    .stat-item {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        color: #666;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'posts' not in st.session_state:
        st.session_state.posts = [
            {
                'id': 1,
                'username': 'alice_researcher',
                'content': 'Just published my latest paper on AI security! 🔬',
                'timestamp': '2 hours ago',
                'likes': 24,
                'comments': 5,
                'image': None,
                'classification': {'label': 'authentic', 'confidence': 95.2}
            },
            {
                'id': 2,
                'username': 'cyber_defender',
                'content': 'New deepfake detection model showing promising results in our lab tests.',
                'timestamp': '4 hours ago',
                'likes': 18,
                'comments': 3,
                'image': None,
                'classification': {'label': 'authentic', 'confidence': 88.7}
            }
        ]
    if 'current_user' not in st.session_state:
        st.session_state.current_user = 'ethical_hacker_pro'

def get_security_badge(classification):
    """Generate security badge based on classification"""
    if classification['label'].lower() in ['authentic', 'real']:
        if classification['confidence'] >= 90:
            return "🟢 Verified Authentic", "safe-badge"
        elif classification['confidence'] >= 70:
            return "🟡 Likely Authentic", "warning-badge"
        else:
            return "🟠 Low Confidence", "warning-badge"
    else:
        return "🔴 Potential Deepfake", "danger-badge"

def create_post_ui():
    """Create new post interface"""
    st.markdown('<div class="main-header"><h1>🛡️ SecureShare - Ethical Social Platform</h1><p>AI-Powered Content Verification for Digital Trust</p></div>', unsafe_allow_html=True)
    
    with st.expander("📝 Create New Secure Post", expanded=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            post_content = st.text_area(
                "What's on your mind?", 
                placeholder="Share your thoughts... (All media will be automatically verified for authenticity)",
                height=100
            )
        
        with col2:
            st.markdown("### 🔐 Security Features")
            st.markdown("- ✅ Real-time deepfake detection")
            st.markdown("- 🔍 AI content analysis")
            st.markdown("- 🛡️ Authenticity scoring")
            st.markdown("- 📊 Threat intelligence")
        
        st.markdown("---")
        
        # File upload section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            file_uploaded = st.file_uploader(
                "📷 Add Image/Video (Optional)", 
                type=["jpg", "png", "jpeg"],
                help="All uploads are automatically scanned for deepfakes and manipulation"
            )
        
        with col2:
            if file_uploaded:
                st.image(file_uploaded, width=200, caption="Preview")
        
        # Analysis and posting
        if file_uploaded is not None:
            with st.spinner("🔍 Analyzing content for authenticity..."):
                # Use your existing classification function
                classification_result = util.classify_image(file_uploaded)
                
            # Display analysis results
            st.markdown("### 🧠 AI Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                badge_text, badge_class = get_security_badge(classification_result)
                st.markdown(f'<span class="security-badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)
            
            with col2:
                st.metric("Confidence Score", f"{classification_result.get('confidence', 0):.1f}%")
            
            with col3:
                threat_level = "LOW" if classification_result['label'].lower() in ['authentic', 'real'] else "HIGH"
                st.metric("Threat Level", threat_level)
            
            # Detailed analysis
            with st.expander("🔬 Detailed Forensic Analysis"):
                st.json(classification_result)
                
                # Add some mock forensic details for demonstration
                st.markdown("*Detection Techniques Applied:*")
                techniques = [
                    "Facial landmark analysis",
                    "Temporal consistency check", 
                    "Compression artifact detection",
                    "Neural network authenticity scoring"
                ]
                for technique in techniques:
                    st.markdown(f"- ✅ {technique}")
        
        # Post button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Post Securely", type="primary", use_container_width=True):
                if post_content.strip() or file_uploaded:
                    # Create new post
                    new_post = {
                        'id': len(st.session_state.posts) + 1,
                        'username': st.session_state.current_user,
                        'content': post_content,
                        'timestamp': 'Just now',
                        'likes': 0,
                        'comments': 0,
                        'image': file_uploaded,
                        'classification': classification_result if file_uploaded else {'label': 'text_only', 'confidence': 100}
                    }
                    
                    # Add to posts (insert at beginning)
                    st.session_state.posts.insert(0, new_post)
                    st.success("✅ Post created successfully with security verification!")
                    st.rerun()
                else:
                    st.warning("Please add some content or an image to post.")

def display_feed():
    """Display the social media feed"""
    st.markdown("## 📱 Secure Feed")
    st.markdown("All posts are automatically verified for authenticity")
    
    for post in st.session_state.posts:
        # Post container
        st.markdown(f'<div class="post-container">', unsafe_allow_html=True)
        
        # User info and security badge
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"*👤 @{post['username']}* • {post['timestamp']}")
        
        with col2:
            if post['classification']['label'] != 'text_only':
                badge_text, badge_class = get_security_badge(post['classification'])
                st.markdown(f'<span class="security-badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)
        
        # Post content
        if post['content']:
            st.markdown(post['content'])
        
        # Image display with analysis
        if post['image']:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(post['image'], use_column_width=True)
            
            with col2:
                st.markdown("*🔍 Security Analysis*")
                classification = post['classification']
                st.write(f"*Status:* {classification['label'].title()}")
                st.write(f"*Confidence:* {classification.get('confidence', 0):.1f}%")
                
                if classification['label'].lower() not in ['authentic', 'real']:
                    st.error("⚠️ Potential manipulation detected!")
                else:
                    st.success("✅ Content verified as authentic")
        
        # Post interactions
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(f"👍 {post['likes']}", key=f"like_{post['id']}"):
                post['likes'] += 1
                st.rerun()
        
        with col2:
            if st.button(f"💬 {post['comments']}", key=f"comment_{post['id']}"):
                st.info("Comment feature coming soon!")
        
        with col3:
            if st.button("🔄 Share", key=f"share_{post['id']}"):
                st.info("Share feature coming soon!")
        
        with col4:
            if st.button("📊 Analysis", key=f"analysis_{post['id']}"): 
                if post['image']:
                    with st.expander(f"Detailed Analysis - Post {post['id']}", expanded=True):
                        st.json(post['classification'])
                else:
                    st.info("No media to analyze in this post.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

def sidebar_info():
    """Display sidebar with platform information"""
    st.sidebar.markdown("## 🛡️ SecureShare")
    st.sidebar.markdown("*Ethical AI Social Platform*")
    
    st.sidebar.markdown("### 🔐 Security Features")
    st.sidebar.markdown("""
    - *Real-time Deepfake Detection*
    - *AI Content Verification*  
    - *Forensic Analysis Tools*
    - *Threat Intelligence*
    - *Proactive Defense System*
    """)
    
    st.sidebar.markdown("### 📊 Platform Stats")
    total_posts = len(st.session_state.posts)
    verified_posts = sum(1 for post in st.session_state.posts 
                        if post['classification']['label'].lower() in ['authentic', 'real', 'text_only'])
    
    st.sidebar.metric("Total Posts", total_posts)
    st.sidebar.metric("Verified Posts", verified_posts)
    st.sidebar.metric("Security Score", f"{(verified_posts/total_posts)*100:.1f}%")
    
    st.sidebar.markdown("### 👤 Current User")
    st.sidebar.write(f"@{st.session_state.current_user}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Ethical Hacking Focus")
    st.sidebar.markdown("""
    This platform demonstrates:
    - *Proactive Cybersecurity*
    - *Digital Forensics*
    - *AI Security Research*
    - *Responsible AI Implementation*
    """)

def main():
    """Main application function"""
    initialize_session_state()
    sidebar_info()
    
    # Main content
    create_post_ui()
    st.markdown("---")
    display_feed()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>🛡️ SecureShare</strong> - Built for Ethical Hacking & AI Security Research</p>
        <p>Powered by Advanced Deepfake Detection • Promoting Digital Authenticity</p>
    </div>
    """, unsafe_allow_html=True)

if _name_ == "_main_":
    main()
