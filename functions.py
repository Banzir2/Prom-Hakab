import math

import numpy as np
import pyproj as pj

import constants
import mvp_functions


def theta(r_balloon: np.array, r_object: np.array) -> bool:
    diff = r_balloon - r_object
    dist = vec_length(diff)
    if dist < constants.small_range:
        return True
    return False


def prob_detect(balloons: list[np.array], path: list[tuple[np.array, float]]) -> float:
    prob_no_detect = 1
    times = []
    for b in balloons:
        time_in_range = 0
        for i in range(len(path) - 1):
            if theta(b, path[i][0]):
                time_in_range += path[i + 1][1] - path[i][1]
            else:
                if time_in_range > constants.min_time_in_range:
                    times.append(time_in_range)
                time_in_range = 0
        if time_in_range > constants.min_time_in_range:
            times.append(time_in_range)
    for t in times:
        prob_no_detect *= (1 - mvp_functions.detection_probability_cu(t))
        print("UAV in range, detection probability:", 100 * mvp_functions.detection_probability_cu(t))
    return 1 - prob_no_detect


def gps2ecef(lon, lat, alt) -> np.array:
    ecef = pj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    x, y, z = pj.transform(lla, ecef, lon, lat, alt, radians=False)
    return np.array([x, y, z])


def ecef2gps(r: list[float]) -> list[float]:
    ecef = pj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pj.transform(ecef, lla, r[0], r[1], r[2], radians=False)
    return [lon, lat, alt]


def vec_length(vec: np.array) -> float:
    return math.sqrt(sum([x ** 2 for x in vec]))
