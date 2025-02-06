from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-002")

# Function to send query to Gemini model
def get_cgpa_response(image_data):
    prompt = "Extract the marks and grade points from the image, calculate CGPA, identify strengths, and suggest areas of improvement for the student."
    response = model.generate_content([prompt, image_data])
    return response.text

# Function to process the uploaded image
def input_image_setup(uploaded_image):
    byte_data = uploaded_image.getvalue()  # Get raw byte data
    image_parts = {
        "mime_type": uploaded_image.type,  # MIME type like "image/jpeg"
        "data": byte_data  # Raw binary data
    }
    return image_parts

# Streamlit page configuration
st.set_page_config(page_title="CGPA Calculator")
st.header("AI-Powered CGPA Calculator")

# File uploader widget for image upload
uploaded_file = st.file_uploader("Upload an image of your marksheet", type=["jpg", "png", "jpeg"])

# Process the uploaded image
if uploaded_file:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Marksheet", use_column_width=True)

    # Prepare the image data for the API
    input_image = input_image_setup(uploaded_file)

    # Button to trigger the CGPA calculation
    if st.button("Calculate CGPA"):
        # Get the model's response
        try:
            response = get_cgpa_response(input_image)
            st.subheader("Results")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")