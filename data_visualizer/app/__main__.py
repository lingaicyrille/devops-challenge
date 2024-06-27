import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import zmq
import struct
import pickle
import numpy as np
import cv2
import os
import base64
import sys


REDACTOR_PORT = os.getenv("REDACTOR_PORT", default="5556")
REDACTOR_HOST = os.getenv("REDACTOR_HOST", default="localhost")  # bind - access all


app = dash.Dash(__name__)

app.layout = html.Div(
    style={"backgroundColor": "black", "maxWidth": "80%", "margin": "0 auto"},
    children=[
        html.H1(
            "Streaming Dynamic Images with Dash",
            style={
                "color": "white",
                "fontFamily": "Arial, sans-serif",
                "fontSize": "32px",
                "textAlign": "center",
            },
        ),
        html.Div(id="image-container"),
        dcc.Interval(
            id="interval-component",
            interval=100,
            n_intervals=0,
        ),
    ],
)

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect(f"tcp://{REDACTOR_HOST}:{REDACTOR_PORT}")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
print("connection complete")

image = None


def generate_image():
    width, height = 400, 400
    image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    return image


@app.callback(
    Output("image-container", "children"), Input("interval-component", "n_intervals")
)
def update_graph(n_intervals):
    global image
    global subscriber

    while subscriber.poll(0):
        data = subscriber.recv()
        width, height = struct.unpack(">QQ", data[0:16])
        image = pickle.loads(data[16:])

    if image is None:
        image = generate_image()

    _, image_encoded = cv2.imencode(".jpg", image)
    image_base64 = base64.b64encode(image_encoded.tobytes()).decode()

    image_html = html.Img(
        src="data:image/jpg;base64," + image_base64,
        style={"width": "100%", "height": "auto"},
    )

    return image_html


if __name__ == "__main__":
    print("data_visualizer started.")
    app.run_server(host="0.0.0.0", debug=False)
