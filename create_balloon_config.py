import csv
import math
import warnings

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import constants
import functions

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    df = pd.read_csv("israel-map.csv")
    interpolates = list(df.values)
    positions = [np.array(interpolates[0])]
    interpolates.append(interpolates[0])
    for i in range(len(interpolates)):
        if i == 0:
            continue
        diff = np.array(interpolates[i]) - np.array(interpolates[i - 1])
        step = math.degrees(500 / constants.earth_radius)
        step_vec = (diff / functions.vec_length(diff)) * step
        pos = np.array(interpolates[i - 1])
        while functions.vec_length(diff) > functions.vec_length(step_vec):
            pos += step_vec
            positions.append(pos.__copy__())
            diff -= step_vec

    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = [p[0] for p in positions]
    y = [p[1] for p in positions]
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_aspect('equal')
    ax.scatter(x, y)
    # plt.show()

    balloon_positions = [np.array(interpolates[0])]
    num_balloons = 0
    i = 0
    balloon_dist = math.degrees(constants.dist_between_balloons / constants.earth_radius)
    while i < len(positions):
        last_balloon = balloon_positions[num_balloons]
        new_position = positions[i]

        if functions.vec_length(new_position - last_balloon) < balloon_dist:
            i += 1
        else:
            balloon_positions.append(positions[i - 1])
            num_balloons += 1

    with open(f'configurations/balloons{len(balloon_positions)}.csv', 'w', newline='') as configfile:
        wr = csv.writer(configfile, quoting=csv.QUOTE_NONE)
        wr.writerow(['lat', 'lon'])
        wr.writerows([list(balloon) for balloon in balloon_positions])
