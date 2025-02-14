from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from werkzeug.utils import secure_filename
import os

data_bp = Blueprint("visualization", __name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = "Apps/data_visualization/static/uploads"
ALLOWED_EXTENSIONS = {'csv'}

# Load Dataset
df = pd.read_csv("Apps/data_visualization/static/data/Final.csv")  # Change to your actual dataset filename

# Filter Data for Year 2020
df_2020 = df[df["Year"] == 2020]

# Function to generate the 3D globe visualization
def create_3d_globe_graph():
    # Prepare data for the 3D globe visualization (we'll use the 'Code' for the country codes)
    locations = df_2020['Code'].tolist()
    internet_users = df_2020['Internet Users(%)'].tolist()  # You can use other data as needed

    # Create a choropleth map on a 3D globe using Plotly
    fig = go.Figure(go.Choropleth(
        locations=locations,
        z=internet_users,
        hoverinfo='location+z',
        colorbar_title="Internet Users (%)",
        colorscale="greens",  # Customize colors if needed
    ))

    # Update the layout to use a 3D globe
    fig.update_geos(
        projection_type="orthographic",  # Orthographic projection for globe effect
        landcolor="rgb(243, 243, 243)",  # Light gray land color
        oceancolor="rgb(0, 123, 255)",  # Blue ocean color
        visible=False  # Hide coastlines and country borders for a cleaner look
    )
    fig.update_layout(
        title="Internet Users (2020) on 3D Globe",
        geo=dict(showland=True, landcolor="rgb(243, 243, 243)", showcoastlines=True,coastlinecolor="black")
    )

    # Return the HTML for the plot
    return fig.to_html(full_html=False)

@data_bp.route('/')
def index():
    graph_html = create_3d_globe_graph()
    return render_template('index_data.html', graph_html=graph_html)