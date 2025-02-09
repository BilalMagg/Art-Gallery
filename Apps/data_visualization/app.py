from flask import Flask, render_template, request, Blueprint
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# app = Flask(__name__)
data_bp = Blueprint("visualization",__name__,template_folder="templates",static_folder="static")

UPLOAD_FOLDER = "Apps/data_visualization/static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# data_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@data_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index_data.html')

@data_bp.route('/visualize', methods=['POST'])
def visualize():
    file = request.files['file']
    color_scale = request.form['color_scale']
    graph_type = request.form['graph_type']
    
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        df = pd.read_csv(file_path)
        df_2020 = df[df["Year"] == 2020]
        
        fig = go.Figure()
        if graph_type == "globe":
            fig.add_trace(go.Choropleth(
                locations=df_2020["Code"],
                z=df_2020["Internet Users(%)"],
                text=df_2020["Entity"],
                colorscale=color_scale,
                zmin=df_2020["Internet Users(%)"].min(),
                zmax=df_2020["Internet Users(%)"].max(),
                marker_line_color="black",
                colorbar_title="Internet Users (%)",
            ))
            fig.update_geos(projection_type="orthographic", showcoastlines=True, oceancolor="rgb(0, 102, 204)")
            frames = [go.Frame(layout=dict(geo=dict(projection_rotation=dict(lon=lon)))) for lon in np.linspace(0, 360, 60)]
            fig.frames = frames
            fig.update_layout(
                updatemenus=[dict(type="buttons", buttons=[dict(label="Rotate", method="animate", args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)] ) ])]
            )
        
        graph_html = fig.to_html(full_html=False)
        return render_template('graph.html', graph_html=graph_html)
    
    return "Error processing file."

# if __name__ == '__main__':
#     app.run(debug=True)
