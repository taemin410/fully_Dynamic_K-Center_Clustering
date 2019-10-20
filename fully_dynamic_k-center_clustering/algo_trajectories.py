from set_ import Set_collection
from math import ceil, log
from utils import log_

class Trajectory_level:
    def __init__(self, k, radius, array, nb_points):
        self.nb = 0
        self.k = k
        self.radius = radius
        self.centers = [] # integer array
        self.true_rad = [None] * k
        self.max_trajectories_nb = nb_points
        self.current_trajectories_nb = 0
        self.trajectories = array
        self.clusters = Set_collection(k+1, nb_points, nb_points)

    def trajectories_delete_level(self) -> None:
        self.clusters.free_set_collection()
        self.centers = []
        self.true_rad = []
        self.max_trajectories_nb = 0
        self.current_trajectories_nb = 0
        self.trajectories = None

    def trajectories_compute_true_radius(self) -> float:
        max_rad = 0
        for i in range(self.nb):
            max_rad = max(max_rad, self.true_rad[i])

        return max_rad

    def trajectories_k_center_add(self, element) -> None:
        for i in range(self.nb):
            tmp = trajectories_distance(self.trajectories[element], self.centers[i])
            if self.radius >= tmp:
                self.clusters.add_element_set_collection(element, i)
                self.true_rad[i] = max(tmp, self.true_rad[i])
                return

        # no insertion possible
        self.clusters.add_element_set_collection(element, self.nb)
        if self.nb < self.k:
            self.centers[self.nb] = element
            self.true_rad[self.nb] = 0
            self.nb += 1
            return

    def trajectories_is_center(self, element, cluster_index) -> int:
        cluster_index = self.clusters.get_set_index(element)
        assert -1 != cluster_index
        return 1 if self.k > cluster_index and self.centers[cluster_index] == element else 0

    def __trajectories_update_non_center(self, element, cluster_index) -> None:
        if cluster_index == self.k:
            self.clusters.sets[cluster_index].remove_element_set(element)
            self.trajectories_k_center_add(element)
            return
        
        tmp = trajectories_distance(self.trajectories[element], self.trajectories[self.centers[cluster_index]])
        if tmp > self.radius:
            self.clusters.sets[cluster_index].remove_element_set(element)
            self.trajectories_k_center_add(element)
    
    def __trajectories_reverse_update_non_center(self, element, cluster_index) -> None:
        tmp = trajectories_distance(self.trajectories[self.centers[cluster_index]], 
                                    self.trajectories[element])

        if tmp > self.radius:
            self.clusters.sets[cluster_index].remove_element_set(element)
            self.trajectories_k_center_add(element)
            return 0

        return 1

    def __trajectories_update_center_restart(self, element, cluster_index, helper_array) -> None:
        size = None

        self.clusters.sets[cluster_index].remove_element_set(element)
        self.nb = cluster_index
        self.clusters.remove_all_elements_after_set(cluster_index, helper_array, size)
        shuffle_array(helper_array, size)

        for i in range(size):
            self.trajectories_k_center_add(helper_array[i])
        self.trajectories_k_center_add(element)

    def __trajectories_check_legit_center(self, center_index, cluster_index) -> int:
        i = 0
        while i < cluster_index:
            tmp = trajectories_distance(self.trajectories[center_index], self.trajectories[self.centers[i]])
            if self.radius >= tmp:  return 0
            i += 1 

        i += 1

        while i < self.nb:
            tmp = trajectories_distance(self.trajectories[center_index], self.trajectories[self.centers[i]])
            if self.radius >= tmp: return 0
            i += 1

        return 1

    def __trajectories_iterate_reverse_center_trash(self, center_index, cluster_index) -> None:
        flag_set = self.clusters.sets[self.k]

        i = 0
        while i < flag_set.card:
            element = flag_set.elements[i]
            tmp = trajectories_distance(self.trajectories[center_index], 
                                        self.trajectories[element])
            
            if tmp <= self.radius:
                self.clusters.sets[self.k].remove_element_set(element)
                self.clusters.add_element_set_collection(element, cluster_index)
                self.true_rad[cluster_index] = max(tmp, self.true_rad[cluster_index])
            else:
                i += 1

    def __trajectories_iterate_reverse_center(self, center_index, cluster_index) -> None:
        flag_set = self.clusters.sets[cluster_index]
        old = -1

        i = 0
        while i < flag_set.card:
            assert old != flag_set.elements[i]
            old = flag_set.elements[i]
            if old != center_index:
                    i += self.__trajectories_reverse_update_non_center(flag_set.elements[i], cluster_index)
            else:
                i += 1

    def __trajectories_update_center(self, index, cluster_index, helper_array) -> None:
        if self.__trajectories_check_legit_center(index, cluster_index):
            self.__trajectories_iterate_reverse_center(index, cluster_index)
            self.__trajectories_iterate_reverse_center_trash(index, cluster_index)
        else:
            self.__trajectories_update_center_restart(index, cluster_index, helper_array)
    
    def trajectories_k_center_update(self, index, helper_array) -> None:
        cluster_index = None
        if self.trajectories_is_center(index, cluster_index):
            self.__trajectories_update_center(index, cluster_index, helper_array)
        else:
            self.__trajectories_update_non_center(index, cluster_index)


# @TODO: specify the return type after enum util py is written
#        import the library to use the unimplemented function
def trajectories_write_log(levels, nb_instances, nb_points, q):
    if log_.has_log():
        key = 'a' if query.type == "ADD" else 'u'
        result = trajectories_get_index_smallest(levels, nb_instances)
        if result == nb_instances:
            print("Error, no valid level found with bound given\n")
            return 4 #ONLY_BAD_LEVELS_ERROR
        
        if not log_.has_long_log():
            f = open(log_.get_log_file(), "w+")
            f.write("%c %u %u c%u %lf %d\n",
            q.data_index, nb_points, result, levels[result].radius, levels[result].nb)
            f.close()   
        else:
            f = open(log_.get_log_file(), "w+")
            f.write("%c %u %u c%u %lf %d\n",
            key, q.data_index, nb_points, result, levels[result].trajectories_compute_true_radius(), levels[result].nb)
            f.close()

    return 0 #NO_ERROR

def trajectories_apply_one_query(levels, nb_instances, q, helper_array):
    nb_points = 0
    if add_point_trajectories(levels[0].trajectories[q.data_index]):
        q.type = "UPDATE"
        for i in range(nb_instances):
            levels[i].trajectories_k_center_update(q.data_index, helper_array)
    else:
        nb_points += 1
        for i in range(nb_instances):
            levels[i].trajectories_k_center_add(q.data_index)

    trajectories_write_log(levels, nb_instances, nb_points, q)

def trajectories_k_center_run(levels, nb_instances, queries, helper_array):
    q = None
    while get_next_query_trajectories(queries, q):
        trajectories_apply_one_query(levels, nb_instances, q, helper_array)

def trajectories_initialise_level_array(k, eps, d_min, d_max, nb_instances, array, nb_points, helper_array) -> list:
    nb_instances = tmp = (1 + ceil(log(d_max / d_min) / log(1 + eps)))
    levels = [None] * tmp
    helper_array = [None] *nb_points

    first_trajectory_level = Trajectory_level(k, 0, array, nb_points)
    levels.append(first_trajectory_level)

    for _ in range(1, tmp):
        new_trajectory_level = Trajectory_level(k, d_min, array, nb_points)
        levels.append(new_trajectory_level)
        d_min = (1 + eps) * d_min

    return levels

def trajectories_delete_level_array(levels, nb_instances, helper_array) -> None:
    for i in range(nb_instances):
        levels[i].trajectories_delete_level()
    
    levels = []
    helper_array = []

def trajectories_get_index_smallest(levels, nb_instances) -> int:
    for i in range(nb_instances):
        if 0 == levels[i].clusters.sets[levels[i].k].card:
            return i
    
    return nb_instances