from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import io

app = Flask(__name__)
model = YOLO('yolov8x.pt')

def draw_label(image, box, class_name, confidence):
    x1, y1, x2, y2 = [int(i) for i in box]
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    label = f"{class_name}: {confidence:.2f}"
    cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


@app.route('/objects', methods=['POST'])
def get_objects():
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
