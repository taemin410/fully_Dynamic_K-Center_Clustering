import pytest
import os 
from fdkcc.algo_fully_adv import * 
from fdkcc.data_fully_adv import *

TEST_DATA_POINTS = """1504866207	0.37526667 52.26389667
1504866208	121.0352397 14.65166573
1504866208	-61.20515108 -27.21325946
1504866209	101.69062016 3.05276432
1504866209	12.3267 45.4386
1504866209	135.50360024 34.68021892
1504866209	139.75256794 35.65444131
1504866209	139.77624317 35.71330529
1504866209	4.08333 48.3
1504866210	103.854934 1.300463
1504866209	500.0 500.0
1504866210	12.3267 45.4386"""

TEST_LELVELS = []
TEST_EPSILON = 0.1
TEST_D_MIN = 1
TEST_D_MAX = 80

WINDOW_LENGTH = 15
INPUT_k = 10
INPUT_RADIUS = 0
INPUT_NB_POINTS = 12
INPUT_CLUSTER_SIZE = 12

EXPECTED_K = 10
EXPECTED_CENTERS_SIZE = 5
EXPECTED_CLUSTERS_SIZE = 12
EXPECTED_NB_POINTS = 12
EXPECTED_INDEX_OF_DUPLICATE_POINT = 4

@pytest.fixture
def create_and_read_file(tmpdir):
    d = tmpdir.mkdir("subdir")
    fo = d.join("inputdata.txt")
    fo.write(TEST_DATA_POINTS)

    return fo

@pytest.fixture
def import_points(tmpdir, create_and_read_file)->list:
    _, point_array = fully_adv_import_points(tmpdir+"/subdir/inputdata.txt", WINDOW_LENGTH)
    return point_array

@pytest.fixture
def fully_adv_cluster(import_points):
    return Fully_adv_cluster(INPUT_k, INPUT_RADIUS, import_points, INPUT_NB_POINTS, INPUT_CLUSTER_SIZE)

def test_Fully_adv_cluster_class(fully_adv_cluster, import_points):
    assert fully_adv_cluster.array == import_points
    assert len(fully_adv_cluster.array) == EXPECTED_NB_POINTS
    assert fully_adv_cluster.k == EXPECTED_K
    assert len(fully_adv_cluster.centers) == EXPECTED_K+1
    assert len(fully_adv_cluster.clusters.sets) == EXPECTED_K+1

@pytest.fixture
def test_fully_adv_k_center_add(fully_adv_cluster, import_points):
    for i in range(INPUT_NB_POINTS):
        fully_adv_cluster.fully_adv_k_center_add(i)
        
    assert fully_adv_cluster.clusters.sets[EXPECTED_K-1].card == 1
    assert fully_adv_cluster.clusters.sets[0].elm_ptr[EXPECTED_NB_POINTS-2].set_index == EXPECTED_K
    assert fully_adv_cluster.clusters.sets[EXPECTED_INDEX_OF_DUPLICATE_POINT].card == 2

    return fully_adv_cluster

def test_fully_adv_k_center_delete(test_fully_adv_k_center_add, import_points):
    helper_array = []
    remove_result = test_fully_adv_k_center_add.fully_adv_k_center_delete(EXPECTED_NB_POINTS-2, helper_array)

    assert remove_result == False
    assert len(helper_array) == 0
    assert test_fully_adv_k_center_add.clusters.sets[EXPECTED_K].card == 0

    remove_result = test_fully_adv_k_center_add.fully_adv_k_center_delete(EXPECTED_INDEX_OF_DUPLICATE_POINT, helper_array)

    assert remove_result == True
    assert len(helper_array) > 0
    assert test_fully_adv_k_center_add.clusters.sets[EXPECTED_INDEX_OF_DUPLICATE_POINT].card == 1

def test_fully_adv_compute_true_radius(fully_adv_cluster):
    assert fully_adv_cluster.fully_adv_compute_true_radius() == 0

def test_fully_adv_delete_level(fully_adv_cluster):
    fully_adv_cluster.fully_adv_delete_level()

    assert fully_adv_cluster.clusters == None
    assert fully_adv_cluster.centers == None
    assert fully_adv_cluster.true_rad == 0
    assert fully_adv_cluster.centers == None
    assert fully_adv_cluster.nb_points == 0
    assert fully_adv_cluster.array == None




@pytest.fixture
def selective_reclustering(import_points):
    return Fully_adv_cluster_selective_unclustering(INPUT_k, INPUT_RADIUS, import_points, INPUT_NB_POINTS, INPUT_CLUSTER_SIZE)

def test_Fully_adv_cluster_selective_unclustering(selective_reclustering, import_points):
    assert selective_reclustering.array == import_points
    assert len(selective_reclustering.array) == EXPECTED_NB_POINTS
    assert selective_reclustering.k == EXPECTED_K
    assert len(selective_reclustering.centers) == EXPECTED_K+1
    assert len(selective_reclustering.clusters.sets) == EXPECTED_K+1

@pytest.fixture
def test_fully_adv_k_center_add_SR(selective_reclustering, import_points):
    for i in range(INPUT_NB_POINTS):
        selective_reclustering.fully_adv_k_center_add(i)
        
    assert selective_reclustering.clusters.sets[EXPECTED_K-1].card == 1
    assert selective_reclustering.clusters.sets[0].elm_ptr[EXPECTED_NB_POINTS-2].set_index == EXPECTED_K
    assert selective_reclustering.clusters.sets[EXPECTED_INDEX_OF_DUPLICATE_POINT].card == 2

    return selective_reclustering

def test_fully_adv_k_center_delete_SR(test_fully_adv_k_center_add_SR, import_points):
    helper_array = []
    remove_result = test_fully_adv_k_center_add_SR.fully_adv_k_center_delete(EXPECTED_NB_POINTS-2, helper_array)

    assert remove_result == False
    assert len(helper_array) == 0
    assert test_fully_adv_k_center_add_SR.clusters.sets[EXPECTED_K].card == 0

    remove_result = test_fully_adv_k_center_add_SR.fully_adv_k_center_delete(EXPECTED_INDEX_OF_DUPLICATE_POINT, helper_array)

    assert remove_result == True
    assert len(helper_array) > 0
    assert test_fully_adv_k_center_add_SR.clusters.sets[EXPECTED_INDEX_OF_DUPLICATE_POINT].card == 1


def test_initialize_level_array():
    test_strings =["default", "nn", "cache", "selective"]
    nb_instances = 0
    for string in test_strings:
        expected_nb_instances = (1 + ceil( log(TEST_D_MAX / TEST_D_MIN) / log(1 + TEST_EPSILON)))
        nb_instances, helper_arr = fully_adv_initialise_level_array(TEST_LELVELS, INPUT_k, TEST_EPSILON, TEST_D_MIN, TEST_D_MAX, 
                                    nb_instances, import_points, INPUT_NB_POINTS, INPUT_CLUSTER_SIZE, [], string)

        assert nb_instances == expected_nb_instances
        assert len(helper_arr) == 0


    

    
