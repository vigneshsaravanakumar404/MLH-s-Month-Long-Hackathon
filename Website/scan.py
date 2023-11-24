import streamlit as st
import requests
import base64
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Functions

def send_image_to_server(image, url):
    """
    Sends an image to a server using a POST request.

    Args:
        image_path (str): The path to the image file.
        url (str): The URL of the server to send the image to.

    Returns:
        requests.Response: The response from the server.
    """
    encoded_string = base64.b64encode(image).decode()
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = json.dumps({"image": encoded_string})

    response = requests.post(url, data=data, headers=headers)
    return response

def app():
    st.header("Scan")
    st.write("Scan items to recycle them correctly.")

    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # Read the image into bytes
        image_bytes = img_file_buffer.getvalue()
        response = send_image_to_server(image=image_bytes, url='http://localhost:5000/objects')
        response_data = response.json()
        st.write(response_data)
    else:
        st.write("No image selected")
    