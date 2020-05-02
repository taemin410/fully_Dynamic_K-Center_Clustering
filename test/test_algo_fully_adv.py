import pytest
import os 

from fdkcc.algo_fully_adv import * 
from fdkcc.data_fully_adv import *

@pytest.fixture
def create_and_read_file(tmpdir):
    d = tmpdir.mkdir("subdir")

    fo = d.join("inputdata.txt")

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

def test_Fully_adv_cluster_class(tmpdir, create_and_read_file):
    print(tmpdir)
    print(create_and_read_file)
    
    WINDOW_LENGTH = 15
    counter, point_array = fully_adv_import_points(tmpdir+"/subdir/inputdata.txt", WINDOW_LENGTH)
    fullyadvcluster = Fully_adv_cluster(20, 0, point_array, 10, 5)
    assert fullyadvcluster.array == point_array

