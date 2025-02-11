from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'Apps/data_visualization/static/uploads'
ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_country_columns(df):
    """Detect potential country identifier columns"""
    possible_country_cols = []
    for col in df.columns:
        col_lower = col.lower()
        # Check for common country-related column names
        if any(keyword in col_lower for keyword in ['country', 'code', 'entity', 'nation']):
            possible_country_cols.append(col)
    return possible_country_cols

def detect_time_columns(df):
    """Detect potential time-related columns"""
    time_cols = []
    for col in df.columns:
        col_lower = col.lower()
        # Check for common time-related column names
        if any(keyword in col_lower for keyword in ['year', 'date', 'time', 'period']):
            time_cols.append(col)
        # Check if column contains year-like values
        elif df[col].dtype in ['int64', 'float64']:
            if df[col].nunique() > 1:  # More than one unique value
                sample_values = df[col].dropna().astype(str).str[:4].unique()
                if all(val.isdigit() and 1900 <= int(val) <= 2100 for val in sample_values):
                    time_cols.append(col)
    return time_cols

@app.route('/')
def index():
    return render_template('index_data.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        df = pd.read_csv(filepath)
        columns = df.columns.tolist()
        
        # Detect special columns
        country_columns = detect_country_columns(df)
        time_columns = detect_time_columns(df)
        
        return jsonify({
            'success': True,
            'columns': columns,
            'country_columns': country_columns,
            'time_columns': time_columns,
            'filename': file.filename
        })
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    filename = data.get('filename')
    viz_type = data.get('viz_type')
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filepath)
    
    if viz_type == 'globe':
        country_col = data.get('country_column')
        value_col = data.get('value_column')
        time_col = data.get('time_column')
        time_value = data.get('time_value')
        
        # Filter by time if time column is provided
        if time_col and time_value:
            df_filtered = df[df[time_col] == float(time_value)]
        else:
            df_filtered = df
            
        # Create the choropleth trace
        fig = go.Figure()
        fig.add_trace(go.Choropleth(
            locations=df_filtered[country_col],
            z=df_filtered[value_col],
            text=df_filtered[country_col],  # Use country column for hover text
            colorscale='Viridis',
            zmin=df_filtered[value_col].min(),
            zmax=df_filtered[value_col].max(),
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title=value_col
        ))
        
        # Update the layout for 3D globe
        fig.update_geos(
            projection_type='orthographic',
            showcoastlines=True,
            oceancolor='rgb(0, 102, 204)',
            showocean=True,
            showframe=False
        )
        
        # Add rotation animation
        frames = [
            go.Frame(
                layout=dict(
                    geo=dict(
                        projection_rotation=dict(lon=lon)
                    )
                )
            ) 
            for lon in np.linspace(0, 360, 60)
        ]
        fig.frames = frames
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': 'Rotate Globe',
                    'method': 'animate',
                    'args': [
                        None,
                        {
                            'frame': {'duration': 50, 'redraw': True},
                            'fromcurrent': True,
                            'mode': 'immediate',
                        }
                    ]
                }]
            }],
            height=800
        )
        
        return jsonify({
            'success': True,
            'plot': fig.to_json()
        })
    
    # Handle other visualization types...
    
    return jsonify({'error': 'Invalid visualization type'})

if __name__ == '__main__':
    app.run(debug=True)