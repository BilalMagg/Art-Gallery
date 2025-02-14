from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from werkzeug.utils import secure_filename
import os

data_bp = Blueprint("visualization", __name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = "Apps/data_visualization/static/uploads"
ALLOWED_EXTENSIONS = {'csv'}

# Load preset data
PRESET_DATA = pd.read_csv("Apps\data_visualization\static\data\Final.csv")
AVAILABLE_YEARS = sorted(PRESET_DATA['Year'].unique().tolist())

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@data_bp.route('/', methods=['GET'])
def index():
    return render_template('index_data.html')

@data_bp.route('/get_preset_years', methods=['GET'])
def get_preset_years():
    return jsonify({"years": AVAILABLE_YEARS})

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
        
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        
        return jsonify({
            "filename": filename,
            "columns": columns,
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns
        })
    
    return jsonify({"error": "File type not allowed"}), 400

@data_bp.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    viz_type = data.get('viz_type')
    data_source = data.get('data_source')
    
    if data_source == 'preset':
        year = int(data.get('year'))
        metric = data.get('metric', 'internet')
        df = PRESET_DATA[PRESET_DATA['Year'] == year]
        
        if viz_type == 'globe':
            metric_map = {
                'internet': 'Internet Users(%)',
                'cellular': 'Cellular Subscription',
                'broadband': 'Broadband Subscription'
            }
            metric_col = metric_map[metric]
            
            fig = go.Figure(data=go.Choropleth(
                locations=df['Code'],
                z=df[metric_col],
                text=df['Entity'],
                colorscale='Viridis',
                colorbar_title=metric_col
            ))
            fig.update_layout(
                geo=dict(showland=True, showcountries=True, projection_type='orthographic'),
                title=f"{metric_col} by Country ({year})"
            )
            
        elif viz_type == 'bar':
            metric_col = 'Internet Users(%)' if metric == 'internet' else metric
            df_sorted = df.nlargest(10, metric_col)
            fig = px.bar(
                df_sorted,
                x='Entity',
                y=metric_col,
                title=f"Top 10 Countries by {metric_col} ({year})"
            )
            
        elif viz_type == 'line':
            # For line chart, we'll use all years
            df_line = PRESET_DATA.copy()
            fig = px.line(
                df_line,
                x='Year',
                y='Internet Users(%)',
                color='Entity',
                title='Internet Usage Trends Over Time'
            )
            
        elif viz_type == 'scatter':
            fig = px.scatter(
                df,
                x='Cellular Subscription',
                y='Internet Users(%)',
                text='Entity',
                title=f'Internet vs Cellular Usage ({year})'
            )
            
    else:  # Custom upload
        filename = data.get('filename')
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df = pd.read_csv(filepath)
        
        if viz_type == 'bar':
            fig = px.bar(
                df,
                x=data['x_column'],
                y=data['y_column'],
                color=data.get('color_column'),
                title=f"Bar Chart of {data['y_column']} by {data['x_column']}"
            )
        # Add other visualization types for custom uploads as needed
    
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return jsonify({"plot": fig.to_json()})