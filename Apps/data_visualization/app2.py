from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import numpy as np

app = Flask(__name__)

def create_3d_globe(df, color_scale):
    df_2020 = df[df["Year"] == 2020]
    
    fig = go.Figure(data=go.Choropleth(
        locations=df_2020["Code"],
        z=df_2020["Internet Users(%)"],
        text=df_2020["Entity"],
        colorscale=color_scale,
        colorbar_title="Internet Users (%)"
    ))
    
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True,
        showland=True,
        landcolor="rgb(230, 230, 230)",
        showocean=True,  # Enable ocean display
        oceancolor="rgb(150, 200, 255)"  # Set water color (light blue)
    )
    
    frames = [
        go.Frame(
            layout=dict(
                geo=dict(
                    projection_rotation=dict(lon=lon)
                )
            )
        )
        for lon in np.linspace(0, 360, 180)
    ]
    
    fig.frames = frames
    
    fig.update_layout(
        title="Internet Users Percentage by Country (2020)",
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="Rotate",
                        method="animate",
                        args=[None, dict(frame=dict(duration=5, redraw=True), fromcurrent=True)]
                    )
                ]
            )
        ]
    )
    return fig

@app.route("/", methods=["GET", "POST"])
def index():
    graph_html = None
    if request.method == "POST":
        file = request.files["file"]
        color_scale = request.form.get("color_scale", "reds")
        if file:
            df = pd.read_csv(file)
            fig = create_3d_globe(df, color_scale)
            graph_html = fig.to_html(full_html=False)
    return render_template("index_data.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
