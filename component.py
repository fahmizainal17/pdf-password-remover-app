# component.py
import streamlit as st
from PIL import Image
import base64
import os

def get_base64_of_bin_file(bin_file):
    """Encode a local file (image or gif) to a base64 string."""
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def page_style():
    # === Page configuration ===
    icon_path = "assets/logo.png"
    if not os.path.exists(icon_path):
        icon_path = "./assets/logo.png"
    try:
        icon = Image.open(icon_path)
        st.set_page_config(page_title="PDF Password Remover", page_icon=icon, layout="wide")
    except Exception as e:
        st.warning(f"Failed to load page icon: {e}")
        st.set_page_config(page_title="PDF Password Remover", layout="wide")

    # === Sidebar background image ===
    sidebar_image_path = "assets/background.jpg"
    if not os.path.exists(sidebar_image_path):
        sidebar_image_path = "./assets/background.jpg"
    try:
        sidebar_image_base64 = get_base64_of_bin_file(sidebar_image_path)
    except FileNotFoundError:
        st.warning(f"Sidebar background image not found at {sidebar_image_path}")
        sidebar_image_base64 = ""

    custom_style = f"""
        <style>
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}

            [data-testid="stSidebar"] > div:first-child {{
                background-color: #111;
                background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)),
                                 url("data:image/jpg;base64,{sidebar_image_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: local;
            }}
            .stButton>button, .stDownloadButton>button {{
                background-color: #228B22 !important;
                color: white !important;
            }}
            .cert-card {{
                background-color: #333333;
                color: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .cert-card:hover {{
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }}
        </style>
    """

    st.markdown(custom_style, unsafe_allow_html=True)

    # === Main banner image ===
    main_bg_path = "assets/Mainpdf_Background.png"
    if not os.path.exists(main_bg_path):
        main_bg_path = "./assets/Mainpdf_Background.png"
    try:
        main_bg = Image.open(main_bg_path)
        st.image(main_bg, use_container_width=True)
    except Exception as e:
        st.warning(f"Failed to load main background image: {e}")

    # === Sidebar content ===
    with st.sidebar:
        # Logo
        st.image("assets/logo.png", width=80)
        # Title Card
        st.markdown('<div class="cert-card"><h2>🔓 PDF Password Remover</h2><p>Effortlessly remove passwords from your encrypted PDF files.</p></div>', unsafe_allow_html=True)

        # How to Use Card
        st.markdown(
            '<div class="cert-card"><h3>How to Use</h3>' +
            '<ol>' +
            '<li>Upload one or more encrypted PDFs.</li>' +
            '<li>Enter the password(s) or use a single password.</li>' +
            '<li>Click the <strong>Remove Passwords</strong> button.</li>' +
            '<li>Download unlocked PDFs individually or as a ZIP archive.</li>' +
            '</ol></div>',
            unsafe_allow_html=True
        )

        # Note Card
        st.markdown('<div class="cert-card"><strong>Note:</strong> Only remove passwords for files you own or have permission to modify.</div>', unsafe_allow_html=True)

        # Technologies Card
        st.markdown(
            '<div class="cert-card"><h4>⚙️ Technologies</h4>' +
            '<ul>' +
            '<li>Streamlit</li>' +
            '<li>pypdf (PDF handling)</li>' +
            '<li>Python standard libraries</li>' +
            '<li>Session state for persistence</li>' +
            '</ul></div>',
            unsafe_allow_html=True
        )

        # Developer Credit with photo inside the card
        profile_img_path = "photos/Round_Profile_Photo.png"
        if not os.path.exists(profile_img_path):
            profile_img_path = "./photos/Round_Profile_Photo.png"
        try:
            profile_img_base64 = get_base64_of_bin_file(profile_img_path)
            profile_img_html = f'<img src="data:image/png;base64,{profile_img_base64}" width="80" style="border-radius:50%;margin-bottom:10px;" />'
        except Exception:
            profile_img_html = ""

        st.markdown(
            f'''<div class="cert-card" style="text-align:center;">
                {profile_img_html}
                <p>Developed with ❤️ by Fahmi Zainal</p>
                <p><a href="https://github.com/fahmizainal17/pdf-password-remover" style="color:white;">View on GitHub</a></p>
            </div>''',
            unsafe_allow_html=True
        )