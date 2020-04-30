from fdkcc.point import *

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