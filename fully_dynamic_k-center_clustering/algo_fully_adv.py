import point
from set_ import Set_, Set_collection
from query import query, query_provider
from data_fully_adv import fully_adv_distance
from utils import log_, shuffle_array
from math import ceil, log
import static_variables as sv

class Fully_adv_cluster:
    def __init__(self, k, radius, array, nb_points, cluster_size):
        self.nb = 0 # number of cluster
        self.k = k # maximum number of cluster allowed
        self.radius = radius # maximum cluster radius of current level
        self.centers = [None for _ in range(k+1)] # index of center of each cluster
        self.true_rad = [None for _ in range(k)] # exact radius of each cluster
        self.clusters = Set_collection(k+1, cluster_size, nb_points) # content of all clusters (array of sets)
        self.nb_points = nb_points # total number of points in array
        self.array = array # pointer to all points

    def fully_adv_delete_level(self) -> None:
        self.clusters = None
        self.centers = None
        self.true_rad = None
        self.centers = None
        self.nb_points = 0
        self.array = None

    '''
        Add new element to all of clustering environments.

        params:
            index - data_index of next query obj (data_index denotes the random query index from query text)
    '''
    def fully_adv_k_center_add(self, index) -> None:
        for i in range(self.nb):
            tmp = fully_adv_distance(self.array[index], self.array[self.centers[i]])
            if self.radius >= tmp:
                self.clusters.add_element_set_collection(index, i)
                self.true_rad[i] = max(tmp, self.true_rad[i])
                return

        self.clusters.add_element_set_collection(index, self.nb)
        if self.nb < self.k:
            self.centers[self.nb] = index
            self.true_rad[self.nb] = 0
            self.nb += 1

    def fully_adv_k_center_delete(self, element_index, helper_array) -> None:
        size = int()
        cluster_index = self.clusters.get_set_index(element_index)
        self.clusters.remove_element_set_collection(element_index)

        # center of cluster deleted
        if cluster_index < self.k and element_index == self.centers[cluster_index]:
            self.nb = cluster_index
            size = self.clusters.remove_all_elements_after_set(cluster_index, helper_array, size)
            shuffle_array(helper_array, size)
            
            for i in range(size):
                self.fully_adv_k_center_add(helper_array[i])

    def fully_adv_compute_true_radius(self) -> float:
        max_rad = 0
        for i in range(self.nb):
            max_rad = max(max_rad, self.true_rad[i])

        return max_rad

def fully_adv_write_log(levels, nb_instances, nb_points, q) -> int:
    key = 'a' if q.type == "ADD" else 'd'
    if log_.has_log():
        result = fully_adv_get_index_smallest(levels, nb_instances)

        if result == nb_instances:
            print('Error, no feasible radius possible found after inserting', q.data_index)
            return 4 #only_bad_levels_error

        content = 'key: ' + str(key) + ' ' + 'data index: ' + \
            str(q.data_index) + ' ' + 'nb_points: ' + str(nb_points) + ' '\
            'result: ' + str(result) + ' ' + 'radius: ' + str(levels[result].radius) + ' ' + 'true radius: ' + str(levels[result].fully_adv_compute_true_radius()) \
            + '\n'

        if log_.has_long_log():
            f = log_.get_log_file()
            f.write(content)

        else:
            f = log_.get_log_file()
            f.write(content)
    return 0

def fully_adv_apply_one_query(levels, nb_instances, q, helper_array) -> None:
    if q.type == "ADD":
        sv.nb_points += 1

        # add a new data point to all clustering environments
        for i in range(nb_instances):
            levels[i].fully_adv_k_center_add(q.data_index)
    else:
        sv.nb_points -= 1

        # delete a data point from all clustering environments
        for i in range(nb_instances):
            levels[i].fully_adv_k_center_delete(q.data_index, helper_array)

    return fully_adv_write_log(levels, nb_instances, sv.nb_points, q)

def fully_adv_center_run(levels, nb_instances, queries, helper_array) -> None:
    q = query() #query type pointer
    while queries.get_next_query_set(q, levels[0].clusters):
        fully_adv_apply_one_query(levels, nb_instances, q, helper_array)


'''
    Updates the array of clustering environment
        Each element in array represents the clustering which runs as fully adv model.
        This element contains different clusters, which is the group of data points (e.g., geo point).

    params:
        levels - clusters array of Fully_adv_cluster obj
        k - number of cluster
        eps - epsilon
        d_min - minimum distance between two data points
        d_max - maximum distance between two data points
        nb_instances - number of data points
        points - array of Geo Point array
        nb_points - number of data points
        cluster_size - size of the clusters
        helper_array - ??

    return:
        nb_instances - number of dynamic clustering environments
        helper_array - helper array
'''
def fully_adv_initialise_level_array(levels, k, eps, d_min, d_max, nb_instances, points, nb_points, cluster_size, helper_array) -> tuple:
    nb_instances = tmp = (1 + ceil( log(d_max / d_min) / log(1 + eps)))
    helper_array = [None] * nb_points

    # assign new fully adv cluster to each index of array
    levels.append(Fully_adv_cluster(k, 0, points, nb_points, cluster_size))
    for _ in range(1, tmp):
        levels.append(Fully_adv_cluster(k, d_min, points, nb_points, cluster_size))
        d_min = (1 + eps) * d_min

    return nb_instances, helper_array

def fully_adv_delete_level_array(levels, helper_array):
    levels = None
    helper_array = None

def fully_adv_get_index_smallest(levels, nb_instances):
    for i in range(nb_instances):
        if (levels[i].clusters.sets[levels[i].k].card == 0):
            return i

    return nb_instances

def fully_adv_k_center_run(levels, nb_instances, queries, helper_array):
    q = query()
    while queries.get_next_query_set(q, levels[0].clusters):
        fully_adv_apply_one_query(levels, nb_instances, q, helper_array)
