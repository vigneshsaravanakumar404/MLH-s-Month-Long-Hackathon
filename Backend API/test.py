# Imports
import requests
import base64
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Functions
def encode_image_to_base64(image_path):
    """
    Encodes an image file to base64 format.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded string representation of the image.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def send_image_to_server(image_path, url):
    """
    Sends an image to a server using a POST request.

    Args:
        image_path (str): The path to the image file.
        url (str): The URL of the server to send the image to.

    Returns:
        requests.Response: The response from the server.
    """
    image_base64 = encode_image_to_base64(image_path)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = json.dumps({"image": image_base64})

    response = requests.post(url, data=data, headers=headers)
    return response

def decode_and_show_image(base64_string):
    """
    Decodes a base64 string into an image and displays it using matplotlib.

    Parameters:
    base64_string (str): The base64 encoded string representing the image.

    Returns:
    None
    """
    image_binary = base64.b64decode(base64_string)
    image = np.frombuffer(image_binary, dtype=np.uint8)
    source = cv2.imdecode(image, cv2.IMREAD_COLOR)
    plt.imshow(cv2.cvtColor(source, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


# Variables
image_path = r"C:\Users\Vigne\Downloads\main.jpg"
server_url = 'http://localhost:5000/objects'

# Parse Response
response = send_image_to_server(image_path, server_url)
response_data = response.json()
if "image" in response_data:
    decode_and_show_image(response_data["image"])
else:
    print(response_data)