from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        return jsonify({
            'success': True,
            'columns': columns,
            'filename': file.filename
        })
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/visualize', methods=['POST'])
def visualize():
    print('vis')
    data = request.json
    filename = data.get('filename')
    x_col = data.get('x_column')
    y_col = data.get('y_column')
    viz_type = data.get('viz_type')
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filepath)
    print(df.head())
    fig = None
    
    if viz_type == 'globe':
        # Assuming country codes and values for choropleth
        fig = go.Figure(data=go.Choropleth(
            locations=df[x_col],
            z=df[y_col],
            colorscale='Viridis',
            marker_line_color='darkgray',
            marker_line_width=0.5
        ))
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='orthographic'),
            width=800,
            height=800
        )
        fig.show()
        return jsonify({
            'success': True,
            'plot': fig.to_json()
        })
    
    elif viz_type == 'scatter3d':
        z_col = data.get('z_column')
        fig = px.scatter_3d(
            df, x=x_col, y=y_col, z=z_col,
            color=z_col,
            width=800,
            height=800
        )
    
    elif viz_type == 'line':
        fig = px.line(df, x=x_col, y=y_col, width=800, height=600)
    
    elif viz_type == 'bar':
        fig = px.bar(df, x=x_col, y=y_col, width=800, height=600)
    
    if fig:
        return jsonify({
            'success': True,
            'plot': fig.to_json()
        })
    
    return jsonify({'error': 'Visualization failed'})

if __name__ == '__main__':
    app.run(debug=True)