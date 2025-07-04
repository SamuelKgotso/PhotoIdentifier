import streamlit as st
from PIL import Image
import base64
import io
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key="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") # Replace with your OpenAI API key

# Function to convert image to base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Function to get GPT-4o response
def get_openai_response(input_text, image):
    image_base64 = encode_image(image)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": input_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="OpenAI Vision Demo")
st.header("OpenAI Vision App")

input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze with OpenAI")

if submit:
    if input_text and image:
        try:
            response = get_openai_response(input_text, image)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please provide both input text and an image.")
