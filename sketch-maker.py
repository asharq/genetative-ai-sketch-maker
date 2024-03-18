import openai
import streamlit as st
import logging
from openai import OpenAI
from streamlit_drawable_canvas import st_canvas

# Configure OpenAI
client = OpenAI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize session state variables if they're not already present
if 'text_prompt' not in st.session_state:
    st.session_state['text_prompt'] = ""
if 'generated_image_url' not in st.session_state:
    st.session_state['generated_image_url'] = None

# Set Streamlit page config
st.set_page_config(page_title="Stylus Generative Sketch Maker", layout="wide")

# App title and header
st.title("✏️ Stylus Generative Sketch Maker 🖌️")

# Function to generate sketch from prompt
def generate_sketch_from_prompt(prompt):
    safety_guard = "Generate a sketch that's easy to doodle using a stylus. Please ensure the sketch is in black and white, clear, and simple."
    full_prompt = f"{safety_guard} {prompt}"

    logging.info("Starting sketch generation process...")
    with st.spinner('🖼️ Generating your sketch...'):
        try:
            logging.info(f"Sending prompt to OpenAI API: {full_prompt}")
            response = client.images.generate(
                prompt=full_prompt,
                model="dall-e-3",
                n=1,
                size="1024x1024"
            )
            logging.info("Received response from OpenAI API")
            image_url = response.data[0].url
            logging.info(f"Sketch generated successfully: {image_url}")
            st.success('🎉 Sketch generated successfully!')
            return image_url
        except Exception as e:
            logging.error(f"An error occurred during sketch generation: {e}", exc_info=True)
            st.error(f"An error occurred: {e}")
            return None

# Text input for the prompt, directly bound to the session state
text_prompt = st.text_input("🖋️ Type your sketch idea here:", key='text_prompt')

# Function to handle the sketch generation button click
def handle_generate_click():
    generated_image_url = generate_sketch_from_prompt(st.session_state['text_prompt'])
    if generated_image_url:
        st.session_state['generated_image_url'] = generated_image_url

# Button to generate the sketch
st.button("🔮 Generate Sketch!", on_click=handle_generate_click)

# Display the generated sketch and sketch area side by side if a sketch has been generated
if st.session_state['generated_image_url']:
    cols = st.columns(2)  # Create two columns for side by side layout
    with cols[0]:  # First column for the sketch
        st.image(st.session_state['generated_image_url'], caption="🖼️ Your Generated Sketch", width=400)
        st.markdown(f"[🎁 Download Sketch]({st.session_state['generated_image_url']})", unsafe_allow_html=True)
    with cols[1]:  # Second column for the drawing area
        st.header("🖍️ Doodle on Your Sketch")
        sketch = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",  # Transparent
            stroke_width=2,
            stroke_color="#000000",  # Black
            background_color="#FFFFFF",  # White
            height=400,
            width=400,
            drawing_mode="freedraw",
            display_toolbar=True,
            key="canvas"
        )
