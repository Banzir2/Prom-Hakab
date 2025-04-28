import math

min_height = 15000  # Meters
max_height = 20000  # Meters
small_range = 60000  # Meters
large_range = 80000  # Meters

earth_radius = 6378000  # Meters

detection_lambda = 0.0333707984492  # 1/Seconds
detection_radius = 56.5 * 1000  # Meters
min_time_in_range = 5  # Seconds

sim_step = 1  # Seconds
uav_speed = 400 / 3.6  # Meters/Seconds
azimuth_rand_range = math.radians(40)  # Radians

dist_between_balloons = 80000  # Meters
