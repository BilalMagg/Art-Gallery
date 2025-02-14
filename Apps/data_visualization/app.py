from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import os
from werkzeug.utils import secure_filename

data_bp = Blueprint("visualization", __name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = "Apps/data_visualization/static/uploads"
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@data_bp.route('/', methods=['GET'])
def index():
    return render_template('index_data.html')

@data_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Read CSV and get column information
        df = pd.read_csv(filepath)
        columns = df.columns.tolist()
        country_columns = [col for col in columns if 'country' in col.lower() or 'code' in col.lower()]
        time_columns = [col for col in columns if 'year' in col.lower() or 'date' in col.lower()]
        
        return jsonify({
            "filename": filename,
            "columns": columns,
            "country_columns": country_columns,
            "time_columns": time_columns
        })
    return jsonify({"error": "File type not allowed"}), 400

@data_bp.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    filename = data.get('filename')
    viz_type = data.get('viz_type')
    country_column = data.get('country_column')
    value_column = data.get('value_column')
    time_column = data.get('time_column')
    time_value = data.get('time_value')

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filepath)

    if time_column and time_value:
        df = df[df[time_column] == time_value]

    fig = go.Figure()

    if viz_type == 'globe':
        fig.add_trace(go.Choropleth(
            locations=df[country_column],
            z=df[value_column],
            colorscale='Viridis',
            colorbar_title=value_column,
        ))
        fig.update_layout(
            geo=dict(showland=True, showcountries=True, projection_type='orthographic')
        )
    # Add other visualization types here

    return jsonify({"plot": fig.to_json()})

@data_bp.route('/get_time_values', methods=['POST'])
def get_time_values():
    data = request.json
    filename = data.get('filename')
    time_column = data.get('time_column')

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filepath)

    time_values = df[time_column].unique().tolist()
    return jsonify({"success": True, "time_values": time_values})