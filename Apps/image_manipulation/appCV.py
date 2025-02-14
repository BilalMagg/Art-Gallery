from flask import Flask, render_template, request, redirect, url_for, send_file, Blueprint, jsonify
import os,sys
import cv2
# sys.path.append(os.path.abspath('../openCV'))
from .openCV import grayscale, blur, edge_detection,pixelation,cartoon,oil_painting,emboss,invert,sepia
import numpy as np

# app = Flask(__name__)
image_bp = Blueprint("images", __name__, template_folder="templates",static_folder="static")

os.makedirs('Apps/image_manipulation/static/images',exist_ok= True)
os.makedirs('Apps/image_manipulation/static/filtered',exist_ok= True)

@image_bp.route('/')
def index():
  return render_template('indexCV.html')

@image_bp.route('/upload_image',methods=['POST'])
def upload_image():
  if 'image' in request.files:
        img_file = request.files['image']
        if img_file:
            file_path = os.path.join('Apps/image_manipulation/static/images', img_file.filename)
            img_file.save(file_path)
            return redirect(url_for('images.show_image', filename=img_file.filename))
  return redirect(url_for('index'))

@image_bp.route('/image/<filename>')
def show_image(filename):
  return render_template('show_imageCV.html',filename = filename)

@image_bp.route('/apply_filter/<filter_type>/<filename>')
def apply_filter(filter_type,filename):
    input_path = os.path.join('Apps/image_manipulation/static/images',filename)
    output_path = os.path.join('Apps/image_manipulation/static/filtered',f"{filter_type}_{filename}")

    if not os.path.exists(input_path):
        return "File Not Found!!",404
    
    img = cv2.imread(input_path)
    if filter_type == "grayscale":
        img = grayscale(img)
    elif filter_type == "blur":
        img = blur(img)
    elif filter_type == "edge detection":
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

    return render_template('show_imageCV.html',filename=filename,filtered_filename=f"{filter_type}_{filename}")

@image_bp.route('/download/<filename>')
def download_img(filename):
    file_path = os.path.join('Apps/image_manipulation/static/filtered',filename)
    print (file_path)

    if not os.path.exists(file_path):
        print('Not found')
        return "File Not Found !!",404
    
    return send_file(file_path, as_attachment = True)

@image_bp.route('/add_to_gallery', methods=['POST'])
def add_to_gallery():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"message": "No filename provided"}), 400

    src_path = os.path.join('Apps/image_manipulation/static/filtered', filename)
    dest_folder = "static/gallery"
    os.makedirs(dest_folder, exist_ok=True)  # Ensure gallery folder exists

    # Check if file already exists in the gallery
    dest_path = os.path.join(dest_folder, filename)
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = f"{base}_{counter}{ext}"
        new_dest_path = os.path.join(dest_folder, new_filename)

        # Keep incrementing until we find a unique filename
        while os.path.exists(new_dest_path):
            counter += 1
            new_filename = f"{base}_{counter}{ext}"
            new_dest_path = os.path.join(dest_folder, new_filename)

        dest_path = new_dest_path  # Use the new unique filename

    # Move the file
    try:
        os.rename(src_path, dest_path)  # Move file to the gallery
        return jsonify({"message": f"Image added to gallery as {os.path.basename(dest_path)}!"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# if __name__ == "__main__":
#     image_bp.run(debug=True)