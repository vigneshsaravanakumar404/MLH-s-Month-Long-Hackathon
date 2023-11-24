import streamlit as st
import requests
import base64
import json
import time

# Functions
def send_image_to_server(image, url):
    """
    Sends an image to a server using a POST request with retry on failure.

    Args:
        image (bytes): The image data in bytes.
        url (str): The URL of the server to send the image to.

    Returns:
        requests.Response: The response from the server.
    """
    encoded_string = base64.b64encode(image).decode()
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = json.dumps({"image": encoded_string})

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.post(url, data=data, headers=headers)
            return response
        except requests.ConnectionError:
            if attempt < 2:  # Don't show a message on the final attempt
                st.warning("Connection error, retrying...")
            time.sleep(1)  # Wait a bit before retrying
    return None  # Return None if all retries fail

def app():
    st.header("Scan")
    st.write("Scan items to recycle them correctly.")

    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        image_bytes = img_file_buffer.getvalue()

        # Button to send the request
        if st.button("Scan"):
            with st.spinner("Processing..."):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.04)  # Simulate time passing (4 seconds total)
                    progress_bar.progress(percent_complete + 1)
            
            response = send_image_to_server(image=image_bytes, url='http://localhost:5000/objects')
            
            if response is not None:
                response_data = response.json()
                st.write(response_data)
                progress_bar.empty()
            else:
                st.error("Failed to connect to the server after several attempts.")
                progress_bar.empty()
    else:
        st.write("No image selected")
