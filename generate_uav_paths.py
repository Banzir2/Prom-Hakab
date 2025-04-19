import math

import pandas as pd
import numpy as np
import csv
import constants
import functions

if __name__ == '__main__':
    points = pd.read_csv('paths/points.csv').values
    step_dist = math.degrees((constants.sim_step * constants.karrar_speed) / constants.earth_radius)
    for i in range(int(len(points) / 2)):
        path = []
        p1 = np.array(points[2*i])
        p2 = np.array(points[2*i + 1])
        diff = p2 - p1
        az_vector = (diff / functions.vec_length(diff)) * step_dist
        p = p1
        for j in range(int(math.floor(functions.vec_length(diff) / step_dist))):
            l = functions.gps2ecef_pyproj(p[1], p[0], p[2]).tolist()
            l.append(j * constants.sim_step)
            path.append(l)
            p = p + az_vector
        with open(f'paths/path{i+1}.csv', 'w', newline='') as pathfile:
            wr = csv.writer(pathfile, quoting=csv.QUOTE_NONE)
            wr.writerow(['x', 'y', 'z', 't'])
            wr.writerows(path)
