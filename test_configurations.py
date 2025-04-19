import math

import plotly.graph_objects as go
import pandas as pd

import constants

if __name__ == '__main__':
    df = pd.read_csv("configurations/balloons1.csv")

    token = "pk.eyJ1IjoiYXRoYXJ2YWthdHJlIiwiYSI6ImNrZ2dkNHQ5MzB2bDUyc2tmZWc2dGx1eXQifQ.lVdNfajC6maADBHqsVrpcg"

    fig = go.Figure(go.Scattermapbox(
        mode="markers+text",
        lon=df['lon'], lat=df['lat'],
        marker={'size': 10, 'symbol': "airport", 'allowoverlap': False, },
        hoverinfo='none'
    ))

    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=df['lon'], lat=df['lat'],
        marker={'size': 200, 'sizemode': 'area',
                'symbol': "circle", 'opacity': 0.3,
                'allowoverlap': True, },
        hoverinfo='skip'))

    fig.update_layout(
        mapbox={
            'accesstoken': token,
            'style': "streets",
            'bearing': 0,
            'pitch': 0,
            'center': {'lat': 31.55, 'lon': 35},
            'zoom': 6.5
        },
        showlegend=False)

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.show()
