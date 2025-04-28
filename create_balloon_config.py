import math
import warnings

import numpy as np
import pandas as pd

import constants
import functions

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    df = pd.read_csv("balloon_interpolates.csv")
    interpolates = list(df.values)
    positions = [np.array(interpolates[0])]
    interpolates.append(interpolates[0])
    for i in range(len(interpolates)):
        if i == 0:
            continue
        diff = np.array(interpolates[i]) - np.array(interpolates[i-1])
        step = math.degrees(500 / constants.earth_radius)
        step_vec = (diff / functions.vec_length(diff)) * step
        pos = np.array(interpolates[i-1])
        while functions.vec_length(diff) > functions.vec_length(step_vec):
            pos += step_vec
            positions.append(pos)
            diff -= step_vec

