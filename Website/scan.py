import streamlit as st
import requests
import base64
import json
import time
from PIL import Image
import io
import redis
import json

# TODO: 
# Add information about recycling
# Add logic to add NFT to wallet once image is scanned
# Add logic to limit to 1 per type of item and 10 total recycable items per day
# Add logic to update user profile

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

    for attempt in range(3):
        try:
            response = requests.post(url, data=data, headers=headers)
            return response
        except requests.ConnectionError:
            if attempt < 2:  # Don't show a message on the final attempt
                st.warning("Connection error, retrying...")
            time.sleep(1)
    return None

def retrieve_recycling_information_redis():
    """
    Retrieve recycling information from Redis.

    This function connects to a Redis server and attempts to retrieve the recycling data
    stored under the 'RecyclingData' key.

    Returns:
        dict or None: The recycling data stored in Redis, or None if an error occurs.
    """
    hostname = 'redis-12111.c321.us-east-1-2.ec2.cloud.redislabs.com'
    port = 12111
    password = 'ijNeFVOexsgOvFBn0Q4grGb3OOwXACkZ'
    key = 'RecyclingData'

    # Attempt to retrieve data from Redis
    try:
        return json.loads(redis.Redis(host=hostname, port=port, password=password, ssl=False).get(key))
    except Exception as e:
        return None

def app():
    # Custom CSS to inject
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .info-text {
        font-size:16px;
        color: #4a4a4a;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("♻️ Recycling Scanner")
    st.markdown("""
        <div class='info-text'>
            Welcome to the Recycling Scanner! This tool helps you identify recyclable items 
            using your camera. Simply take a picture, and let the AI do the rest.
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("📃 <span class='big-font'>Instructions</span>", unsafe_allow_html=True)
        st.markdown("""
            <ul>
                <li>Click on 'Take a picture' below.</li>
                <li>Allow camera access if prompted.</li>
                <li>Capture the image of the item you want to check.</li>
                <li>Wait for the AI to analyze the image.</li>
                <li>View the results and recycling information.</li>
                <li>If applicable, add the NFT to your wallet.</li>
            </ul>
        """, unsafe_allow_html=True)
        st.markdown("### Want to Learn More about your NFT?")
        st.caption("If you encounter any issues, visit our your profile page")

    # Camera input
    st.header("📸 Scan Your Item")
    img_file_buffer = st.camera_input(" ")

    if img_file_buffer is not None:
        image_bytes = img_file_buffer.getvalue()

        # Button to send the request
        if st.button("Scan"):
            with st.spinner("Processing..."):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.06)
                    progress_bar.progress(percent_complete + 1)
            
            response = send_image_to_server(image=image_bytes, url='http://localhost:5000/objects')
            
            if response is not None:
                progress_bar.empty()
                response_data = response.json()

                # TODO: Display Success Messages if item is recyclable based on logic
                st.success("Item scanned successfully!")
                st.balloons()
                st.write("You have earned 1 RecycleCoin!")

                # Display class IDs
                class_ids = [obj['class_id'] for obj in response_data['objects']]
                st.write("Class IDs:", class_ids)

                # TODO: Display information about recycling
                st.header("♻️ Recycling Information")
                st.write(retrieve_recycling_information_redis())

                # Display JSON
                st.header("🤖 The Data from our AI")
                st.write(response_data)

                # Display image
                response_image = response_data['image']
                decoded_image = base64.b64decode(response_image)
                image = Image.open(io.BytesIO(decoded_image))
                st.header("📸 The Image We See")
                st.image(image, caption='What we see', use_column_width=True)

                # Save image to Website\Usage History
                image.save('Usage History/' + str(time.time()) + '.jpg')


                # TODO: Add logic to add NFT to wallet once image is scanned
                # Implement logic to limit to 1 per type of item and 10 total recycable items per day
                # Implement logic to update user profile
            else:
                st.error("Failed to connect to the server after several attempts.")
                progress_bar.empty()
    else:
        st.info("Please capture an image using your camera")