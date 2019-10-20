from math import acos, sin, cos, sqrt

M_PI = 3.14159265358979323846

class Geo_point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Timestamped_point:
    def __init__(self, geo_point):
        self.in_date = 0.0
        self.exp_date = 0.0
        self.geo_point = geo_point

def euclidean_distance(a, b) -> float:
    return sqrt((a.latitude - b.latitude) ** 2 + ( min( abs(a.latitude - b.latitude), 360 - abs(a.longitude - b.longitude)) ) ** 2)

def great_circle_distance(a, b) -> float:
    return acos( sin(a.latitude) * sin(b.latitude) + cos(a.latitude) * cos(b.latitude) * cos(a.longitude - b.longitude) )

def translate_coordinates_radian(point) -> None:
    point.latitude = point.latitude * M_PI / 180
    point.longitude = point.longitude * M_PI / 180
