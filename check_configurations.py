import os
import warnings

import numpy as np
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

        sum_prob = 0
        normalizer = 0
        for i in range(0, len(os.listdir('paths')), 1):
            with open(f'paths/path{i + 1}.csv') as path:
                df = pd.read_csv(path)
                data = df.values

                print(f"Simulating path {i + 1}...")
                points = [tuple([np.array(data[j][0:-1]), data[j][len(data[j]) - 1]]) for j in range(len(data))]
                prob = 100 * functions.improved_prob_detect(ecef_coords, points)

                start = data[0][0:-1]
                end = data[-1][0:-1]
                p1 = functions.gps2ecef(start[1], start[0], 0)
                p2 = functions.gps2ecef(end[1], end[0], 0)
                dist = functions.vec_length(p2 - p1)
                sum_prob += prob / dist
                print("Balloon array detected UAV, probability: ", prob, '\n')
                normalizer += 1 / dist

        print("Expected configuration detection probability: ", sum_prob / normalizer)
        df = pd.read_csv("configurations/" + config)
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
