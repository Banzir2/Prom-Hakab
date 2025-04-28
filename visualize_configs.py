import os
import warnings

import pandas as pd
import plotly.graph_objects as go

import constants
import functions

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    for config in os.listdir("configurations"):
        df = pd.read_csv("configurations/" + config)

        gps_coords = df.values
        ecef_coords = []
        for c in gps_coords:
            ecef_coords.append(functions.gps2ecef(c[1], c[0], constants.max_height))

        token = "pk.eyJ1IjoiYXRoYXJ2YWthdHJlIiwiYSI6ImNrZ2dkNHQ5MzB2bDUyc2tmZWc2dGx1eXQifQ.lVdNfajC6maADBHqsVrpcg"
        map_plot = go.Figure(go.Scattermapbox(
            mode="markers+text",
            lon=df['lon'], lat=df['lat'],
            marker={'size': 10, 'symbol': "airport", 'allowoverlap': False, },
            hoverinfo='none'
        ))
        map_plot.add_trace(go.Scattermapbox(
            mode="markers",
            lon=df['lon'], lat=df['lat'],
            marker={'size': 150, 'sizemode': 'area',
                    'symbol': "circle", 'opacity': 0.3,
                    'allowoverlap': True, },
            hoverinfo='skip'))
        map_plot.update_layout(
            mapbox={
                'accesstoken': token,
                'style': "streets",
                'bearing': 0,
                'pitch': 0,
                'center': {'lat': 31.55, 'lon': 35},
                'zoom': 6.5
            },
            showlegend=False)
        map_plot.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        map_plot.show()
