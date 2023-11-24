from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import io

# Variables
app = Flask(__name__)
model = YOLO('yolov8x.pt')

# Methods
def draw_label(image, box, class_name, confidence):
    """
    Draws a labeled bounding box on the given image.

    Args:
        image (numpy.ndarray): The image on which to draw the bounding box.
        box (tuple): The coordinates of the bounding box in the format (x1, y1, x2, y2).
        class_name (str): The name of the class associated with the bounding box.
        confidence (float): The confidence score for the detected class.

    Returns:
        None
    """
    x1, y1, x2, y2 = [int(i) for i in box]
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    label = f"{class_name}: {confidence:.2f}"
    cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


@app.route('/objects', methods=['POST'])
def get_objects():
    """
    Endpoint for detecting objects in an image.

    Returns a JSON response containing the detected objects and the processed image.

    Request Body:
    {
        "image": "<base64 encoded image>"
    }

    Response Body:
    {
        "objects": [
            {
                "class_id": "<class id>",
                "confidence": <confidence score>,
                "coordinates": [<x1>, <y1>, <x2>, <y2>]
            },
            ...
        ],
        "image": "<base64 encoded image>"
    }

    Returns:
        - 200 OK: If the objects are successfully detected and the response is generated.
        - 400 Bad Request: If no image is provided or the image is invalid.
    """
    data = request.json
    if 'image' not in data:
        return jsonify({"error": "No image provided"}), 400

    image_data = data['image']
    try:
        objects = []
        image_binary = base64.b64decode(image_data)
        image = np.frombuffer(image_binary, dtype=np.uint8)
        source = cv2.imdecode(image, cv2.IMREAD_COLOR)
        results = model(source)
        result = results[0]
        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            cords = box.xyxy[0].tolist()
            conf = round(box.conf[0].item(), 2)

            draw_label(source, cords, class_id, conf)
            objects.append({"class_id": class_id, "confidence": conf, "coordinates": cords})

        _, buffer = cv2.imencode('.jpg', source)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({"objects": objects, "image": encoded_image}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid image"}), 400
