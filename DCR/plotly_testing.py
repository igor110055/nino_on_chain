import plotly.graph_objects as go
from PIL import Image
# Create figure
fig = go.Figure()

# Add trace
fig.add_trace(
    go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
)

# Add images
img = Image.open('DCR\spacewhale_logo.png')
fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing=None,
            opacity=1,
            layer="below")
)

# Set templates
fig.update_layout(template="plotly_white")

fig.show()