import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow_hub as hub
from flask import Flask, render_template, request, Blueprint
import os

def load_and_process_image(image_path, max_dim=512):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    scale = max_dim / max(h, w)
    img = cv2.resize(img, (int(w * scale), int(h * scale)))
    img = np.expand_dims(img, axis=0).astype('float32') / 255.0
    return img

def style_transfer(content_path, style_path):
    content_img = load_and_process_image(content_path)
    style_img = load_and_process_image(style_path)
    
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    stylized_image = model(tf.constant(content_img), tf.constant(style_img))[0] * 1.2

    
    output = np.squeeze(stylized_image.numpy()) * 255
    output = np.clip(output, 0, 255).astype('uint8')
    output_path = 'Apps/ML/static/output.jpg'
    cv2.imwrite(output_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
    return output_path

# app = Flask(__name__)
ml_bp = Blueprint("ml",__name__,template_folder="templates",static_folder="static")
UPLOAD_FOLDER = 'Apps/ML/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@ml_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        content_file = request.files['content_image']
        style_file = request.files['style_image']
        
        if content_file and style_file:
            content_path = os.path.join(UPLOAD_FOLDER, content_file.filename)
            style_path = os.path.join(UPLOAD_FOLDER, style_file.filename)
            content_file.save(content_path)
            style_file.save(style_path)
            
            output_path = style_transfer(content_path, style_path)
            return f'<h1>Style Transfer Complete!</h1><img src="/{output_path}" width="512">'
    
    return render_template("index_ml.html")

# if __name__ == '__main__':
#     app.run(debug=True)
