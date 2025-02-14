from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from werkzeug.utils import secure_filename
import os

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
        
        df = pd.read_csv(filepath)
        columns = df.columns.tolist()
        
        # Detect numeric columns for various visualizations
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        # Detect categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        
        # Detect date columns
        date_columns = [col for col in columns if 'date' in col.lower() or 'year' in col.lower()]
        
        # Detect location columns
        location_columns = [col for col in columns if 'country' in col.lower() or 
                          'city' in col.lower() or 'location' in col.lower() or 
                          'code' in col.lower()]
        
        return jsonify({
            "filename": filename,
            "columns": columns,
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "date_columns": date_columns,
            "location_columns": location_columns
        })
    
    return jsonify({"error": "File type not allowed"}), 400

@data_bp.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    filename = data.get('filename')
    viz_type = data.get('viz_type')
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filepath)
    
    fig = go.Figure()
    
    try:
        if viz_type == 'globe':
            fig.add_trace(go.Choropleth(
                locations=df[data['location_column']],
                z=df[data['value_column']],
                colorscale='Viridis',
                colorbar_title=data['value_column']
            ))
            fig.update_layout(
                geo=dict(showland=True, showcountries=True, projection_type='orthographic'),
                title=f"Global Distribution of {data['value_column']}"
            )
            
        elif viz_type == 'bar':
            fig = px.bar(
                df,
                x=data['x_column'],
                y=data['y_column'],
                color=data.get('color_column'),
                title=f"Bar Chart of {data['y_column']} by {data['x_column']}"
            )
            
        elif viz_type == 'line':
            fig = px.line(
                df,
                x=data['x_column'],
                y=data['y_column'],
                color=data.get('color_column'),
                title=f"Line Chart of {data['y_column']} over {data['x_column']}"
            )
            
        elif viz_type == 'scatter3d':
            fig = px.scatter_3d(
                df,
                x=data['x_column'],
                y=data['y_column'],
                z=data['z_column'],
                color=data.get('color_column'),
                title=f"3D Scatter Plot"
            )
            
        elif viz_type == 'box':
            fig = px.box(
                df,
                x=data['category_column'],
                y=data['value_column'],
                title=f"Box Plot of {data['value_column']} by {data['category_column']}"
            )
            
        elif viz_type == 'histogram':
            fig = px.histogram(
                df,
                x=data['value_column'],
                nbins=30,
                title=f"Histogram of {data['value_column']}"
            )
            
        elif viz_type == 'heatmap':
            pivot_table = pd.pivot_table(
                df,
                values=data['value_column'],
                index=data['y_column'],
                columns=data['x_column']
            )
            fig = px.imshow(
                pivot_table,
                title=f"Heatmap of {data['value_column']}"
            )
        
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return jsonify({"plot": fig.to_json()})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@data_bp.route('/get_time_values', methods=['POST'])
def get_time_values():
    data = request.json
    filename = data.get('filename')
    time_column = data.get('time_column')
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filepath)
    
    time_values = sorted(df[time_column].unique().tolist())
    return jsonify({"success": True, "time_values": time_values})