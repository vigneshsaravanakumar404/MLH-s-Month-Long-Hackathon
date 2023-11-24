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
    pass
