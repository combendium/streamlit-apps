#import dependencies
import streamlit as st
import requests
from io import BytesIO

from tensorflow.keras.applications.efficientnet_v2 import preprocess_input as efficientnetv2_preprocess_input
#############################

# Server api
api_url = "https://plastic-resin-code-r7wxdlansa-as.a.run.app"
api_route = '/predict'

# Page config
st.set_page_config(
    page_title="♻️Recycling with Plastic Resin Code🔢",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("♻️Classifying plastic resin codes recycling")

#load image
uploaded_image = st.file_uploader(":system-color[Upload an image in the box below to begin.]", type=["jpg", "png", "jpeg"], help='Please upload a single image at a time in .png or .jpg or .jpeg format.')

predictions = []

if uploaded_image is None:
    st.write(f'<p style="font-size:20px;">Step 1: Upload a file from a local drive or drag an image from browser</p>', unsafe_allow_html=True)
    st.write(f'<p style="font-size:20px;font-style:bold;">Step 2: Wait for result of classification</p>', unsafe_allow_html=True)
    st.write(f'<p style="font-size:16px;color:blue;font-style:bold;">Please use a picture with the symbol framed as big as possible </p>', unsafe_allow_html=True)
    st.write(f'<p style="font-size:16px;font-style:italic;">Disclaimer: Still in beta, classification is not perfect. </p>', unsafe_allow_html=True)

else: 
    st.spinner("In progress.. Please give it a few seconds..")
    file_data = uploaded_image.read()
    #Send the image to the Flask API
    response = requests.post(f'{api_url}{api_route}', files={'image': file_data})

    try:
        prediction = response.json()['predictions'][0]
        st.image(uploaded_image, caption= f'Uploaded image: {uploaded_image.name}', width=224)
        st.write(f'Code type: **{prediction}**')
    except Exception as e:
        st.write(f'Error processing API response: {e}')
