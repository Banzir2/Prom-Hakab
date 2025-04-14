import math
import scipy.integrate as it
import numpy as np
import pyproj as pj

import constants
import mvp_functions


def theta(r_balloon: np.array, r_object: np.array) -> bool:
    diff = r_balloon - r_object
    dist = math.sqrt(sum([x**2 for x in diff]))
    if dist < constants.detection_radius:
        return True
    return False


def prob_detect(balloons: list[np.array], path: list[tuple[np.array, float]]) -> float:
    prob_no_detect = 1
    for b in balloons:
        times = []
        time_in_range = 0
        for i in range(len(path) - 1):
            if theta(b, path[i][0]):
                time_in_range += path[i + 1][1] - path[i + 1][0]
            else:
                if time_in_range > constants.min_time_in_range:
                    times.append(time_in_range)
                time_in_range = 0
        if time_in_range > constants.min_time_in_range:
            times.append(time_in_range)
        for t in times:
            prob_no_detect *= (1 - mvp_functions.detection_probability_cu(t))
    return 1 - prob_no_detect


def gps2ecef_pyproj(lat, lon, alt) -> np.array:
    ecef = pj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    x, y, z = pj.transform(lla, ecef, lon, lat, alt, radians=False)
    return np.array([x, y, z])

