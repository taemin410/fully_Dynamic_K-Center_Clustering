from fdkcc.point import *
from math import acos, sin, cos, sqrt 

def test_Geo_point():

    geopnt = Geo_point(111.111, -133.133)

    assert geopnt.latitude ==  111.111
    assert geopnt.longitude == -133.133


def test_Timestamped_point():
    geopnt = Geo_point(111.111, -133.133)
    timestamppnt = Timestamped_point(153312, 154432, geopnt)

    assert timestamppnt.in_date == 153312
    assert timestamppnt.exp_date == 154432


def test_euclidean_distance():
    a = 3
    b = 4 
    geo_a = Geo_point(0,0)
    geo_b = Geo_point(a,b)
    c = euclidean_distance(geo_a,geo_b)
    assert c == 5
    
def test_great_circle_distance():

    point_a = (-10 , 10)
    point_b = (112, -23)
    result = acos(sin(point_a[0]) * sin(point_b[0]) + cos(point_a[0]) * cos(point_b[0]) * cos(point_a[1]- point_b[1]) )
    assert result == 2.070421812123227

    geo_a = Geo_point(-10 , 10)
    geo_b = Geo_point(112, -23)
    assert great_circle_distance(geo_a, geo_b) == 2.070421812123227


def test_translate_coordinates_radian():

    translate = lambda x : x * M_PI / 180
    latitude_in_radian = translate(-45)
    longitude_in_radian = translate(60)

    point = Geo_point(-45 , 60)
    translate_coordinates_radian(point)

    assert latitude_in_radian == point.latitude
    assert longitude_in_radian == point.longitude

    