import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import random

# Function to get random quote
def get_motivational_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        return f'"{data[0]["q"]}"\n- {data[0]["a"]}'
    except:
        backup_quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
        ]
        return random.choice(backup_quotes)
def draw_attribution(draw, font, img, img_width, img_height):  # Added img parameter
    attribution_text = "Rprogrammers.com"
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), attribution_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    x_position = img_width - text_width - 20  # 20px from right edge
    y_position = img_height - 50  # 50px from bottom
    
    # Draw semi-transparent background
    bg_width = text_width + 20
    bg_height = 40
    text_bg = Image.new('RGBA', (bg_width, bg_height), (0, 0, 0, 150))
    img.paste(text_bg, (x_position - 10, y_position - 10), text_bg)
    
    # Draw text
    draw.text(
        (x_position, y_position),
        attribution_text,
        font=font,
        fill=(255, 255, 255),
        align="right"
    )

# Function to generate wallpaper with todos
def generate_wallpaper_with_todos(todos):
    # Get random wallpaper (1920x1080)
    response = requests.get("https://picsum.photos/1920/1080")
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    
    try:
        main_font = ImageFont.truetype("times.ttf", 36)  # Main content font
        attribution_font = ImageFont.truetype("times.ttf", 24)  # Smaller font for attribution
    except:
        main_font = ImageFont.load_default()
        attribution_font = ImageFont.load_default()
        st.warning("Times New Roman font not found, using default font")

    # Create todo text with line breaks
    todo_text = "To-Do List:\n\n" + "\n".join(f"• {task}" for task in todos)
    
    # Add motivational quote
    todo_text += "\n\n" + get_motivational_quote()
    
    # Calculate main text position
    margin = 50
    max_width = 600
    line_height = 45
    wrapped_text = []
    
    # Wrap text while preserving existing newlines
    for line in todo_text.split('\n'):
        wrapped_text.extend(textwrap.wrap(line, width=40, break_long_words=False))
    
    text_height = len(wrapped_text) * line_height
    
    # Create semi-transparent background for main text
    text_bg = Image.new('RGBA', (max_width + 40, text_height + 60), (0, 0, 0, 180))
    img.paste(text_bg, (img.width - max_width - margin - 20, margin - 30), text_bg)
    
    # Draw main text
    y = margin
    for line in wrapped_text:
        draw.text(
            (img.width - max_width - margin, y),
            line,
            font=main_font,
            fill=(255, 255, 255),
            align="left"
        )
        y += line_height
    
    # Draw Rprogrammers.com attribution
    draw_attribution(draw, attribution_font, img, img.width, img.height)  # Added img argument
    
    return img
# Initialize session state
if "todos" not in st.session_state:
    st.session_state.todos = []

# App layout
st.title("Professional Todo Wallpaper Generator")
st.write("Add tasks and generate downloadable wallpapers with your list + motivational quote")

# Todo input
new_task = st.text_input("Add new task:")
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("Add Task") and new_task:
        st.session_state.todos.append(new_task)
with col2:
    if st.button("Clear All Tasks"):
        st.session_state.todos = []

# Display current todos
st.subheader("Current Tasks:")
for i, task in enumerate(st.session_state.todos):
    cols = st.columns([6, 1])
    cols[0].markdown(f"**{i+1}.** {task}")
    if cols[1].button("❌", key=f"delete_{i}"):
        st.session_state.todos.pop(i)
        st.experimental_rerun()

# Generate wallpaper button
if st.button("✨ Generate Wallpaper"):
    if st.session_state.todos:
        with st.spinner("Creating professional wallpaper..."):
            # Generate image
            img = generate_wallpaper_with_todos(st.session_state.todos)
            
            # Save to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
            # Create download button
            st.download_button(
                label="📥 Download Wallpaper",
                data=img_bytes,
                file_name="professional_todo_wallpaper.png",
                mime="image/png"
            )
            
            # Show preview
            st.image(img, caption="Your Professional Wallpaper Preview", use_column_width=True)
    else:
        st.warning("Please add some tasks first!")

st.markdown("---")
st.info("💡 Pro Tip: Add clear, concise tasks and generate a new wallpaper whenever you update your list for maximum productivity!")