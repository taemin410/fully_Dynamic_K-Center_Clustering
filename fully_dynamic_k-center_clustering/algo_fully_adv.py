import point
from math import ceil, log

class Fully_adv_cluster:
    def __init__(self, k, radius, array, nb_points, cluster_size):
        self.nb = 0 # number of cluster
        self.k = k # maximum number of cluster allowed
        self.radius = radius # maximum cluster radius of current level
        self.centers = [None] * (k+1) # index of center of each cluster
        self.true_rad = [None] * k  # exact radius of each cluster
        self.clusters = [None] * (k+1) # content of all clusters (array of sets)
        self.nb_points = nb_points # total number of points in array
        self.array = array # pointer to all points

    def fully_adv_delete_level(self) -> None:
        self.clusters = None
        self.centers = None
        self.true_rad = None
        self.centers = None
        self.nb_points = 0
        self.array = None

    def fully_adv_k_center_add(self, index) -> None:
        for i in range(self.nb):
            tmp = fully_adv_distance(self.array[i], self.array[self.centers[i]])

            if self.radius >= tmp:
                add_element_set_collection(self.clusters, index, i)
                self.true_rad[i] = max(tmp, self.true_rad[i])
                return
        
        add_element_set_collection(self.clusters, index, self.nb)
        if self.nb <self.k:
            self.centers[self.nb] = index
            self.true_rad[self.nb] = 0
            self.nb += 1

    # def fully_adv_k_center_delete(self, element_index, helper_array):



def fully_adv_initialise_level_array(levels, k, eps, d_min, d_max, nb_instances, points, nb_points, cluster_size, helper_array) -> None:
    nb_instances = tmp = (1 + ceil( log(d_max / d_min) / log(1 + eps)))
    levels = [None] * tmp
    helper_array = [None] * nb_points

    # assign new fully adv cluster to each index of array
    levels[0] = Fully_adv_cluster(k, 0, points, nb_points, cluster_size)
    for i in range(1, tmp):
        levels[i] = Fully_adv_cluster(k, d_min, points, nb_points, cluster_size)
        d_min = (1 + eps) * d_min

def fully_adv_delete_level_array(levels, helper_array):
    levels = None
    helper_array = None

def fully_adv_get_index_smallest(levels, nb_instances):
    for i in range(nb_instances):
        if (0 == levels[i].clusters.sets[levels[i].k].card): 
            return i

        return nb_instances

# def fully_adv_k_center_add(l)
