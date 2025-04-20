import math
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib import patches

import constants
import functions
import warnings

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    df = pd.read_csv("configurations/balloons1.csv")

    gps_coords = df.values
    ecef_coords = []
    for c in gps_coords:
        ecef_coords.append(functions.gps2ecef(c[1], c[0], constants.max_height))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    x = [c[0] for c in gps_coords]
    y = [c[1] for c in gps_coords]

    for i in range(len(x)):
        circle = patches.Circle((x[i], y[i]), radius=math.degrees(constants.detection_radius / constants.earth_radius),
                                fill=False, edgecolor='blue')
        ax.add_patch(circle)

    for i in range(len(os.listdir('paths')) - 1):
        with open(f'paths/path{i + 1}.csv') as path:
            df = pd.read_csv(path)
            data = df.values

            for d in data:
                coords = functions.ecef2gps(d)
                x.append(coords[1])
                y.append(coords[0])

            points = [tuple([np.array(data[j][0:-1]), data[j][len(data[j]) - 1]]) for j in range(len(data))]
            print("Balloon array detected UAV, probability: ", 100 * functions.prob_detect(ecef_coords, points), '\n')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_aspect('equal')
    ax.scatter(x, y)

    df = pd.read_csv("configurations/balloons1.csv")
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
    plt.show()
