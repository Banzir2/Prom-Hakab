import os
import warnings

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import constants
import functions

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    radiuses = pd.read_csv("configurations/radiuses").values
    for config in radiuses:
        df = pd.read_csv("configurations/balloons" + str(config[0]) + ".csv")
        print(f"\nTesting configuration - {config[0]} balloons")
        gps_coords = df.values
        ecef_coords = []
        for c in gps_coords:
            ecef_coords.append(functions.gps2ecef(c[1], c[0], constants.max_height))
        for dir in os.listdir('paths'):
            full_path = os.path.join('paths', dir)

            sum_prob = 0
            normalizer = 0
            for i in range(len(os.listdir(full_path)) - 1):
                with open(f'{full_path}/path{i + 1}.csv') as path:
                    df = pd.read_csv(path)
                    data = df.values

                    # print(f"Simulating path {i + 1}...")
                    points = [tuple([np.array(data[j][0:-1]), data[j][len(data[j]) - 1]]) for j in range(len(data))]
                    prob = 100 * functions.improved_prob_detect(ecef_coords, points, config[1])

                    start = data[0][0:-1]
                    end = data[-1][0:-1]
                    p1 = functions.gps2ecef(start[1], start[0], 0)
                    p2 = functions.gps2ecef(end[1], end[0], 0)
                    dist = functions.vec_length(p2 - p1)
                    sum_prob += prob / dist
                    # print("Balloon array detected UAV, probability: ", prob, '\n')
                    normalizer += 1 / dist

            arena_total_prob = sum_prob / normalizer
            print(f"Expected configuration detection probability from {dir}: ", sum_prob / normalizer)
            