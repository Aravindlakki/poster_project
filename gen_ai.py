import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import base64

# -------------------- Helper Functions --------------------

def create_poster(title, content, theme="modern"):
    width, height = 600, 900
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Define themes with gradient-like backgrounds and colors
    themes = {
        "modern": {
            "bg_top": (58, 123, 213),
            "bg_bottom": (0, 210, 255),
            "text": (255, 255, 255),
            "accent": (255, 255, 255)
        },
        "sunset": {
            "bg_top": (255, 94, 98),
            "bg_bottom": (255, 195, 113),
            "text": (255, 255, 255),
            "accent": (255, 255, 255)
        },
        "forest": {
            "bg_top": (34, 139, 34),
            "bg_bottom": (107, 142, 35),
            "text": (255, 255, 255),
            "accent": (255, 255, 255)
        },
        "midnight": {
            "bg_top": (25, 25, 112),
            "bg_bottom": (0, 0, 50),
            "text": (230, 230, 250),
            "accent": (173, 216, 230)
        }
    }

    t = themes.get(theme, themes["modern"])

    # Gradient background
    for y in range(height):
        ratio = y / height
        r = int(t["bg_top"][0] * (1 - ratio) + t["bg_bottom"][0] * ratio)
        g = int(t["bg_top"][1] * (1 - ratio) + t["bg_bottom"][1] * ratio)
        b = int(t["bg_top"][2] * (1 - ratio) + t["bg_bottom"][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Load font
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        body_font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw title with shadow
    title_y = 80
    draw.text((width // 2 + 2, title_y + 2), title, font=title_font, fill=(0, 0, 0), anchor="mm")
    draw.text((width // 2, title_y), title, font=title_font, fill=t["text"], anchor="mm")

    # Subtitle
    subtitle = f"Presented by AI Poster Generator"
    subtitle_y = title_y + 50
    draw.text((width // 2 + 1, subtitle_y + 1), subtitle, font=subtitle_font, fill=(0, 0, 0), anchor="mm")
    draw.text((width // 2, subtitle_y), subtitle, font=subtitle_font, fill=t["accent"], anchor="mm")

    # Body text
    margin = 50
    text_top = subtitle_y + 60
    text_width = width - 2 * margin
    char_width = body_font.getlength("A")
    max_chars = int(text_width // char_width)

    lines = textwrap.wrap(content, width=max_chars)
    y = text_top
    for line in lines:
        draw.text((margin, y), line, font=body_font, fill=t["text"])
        y += 30

    # Footer
    footer_text = "www.generatedposter.ai"
    draw.rectangle([0, height - 50, width, height], fill=(0, 0, 0))
    draw.text((width // 2, height - 30), footer_text, font=subtitle_font, fill=(255, 255, 255), anchor="mm")

    return img

def get_image_download_link(img, filename="poster.png"):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">📥 Download Poster</a>'
    return href

# -------------------- Streamlit UI --------------------

st.set_page_config(page_title="AI Poster Generator", layout="centered")
st.title("🖼️ AI Poster Generator")
st.caption("Turn your message into a beautiful poster image.")

title = st.text_input("🎯 Poster Title", "Live Fully")
content = st.text_area("✍️ Poster Content", "Life is meant to be lived to the fullest. Embrace the moment, cherish relationships, and never stop growing.")
theme = st.selectbox("🎨 Choose a Theme", ["modern", "sunset", "forest", "midnight"])

if st.button("✨ Generate Poster"):
    poster_img = create_poster(title, content, theme)
    st.image(poster_img, caption="Here’s your poster", use_column_width=True)
    st.markdown(get_image_download_link(poster_img), unsafe_allow_html=True)
