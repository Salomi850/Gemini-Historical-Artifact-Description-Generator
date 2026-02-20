import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
import io

# Load API key
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

st.write("API KEY Loaded:", bool(api_key))  # debug check

client = genai.Client(api_key=api_key)

st.title("🏺 Gemini Historical Artifact Description")
st.write("Upload a historical artifact image to get details")

uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Generate Description"):

        img_bytes = io.BytesIO()
        image.convert("RGB").save(img_bytes, format="JPEG")

        image_part = types.Part.from_bytes(
            data=img_bytes.getvalue(),
            mime_type="image/jpeg"
        )

        prompt = """
        You are a professional historian.
        Identify the artifact and explain:
        Name
        Time period
        Civilization
        Material
        Usage
        Interesting facts
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, image_part],
        )

        st.subheader("📜 Historical Details")
        st.write(response.text)