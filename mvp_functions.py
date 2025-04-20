import math

import constants as c


def detection_probability_cu(time: float) -> float:
    return 1 - math.exp(-c.detection_lambda * time)


def area_cut_circle(r: float, y_max: float) -> float:
    r2 = r ** 2
    a = math.sqrt(r2 - y_max ** 2)
    return y_max * a + r2 * math.atan(y_max / a)


def expected_time(v: float, r: float, t_min: float) -> float:
    y_max = math.sqrt(r ** 2 - (v * t_min / 2) ** 2)
    return (1 / (v * r)) * area_cut_circle(r, y_max)


def prob_detection(v: float, r: float, t_min: float) -> float:
    return detection_probability_cu(expected_time(v, r, t_min))
