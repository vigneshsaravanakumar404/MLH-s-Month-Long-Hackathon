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
# Add logic to add NFT to wallet once image is scanned
# Use redis cloud to store user information (tokens, items recycled, limits, profile picture, etc.)
# Add logic to limit to 1 per type of item and 10 total recycable items per day
# Add logic to update user profile

def send_image_to_server(image, url):
    """
    Sends an image to a server using a POST request with retry on failure.

    Args:
        image (bytes): The image data in bytes.
        url (str): The URL of the server to send the image to.

    Returns:
        requests.Response: The response from the server.
    """

    # Send Request
    encoded_string = base64.b64encode(image).decode()
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = json.dumps({"image": encoded_string})

    # Retry on failure
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

    # Custom CSS to inject for a dark-themed website
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
        color: #E8E6E3;  /* Light gray color for better visibility on dark background */
    }
    .info-text {
        font-size:16px;
        color: #D6D3D1;  /* Slightly darker shade of gray for contrast */
    }
    .sidebar .big-font, .sidebar .info-text {
        color: #FFFFFF;  /* White color for text in the sidebar */
    }
    ul {
        color: #E8E6E3;
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
                <li>If applicable, you will get an NFT added to your wallet.</li>
            </ul>
        """, unsafe_allow_html=True)
        st.markdown("### Want to Learn More about your NFT?")
        st.caption("If you encounter any issues, visit our your profile page")

    # Camera input
    st.header("📸 Scan Your Item")
    img_file_buffer = st.camera_input(" ")

    if img_file_buffer is not None:
        image_bytes = img_file_buffer.getvalue()

        # On Scan button click
        if st.button("Scan"):
            with st.spinner("Processing..."):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(percent_complete + 1)
            
            response = send_image_to_server(image=image_bytes, url='http://localhost:5000/objects')
            
            if response is not None:
                
                # Config
                progress_bar.empty()
                response_data = response.json()

                # Display information about recycling
                st.markdown("""
                    <style>
                    .markdown-text-container {
                        font-family: Arial, sans-serif;
                    }
                    .info-header {
                        color: #4CAF50; /* Green color for headers */
                        font-weight: bold;
                    }
                    .info-text {
                        color: #555; /* Dark gray for text */
                    }
                    .expander-header {
                        background-color: #f2f2f2; /* Light gray background for expander headers */
                    }
                    </style>
                    """, unsafe_allow_html=True)
                st.header("♻️ Recycling Information For the Items Detected")
                recycling_info = retrieve_recycling_information_redis()
                objects = [item["class_id"] for item in response_data["objects"]]

                # Filter and Separate Items
                filtered_recycling_info = [item for item in recycling_info if item["item"] in objects]
                recyclable_items = [info for info in filtered_recycling_info if info["isRecyclable"]]
                non_recyclable_items = [info for info in filtered_recycling_info if not info["isRecyclable"]]

                # Display sections for recyclable items
                st.markdown(f"<h4 style='color: #4CAF50;'>Recyclable Items in the Scan</h4>", unsafe_allow_html=True)
                for info in recyclable_items:
                    with st.expander(f"🔍 Recycling Information for {info['item'].title()}", expanded=False):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"<span style='color: #4CAF50;'>🧱 Material Composition:</span>", unsafe_allow_html=True)
                            st.text(info["materialComposition"])
                            
                            st.markdown(f"<span style='color: #FF5722;'>⚠️ Hazardous Components:</span>", unsafe_allow_html=True)
                            st.text(info["hazardousComponents"])
                            
                            st.markdown(f"<span style='color: #00BCD4;'>🌍 Environmental Impact:</span>", unsafe_allow_html=True)
                            st.text(info["environmentalImpact"])
                            
                            st.markdown(f"<span style='color: #9C27B0;'>🔄 Recycling Process:</span>", unsafe_allow_html=True)
                            st.text(info["recyclingProcessDescription"])

                        with col2:
                            st.markdown(f"<span style='color: #3F51B5;'>📋 Sorting Requirements:</span>", unsafe_allow_html=True)
                            st.text(info["sortingRequirements"])
                            
                            st.markdown(f"<span style='color: #E91E63;'>🆙 Upcycling Opportunities:</span>", unsafe_allow_html=True)
                            st.text(info["upcyclingOpportunities"])
                            
                            st.markdown(f"<span style='color: #009688;'>♻️ Preparation for Recycling:</span>", unsafe_allow_html=True)
                            st.text(info["preparationForRecycling"])
                            
                            st.markdown(f"<span style='color: #FF9800;'>🔄 Alternative Disposal Options:</span>", unsafe_allow_html=True)
                            st.text(info["alternativeDisposalOptions"])

                        st.markdown(f"<span style='color: #8BC34A;'>ℹ️ Other Important Info:</span>", unsafe_allow_html=True)
                        st.text(info["otherImportantInfo"])

                        st.markdown(f"<span style='color: #00BCD4;'>⏳ Average Lifespan:</span>", unsafe_allow_html=True)
                        st.text(info["averageLifespan"])

                        st.markdown(f"<span style='color: #FFC107;'>📊 Recycling Rate Statistics:</span>", unsafe_allow_html=True)
                        st.text(info["recyclingRateStatistics"])
                if len(recyclable_items) == 0:
                    st.markdown(f"<span style='color: #FFEB3B;'>No Recyclable Items in the Scan</span>", unsafe_allow_html=True)

                # Display sections for non-recyclable items
                st.markdown(f"<h4 style='color: #ff4d4d;'>Not Recyclable Items in the Scan</h4>", unsafe_allow_html=True)
                for info in non_recyclable_items:
                    with st.expander(f"🔍 Recycling Information for {info['item'].title()}", expanded=False):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"<span style='color: #4CAF50;'>🧱 Material Composition:</span>", unsafe_allow_html=True)
                            st.text(info["materialComposition"])
                            
                            st.markdown(f"<span style='color: #FF5722;'>⚠️ Hazardous Components:</span>", unsafe_allow_html=True)
                            st.text(info["hazardousComponents"])
                            
                            st.markdown(f"<span style='color: #00BCD4;'>🌍 Environmental Impact:</span>", unsafe_allow_html=True)
                            st.text(info["environmentalImpact"])
                            
                            st.markdown(f"<span style='color: #9C27B0;'>🔄 Recycling Process:</span>", unsafe_allow_html=True)
                            st.text(info["recyclingProcessDescription"])

                        with col2:
                            st.markdown(f"<span style='color: #3F51B5;'>📋 Sorting Requirements:</span>", unsafe_allow_html=True)
                            st.text(info["sortingRequirements"])
                            
                            st.markdown(f"<span style='color: #E91E63;'>🆙 Upcycling Opportunities:</span>", unsafe_allow_html=True)
                            st.text(info["upcyclingOpportunities"])
                            
                            st.markdown(f"<span style='color: #009688;'>♻️ Preparation for Recycling:</span>", unsafe_allow_html=True)
                            st.text(info["preparationForRecycling"])
                            
                            st.markdown(f"<span style='color: #FF9800;'>🔄 Alternative Disposal Options:</span>", unsafe_allow_html=True)
                            st.text(info["alternativeDisposalOptions"])

                        st.markdown(f"<span style='color: #8BC34A;'>ℹ️ Other Important Info:</span>", unsafe_allow_html=True)
                        st.text(info["otherImportantInfo"])

                        st.markdown(f"<span style='color: #00BCD4;'>⏳ Average Lifespan:</span>", unsafe_allow_html=True)
                        st.text(info["averageLifespan"])

                        st.markdown(f"<span style='color: #FFC107;'>📊 Recycling Rate Statistics:</span>", unsafe_allow_html=True)
                        st.text(info["recyclingRateStatistics"])
                if len(non_recyclable_items) == 0:
                    st.markdown(f"<span style='color: #FFEB3B;'>No Non-Recyclable Items in the Scan</span>", unsafe_allow_html=True)

                # Display JSON
                st.header("🤖 The Data from our AI")
                st.write(response_data)

                # Display image
                response_image = response_data['image']
                decoded_image = base64.b64decode(response_image)
                image = Image.open(io.BytesIO(decoded_image))
                st.header("📸 The Image We See")
                st.image(image, caption='What we see', use_column_width=True)

                # TODO: Display Success Messages if item is recyclable based on logic
                st.balloons()
                st.write("You have earned 1 RecycleCoin!") 
                image.save('Usage History/' + str(time.time()) + '.jpg')               

            else:

                # Error message
                st.error("Failed to connect to the server after several attempts.")
                progress_bar.empty()
    else:

        # Instructions
        st.info("Please capture an image using your camera")