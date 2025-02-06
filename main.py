from flask import Flask, render_template

# Import blueprints from each app
# from Apps.paint_tool.app import shapes_bp
# from apps.data_visualization.app import data_bp
from Apps.image_manipulation.appCV import image_bp
# from Apps.audio_manipulation.app import audio_bp
# from apps.machine_learning.app import ml_bp

app = Flask(__name__)

# Register blueprints with URLs
# app.register_blueprint(shapes_bp, url_prefix="/shapes")
# app.register_blueprint(data_bp, url_prefix="/visualization")
app.register_blueprint(image_bp, url_prefix="/images")
# app.register_blueprint(audio_bp, url_prefix="/audio")
# app.register_blueprint(ml_bp, url_prefix="/ml")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
