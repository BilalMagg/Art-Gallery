import plotly.graph_objects as go
import numpy as np
import pandas as pd

def graph():
  # Generate data
  x = ["A", "B", "C", "D"]
  y = ["X1", "X2", "X3"]
  z = np.random.randint(1, 10, size=(len(x), len(y)))

  # Create bars
  bars = []
  for i, x_val in enumerate(x):
      for j, y_val in enumerate(y):
          bars.append(go.Bar3d(x=[x_val], y=[y_val], z=[0], dz=[z[i, j]], width=0.4, marker=dict(color=z[i, j], colorscale="Blues")))

  # Create the figure
  fig = go.Figure(data=bars)

  # Set layout
  fig.update_layout(title="3D Bar Chart", scene=dict(xaxis_title="Category", yaxis_title="Subcategory", zaxis_title="Value"))

  fig.show()

def helix():
  # Generate helix data
  t = np.linspace(0, 10, 100)
  x = np.sin(t)
  y = np.cos(t)
  z = t

  # Create the figure
  fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(width=5, color="red"))])

  # Set layout
  fig.update_layout(
      title="3D Helix Curve",
      scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
      updatemenus=[dict(
          type="buttons",
          showactive=False,
          buttons=[dict(
              label="Rotate",
              method="relayout",
              args=[{
                  "scene.camera.eye": {"x": 2.5, "y": 2.5, "z": 2.5}
              }]
          )]
      )]
  )

  # Enable automatic rotation with frames
  fig.update_layout(
      scene_camera=dict(
          up=dict(x=0, y=0, z=1),
          eye=dict(x=2.5, y=2.5, z=2.5)
      ),
      scene=dict(
          xaxis=dict(showgrid=False),
          yaxis=dict(showgrid=False),
          zaxis=dict(showgrid=False)
      ),
      autosize=True,
      title="Rotating 3D Helix",
  )

  fig.show()

# helix()

def earth():
  df = pd.read_csv('Final.csv')
  df_2020 = df[df["Year"] == 2020]
  import plotly.express as px

  # Create the choropleth map
  fig = px.choropleth(
      df_2020,
      locations="Code",  # Country codes
      color="Internet Users(%)",  # Data to visualize
      hover_name="Entity",  # Show country names on hover
      color_continuous_scale="greens",  # Color theme
      title="Internet Users Percentage by Country (2020)"
  )

  # Show the interactive map
  fig.show()

def earth_3D():
    # Load data
    df = pd.read_csv("Final.csv")
    df_2020 = df[df["Year"] == 2020]

    # Create the figure
    fig = go.Figure()

    # Add choropleth layer (Full country area)
    fig.add_trace(
        go.Choropleth(
            locations=df_2020["Code"],  # Country codes
            z=df_2020["Internet Users(%)"],  # Internet users percentage
            text=df_2020["Entity"] + ": " + df_2020["Internet Users(%)"].astype(str) + "%",  
            hoverinfo="text",
            colorscale="reds",
            autocolorscale=False,
            zmin=df_2020["Internet Users(%)"].min(),
            zmax=df_2020["Internet Users(%)"].max(),
            marker_line_color="black",  # Country borders
            colorbar_title="Internet Users (%)",
        )
    )

    # Set up globe layout
    fig.update_geos(
        projection_type="orthographic",  # 3D globe projection
        showcoastlines=True,
        showland=True,
        landcolor="rgb(230, 230, 230)",  # Light gray land
        showocean=True,
        oceancolor="rgb(0, 102, 204)",  # Blue ocean color
    )

    # Create animation frames for rotation
    frames = [
        go.Frame(
            layout=dict(
                geo=dict(
                    projection_rotation=dict(lon=lon)  # Rotate longitude
                )
            )
        )
        for lon in np.linspace(0, 360, 60)  # Rotate in 60 steps
    ]

    # Assign frames to figure
    fig.frames = frames

    # Add rotation button
    fig.update_layout(
        title="Internet Users Percentage by Country (2020)",
        geo=dict(
            showcoastlines=True,
            showland=True,
            showocean=True,
            oceancolor="rgb(0, 102, 204)",
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="Rotate",
                        method="animate",
                        args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)],
                    )
                ],
            )
        ],
    )

    # Show interactive globe
    fig.show()

# Run function
# earth_3D()