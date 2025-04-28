import csv
import math
import random

import numpy as np
import pandas as pd

import constants
import functions


def generate_random_path(lst: list, start: np.array, end: np.array, step: float, dist: float):
    if functions.vec_length(end - start) < step:
        new_end = end
    else:
        diff = end - start
        azimuth = math.atan2(diff[1], diff[0])
        azimuth = constants.azimuth_rand_range * (1 - random.random() * 2) + azimuth
        az_vector = np.array([math.cos(azimuth), math.sin(azimuth)])
        az_vector = (az_vector / functions.vec_length(az_vector)) * step
        new_end = start + az_vector

    dist_step = math.degrees((constants.sim_step * constants.uav_speed) / constants.earth_radius)
    diff = new_end - start
    az_vector = (diff / functions.vec_length(diff)) * dist_step
    p = start
    list_length = len(lst)
    for j in range(int(math.floor(functions.vec_length(diff) / dist_step))):
        l = list(p)
        l.append(constants.sim_step * (list_length + j))
        lst.append(l)
        p = p + az_vector
    if functions.vec_length(end - start) < step:
        return
    else:
        generate_random_path(lst, new_end, end, step, dist - step)


if __name__ == '__main__':
    launch_points = pd.read_csv('uav_launch-sites.csv').values
    target_points = pd.read_csv('uav_targets.csv').values

    missions = []
    for l in launch_points:
        for t in target_points:
            missions.append([l, t])

    for i in range(len(missions)):
        points = []
        generate_random_path(points, missions[i][0], missions[i][1], 0.03,
                             functions.vec_length(missions[i][1] - missions[i][0]) * 1.5)

        with open(f'paths/path{i + 1}.csv', 'w', newline='') as pathfile:
            wr = csv.writer(pathfile, quoting=csv.QUOTE_NONE)
            wr.writerow(['lat', 'lon', 'time'])
            wr.writerows(points)
