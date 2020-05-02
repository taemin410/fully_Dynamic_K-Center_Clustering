import pytest
import os 
import sys

from fdkcc.data_fully_adv import fully_adv_import_points

@pytest.fixture
def create_and_read_file(tmpdir):
    d = tmpdir.mkdir("subdir")

    fo = d.join("inputdata.txt")
    # fo = open(filename)
    fo.write(
"""1504866207	0.37526667 52.26389667
1504866208	121.0352397 14.65166573
1504866208	-61.20515108 -27.21325946
1504866209	101.69062016 3.05276432
1504866209	12.3267 45.4386
1504866209	135.50360024 34.68021892
1504866209	139.75256794 35.65444131
1504866209	139.77624317 35.71330529
1504866209	4.08333 48.3
1504866210	103.854934 1.300463""")

    return fo
    
def test_fully_adv_import_points(tmpdir, create_and_read_file):
    count = 10
    WINDOW_LENGTH = 15
    counter, point_array = fully_adv_import_points(tmpdir+"/subdir/inputdata.txt", WINDOW_LENGTH)

    assert count == counter

    geopointsarr = [(0.37526667 ,52.26389667),
                    (121.0352397 ,14.65166573),
                    (-61.20515108 ,-27.21325946),
                    (101.69062016 ,3.05276432),
                    (12.3267, 45.4386),
                    (135.50360024 ,34.68021892),
                    (139.75256794 ,35.65444131),
                    (139.77624317 ,35.71330529),
                    (4.08333 ,48.3),
                    (103.854934 ,1.300463)]

    for i in range(len(point_array)):
        assert point_array[i].latitude == geopointsarr[i][0]
        assert point_array[i].longitude == geopointsarr[i][1]
    
    assert count == len(point_array)

