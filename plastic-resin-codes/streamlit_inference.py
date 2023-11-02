#import dependencies
import streamlit as st
import requests
from io import BytesIO 
from PIL import Image # to open image from BytesIO object

from tensorflow.keras.applications.efficientnet_v2 import preprocess_input as efficientnetv2_preprocess_input
#############################

# Server api
api_url = "http://192.168.50.24:8080"
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
    image_data = uploaded_image.read() # read file  
    image_pil = Image.open(BytesIO(image_data)) # display image using PIL
   
    #Send the image to the Flask API
    response = requests.post(f'{api_url}{api_route}', files={'image': image_data})

    try:
        # Check if the image has EXIF data and an orientation tag to reorientate for 
        exif = image_pil._getexif()
        orientation = exif.get(0x0112, 1)
        if orientation == 3:
            image_pil = image_pil.rotate(180, expand=True)
        elif orientation == 6:
            image_pil = image_pil.rotate(270, expand=True)
        elif orientation == 8:
            image_pil = image_pil.rotate(90, expand=True)
            
        #
        #send image data and retrieve response
        prediction = response.json()['predictions'][0]
        st.image(image_pil, caption= f'Uploaded image: {uploaded_image.name}', width=224)
        st.write(f'Code type: **{prediction}**')
    except Exception as e:
        st.write(f'Error processing API response: {e}')
