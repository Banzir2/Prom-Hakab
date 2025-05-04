import csv
import math
import os
import random

import numpy as np
import pandas as pd

import constants
import functions


def generate_random_uav_path(lst: list, start: np.array, end: np.array, cur_time: float, step: float, dist: float):
    """
    The function gets a starting point and an end and returns a path
    :param lst: a list in which the path is written to
    :param start: starting point
    :param end: ending point
    :param cur_time: the time of the starting point
    :param step: the length of one step
    :param dist: the total distance of the path
    :return: None
    """
    if functions.vec_length(end - start) < step:
        new_end = end
    else:
        diff = end - start
        azimuth = math.atan2(diff[1], diff[0])
        azimuth = constants.azimuth_rand_range * (1 - random.random() * 2) + azimuth
        az_vector = np.array([math.cos(azimuth), math.sin(azimuth)])
        az_vector = (az_vector / functions.vec_length(az_vector)) * step
        new_end = start + az_vector

    diff = new_end - start
    lap_len = math.radians(functions.vec_length(diff)) * constants.earth_radius
    lap_time = lap_len / constants.uav_speed

    lst.append(list(start) + [cur_time])

    if functions.vec_length(end - start) < step:
        lst.append(list(end) + [cur_time + lap_time])
        return
    else:
        generate_random_uav_path(lst, new_end, end, cur_time + lap_time, step, dist - step)


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


def generate_paths(launch_sites_csv: str, targets_csv: str, data_loc: str):
    """
    The function gets csv files for launch sites and targets and generates paths
    :param launch_sites_csv: the name of the launch sites csv file
    :param targets_csv: the name of the targets csv file
    :param data_loc: the location of the result
    :return: None
    """
    launch_points = pd.read_csv(launch_sites_csv).values
    target_points = pd.read_csv(targets_csv).values

    missions = []
    for l in launch_points:
        for t in target_points:
            missions.append([l, t])

    for i in range(len(missions)):
        points = []
        generate_random_uav_path(points, missions[i][0], missions[i][1], 0, 0.03,
                                 functions.vec_length(missions[i][1] - missions[i][0]) * 1.5)

        with open(f'{data_loc}/path{i + 1}.csv', 'w', newline='') as pathfile:
            wr = csv.writer(pathfile)
            wr.writerow(['lat', 'lon', 'time'])
            wr.writerows(points)


if __name__ == '__main__':
    arenas_names = []
    for arena in os.listdir("launch_sites"):
        arenas_names.append(arena[:-4])

    for arena in arenas_names:
        launch_sites_csv = "launch_sites/" + arena + ".csv"
        targets_csv = "targets/" + arena + ".csv"
        data_loc = "paths/" + arena
        generate_paths(launch_sites_csv, targets_csv, data_loc)
