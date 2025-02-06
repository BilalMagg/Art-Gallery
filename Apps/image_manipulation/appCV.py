from flask import Flask, render_template, request, redirect, url_for, send_file
import os,sys
import cv2
# sys.path.append(os.path.abspath('../openCV'))
from openCV import grayscale, blur, edge_detection,pixelation,cartoon,oil_painting,emboss,invert,sepia
import numpy as np

app = Flask(__name__)

os.makedirs('static/images',exist_ok= True)
os.makedirs('static/filtered',exist_ok= True)

@app.route('/')
def index():
  return render_template('indexCV.html')

@app.route('/upload_image',methods=['POST'])
def upload_image():
  if 'image' in request.files:
        img_file = request.files['image']
        if img_file:
            file_path = os.path.join('static/images', img_file.filename)
            img_file.save(file_path)
            return redirect(url_for('show_image', filename=img_file.filename))
  return redirect(url_for('index'))

@app.route('/image/<filename>')
def show_image(filename):
  return render_template('show_imageCV.html',filename = filename)

@app.route('/apply_filter/<filter_type>/<filename>')
def apply_filter(filter_type,filename):
    input_path = os.path.join('static/images',filename)
    output_path = os.path.join('static/filtered',f"{filter_type}_{filename}")

    if not os.path.exists(input_path):
        return "File Not Found!!",404
    
    img = cv2.imread(input_path)
    if filter_type == "grayscale":
        img = grayscale(img)
    elif filter_type == "blur":
        img = blur(img)
    elif filter_type == "edge":
        img = edge_detection(img,[100,200])
    elif filter_type == "pixelate":
        img = pixelation(img)
    elif filter_type == "cartoon":
        img = cartoon(img)
    elif filter_type == "oil painting":
        img = oil_painting(img)
    elif filter_type == "emboss":
        img = emboss(img)
    elif filter_type == "invert":
        img = invert(img)
    elif filter_type == "sepia":
        img = sepia(img)
    else :
        return "Invalid filter",400
    cv2.imwrite(output_path,img)

    return render_template('show_imageCV.html',filename=filename,filtered_filename=f"filtered/{filter_type}_{filename}")

@app.route('/download/<filename>')
def download_img(filename):
    file_path = os.path.join('static/filtered',filename)

    if not os.path.exists(file_path):
        return "File Not Found !!",404
    
    return send_file(file_path, as_attachment = True)

if __name__ == "__main__":
    app.run(debug=True)