import math

import numpy as np
import pyproj as pj

import constants
import functions
import mvp_functions


def theta(r_balloon: np.array, r_object: np.array) -> bool:
    diff = r_balloon - r_object
    dist = vec_length(diff)
    if dist < constants.small_range:
        return True
    return False

def improved_prob_detect(balloons: list[np.array], path: list[tuple[np.array, float]]) -> float:
    """
    The function gets a path and a list of balloons and returns the probability that the object will be detected
    :param balloons: list of balloons
    :param path: the path of the object to be detected
    :return: the probability of the object to be detected
    """
    prob_no_detect = 1
    fixed_path_coordinates = [(functions.gps2ecef(loc[0][1], loc[0][0], 0), loc[1]) for loc in path]
    times = []

    for b in balloons:
        time_in_range = get_time_in_range(b, fixed_path_coordinates)

        if time_in_range > constants.min_time_in_range:
            times.append(time_in_range)

    for t in times:
        prob_no_detect *= (1 - mvp_functions.detection_probability_cu(t))
        print("UAV in range, detection probability:", 100 * mvp_functions.detection_probability_cu(t))
    return 1 - prob_no_detect

def get_time_in_range(balloon: np.array, path: list[tuple[np.array, float]]) -> float:
    """
    Gets a balloon and a path and returns the time in the balloon's range
    :param balloon: coordinates of the balloon
    :param path: list of all the checkpoints in the path and times
    :return: time in the balloon's range
    """
    total_time = 0
    for i in range(len(path) - 1):
        path_in_range_len = find_len_in_sphere(path[i][0], path[i + 1][0], balloon, constants.small_range)
        total_len = vec_length(path[i][0] - path[i + 1][0])
        added_time = (path_in_range_len / total_len) * (path[i][1] - path[i + 1][1])
        total_time += added_time

    return total_time

def find_len_in_sphere(startPoint: np.array, endPoint: np.array, center: np.array, radius: float) -> float:
    """
    The function gets two points and a sphere and returns the distance of the part that is in the sphere of the
    line that starts in one point and ends in another.
    :param startPoint: first point
    :param endPoint: second point
    :param center: coordinates of the center of the sphere
    :param radius: radius of the sphere
    :return: float
    """
    d = endPoint - startPoint  # Direction vector of the segment
    f = startPoint - center  # Vector from sphere center to p1

    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - radius ** 2

    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return 0  # No intersection

    sqrt_discriminant = np.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2 * a)
    t2 = (-b + sqrt_discriminant) / (2 * a)

    # Clamp t values to [0, 1] to stay within the segment
    t_start = max(0, min(1, t1))
    t_end = max(0, min(1, t2))

    if t_start >= t_end:
        return 0  # No segment inside the sphere

    point1 = startPoint + t_start * d
    point2 = startPoint + t_end * d

    return np.linalg.norm(point2 - point1)

def prob_detect(balloons: list[np.array], path: list[tuple[np.array, float]]) -> float:
    prob_no_detect = 1
    times = []
    for b in balloons:
        time_in_range = 0
        for i in range(len(path) - 1):
            point = path[i][0]
            if theta(b, functions.gps2ecef(point[1], point[0], 0)):
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


def gps2utm(lon, lat, alt) -> np.array:
    utm = pj.Proj(proj='utm', zone=36, ellps='WGS84', datum='WGS84')
    lla = pj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    x, y, z = pj.transform(lla, utm, lon, lat, alt, radians=False)
    return np.array([x, y])


def ecef2gps(r: list[float]) -> list[float]:
    ecef = pj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pj.transform(ecef, lla, r[0], r[1], r[2], radians=False)
    return [lon, lat, alt]


def vec_length(vec: np.array) -> float:
    return math.sqrt(sum([x ** 2 for x in vec]))


def cross(a: np.array, b: np.array) -> np.array:
    return np.array([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]])
