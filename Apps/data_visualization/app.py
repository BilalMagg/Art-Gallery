# import pandas as pd

# df = pd.read_csv('Final.csv')
# df_2020 = df[df["Year"] == 2020]
# import plotly.express as px

# # Create the choropleth map
# fig = px.choropleth(
#     df_2020,
#     locations="Code",  # Country codes
#     color="Internet Users(%)",  # Data to visualize
#     hover_name="Entity",  # Show country names on hover
#     color_continuous_scale="greens",  # Color theme
#     title="Internet Users Percentage by Country (2020)"
# )

# # Show the interactive map
# fig.show()

import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load data
df = pd.read_csv("Final.csv")
df_2020 = df[df["Year"] == 2020]

# Create the figure
fig = go.Figure()

# Add data points (Country locations)
fig.add_trace(
    go.Scattergeo(
        locations=df_2020["Code"],  # Country codes
        text=df_2020["Entity"] + ": " + df_2020["Internet Users(%)"].astype(str) + "%",
        hoverinfo="text",
        marker=dict(
            size=8,
            color=df_2020["Internet Users(%)"],  # Color based on Internet Users %
            colorscale="greens",
            cmin=df_2020["Internet Users(%)"].min(),
            cmax=df_2020["Internet Users(%)"].max(),
            colorbar_title="Internet Users (%)",
        ),
    )
)

# Set up globe layout
fig.update_geos(
    projection_type="orthographic",  # 3D globe projection
    showcoastlines=True,
    showland=True,
    landcolor="rgb(230, 230, 230)",  # Light gray land
)

# Create animation frames for rotating effect
frames = [
    go.Frame(
        layout=dict(
            geo=dict(
                projection_rotation=dict(lon=lon)
            )
        )
    )
    for lon in np.linspace(0, 360, 60)  # Rotate in 60 steps
]

# Assign frames (Important fix)
fig.frames = frames

# Update layout (without frames inside)
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
