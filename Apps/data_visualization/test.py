# import plotly.graph_objects as go
# import numpy as np

# # Generate data
# x = ["A", "B", "C", "D"]
# y = ["X1", "X2", "X3"]
# z = np.random.randint(1, 10, size=(len(x), len(y)))

# # Create bars
# bars = []
# for i, x_val in enumerate(x):
#     for j, y_val in enumerate(y):
#         bars.append(go.Bar3d(x=[x_val], y=[y_val], z=[0], dz=[z[i, j]], width=0.4, marker=dict(color=z[i, j], colorscale="Blues")))

# # Create the figure
# fig = go.Figure(data=bars)

# # Set layout
# fig.update_layout(title="3D Bar Chart", scene=dict(xaxis_title="Category", yaxis_title="Subcategory", zaxis_title="Value"))

# fig.show()

import plotly.graph_objects as go
import numpy as np

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