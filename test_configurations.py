import math
import os

import numpy as np
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt

import constants
import functions

if __name__ == '__main__':
    df = pd.read_csv("configurations/balloons1.csv")

    gps_coords = df.values
    ecef_coords = []
    for c in gps_coords:
        ecef_coords.append(functions.gps2ecef_pyproj(c[1], c[0], constants.max_height))

    for i in range(len(os.listdir('paths')) - 1):
        with open(f'paths/path{i+1}.csv') as path:
            df = pd.read_csv(path)
            data = df.values
            x = [c[0] for c in ecef_coords]
            y = [c[1] for c in ecef_coords]
            z = [c[2] for c in ecef_coords]
            for d in data:
                x.append(d[0])
                y.append(d[1])
                z.append(d[2])

            # Create 3D scatter plot
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z)

            # Label axes
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')

            points = [tuple([np.array(data[j][0:-1]), data[j][len(data[j])-1]]) for j in range(len(data))]
            print("Balloon array detected UAV, probability: ", 100 * functions.prob_detect(ecef_coords, points), '\n')

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
    plt.show()
