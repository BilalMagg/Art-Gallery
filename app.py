from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image, ImageFilter

app = Flask(__name__)

os.makedirs('static/images', exist_ok=True)
os.makedirs('static/filtered', exist_ok=True)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/upload_image', methods = ['POST'])
def upload_image():
  if 'image' in request.files:
    img_file = request.files['image']
    if img_file:
      file_path = os.path.join('static/images', img_file.filename)
      img_file.save(file_path)
      return redirect(url_for('show_image',filename = img_file.filename))
  return redirect(url_for('index'))

@app.route('/image/<filename>')
def show_image(filename):
  return render_template('show_image.html',filename = filename)

@app.route('/apply_filter/<filter_type>/<filename>')
def apply_filter(filter_type,filename):
  input_path = os.path.join('static/images',filename)
  output_path = os.path.join('static/filtered',f"{filter_type}_{filename}")

  if not os.path.exists(input_path):
    return "File not found", 404
  
  img = Image.open(input_path)

  if filter_type == "grayscale":
    img = img.convert("L")
  elif filter_type == "blur":
    img = img.filter(ImageFilter.BLUR)
  elif filter_type == "pixelate":
    img = img.resize((img.width // 10, img.height // 10), Image.NEAREST)
    img = img.resize((img.width * 10, img.height * 10), Image.NEAREST)

  img.save(output_path)

  return render_template('show_image.html',filename = filename,filtered_filename = f"filtered/{filter_type}_{filename}")

if __name__ == '__main__':
  app.run(debug=True)