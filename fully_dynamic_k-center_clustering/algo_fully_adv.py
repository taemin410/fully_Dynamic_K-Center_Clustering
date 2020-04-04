import point
import random
import copy
import heapq
from set_ import Set_, Set_collection
from query import query, query_provider
from data_fully_adv import fully_adv_distance
from utils import log_, shuffle_array
from math import ceil, log
from cluster_comparison import Cluster_comparator
from center_comparison import Center_comparator
import visualization as viz
import static_variables as sv
# from numba import jit, cuda 


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

        return:
            i - index of cluster that the new element is added
    '''
    def fully_adv_k_center_add(self, index) -> int:
        for i in range(self.nb):
            tmp = fully_adv_distance(self.array[index], self.array[self.centers[i]])
            if self.radius >= tmp:
                self.clusters.add_element_set_collection(index, i)
                self.true_rad[i] = max(tmp, self.true_rad[i])
                return i 

        # add element as a center or put it in a set of unclustered data points
        self.clusters.add_element_set_collection(index, self.nb)
        if self.nb < self.k:
            self.centers[self.nb] = index
            self.true_rad[self.nb] = 0
            self.nb += 1
        
        return self.nb

    def fully_adv_k_center_delete(self, element_index, helper_array) -> bool :
        size = int()
        cluster_index = self.clusters.get_set_index(element_index)
        self.clusters.remove_element_set_collection(element_index)

        # center of cluster deleted
        if cluster_index < self.k and element_index == self.centers[cluster_index]:
            self.nb = cluster_index
            helper_array.clear()
            size = self.clusters.remove_all_elements_after_set(cluster_index, helper_array, size)
            random.shuffle(helper_array)
            
            for point in helper_array:
                self.fully_adv_k_center_add(point)

            return True 
        #if in case of simple deletion
        return False

    def fully_adv_compute_true_radius(self) -> float:
        max_rad = 0
        for i in range(self.nb):
            max_rad = max(max_rad, self.true_rad[i])

        return max_rad


class Fully_adv_cluster_nearest_neighbor(Fully_adv_cluster):
    def __init__(self, k, radius, array, nb_points, cluster_size, nearest_neighbor_dict):
        super().__init__(k, radius, array, nb_points, cluster_size)
        self.nearest_neighbor_dict = nearest_neighbor_dict # key: index of center point, val: priority queue (nearest neighbor will be on top)

    def fully_adv_k_center_add(self, index) -> int:
        for i in range(self.nb):
            tmp = fully_adv_distance(self.array[index], self.array[self.centers[i]])
            if self.radius >= tmp:
                self.clusters.add_element_set_collection(index, i)
                self.true_rad[i] = max(tmp, self.true_rad[i])

                if i < self.k - 1:
                    # print("index: ", i)
                    current_element_heap = self.nearest_neighbor_dict.get(self.centers[i])
                    heapq.heappush(current_element_heap, (tmp, index))
                    # print("dict: ", self.nearest_neighbor_dict)
                return i 

        # add element as a center or put it in a set of unclustered data points
        self.clusters.add_element_set_collection(index, self.nb)
        if self.nb < self.k:
            self.centers[self.nb] = index
            self.true_rad[self.nb] = 0
            self.nb += 1
            self.nearest_neighbor_dict[index] = []
        
        return self.nb

    def fully_adv_k_center_delete(self, element_index, helper_array) -> bool :
            size = int()
            cluster_index = self.clusters.get_set_index(element_index)
            self.clusters.remove_element_set_collection(element_index)

            # center of cluster deleted
            if cluster_index < self.k and element_index == self.centers[cluster_index]:
                self.nb = cluster_index
                new_center_candidates = set()

                # select previous centers of the clusters, with higher index than the cluster whose center has been deleted, as new centers of the clusters
                tmp_index = cluster_index
                while tmp_index+1 < self.k :
                    cand_center = self.centers[tmp_index+1]
                    if cand_center:
                        new_center_candidates.add(cand_center)
                    tmp_index += 1

                # uncluster all the data points in the current cluster and clusters with higher index than the cluster whose center has been deleted
                helper_array.clear()
                size = self.clusters.remove_all_elements_after_set(cluster_index, helper_array, size)
                random.shuffle(helper_array)

                # select the nearest neighbor of the deleted point as a new center of cluster
                candidate_heap = self.nearest_neighbor_dict.pop(element_index)
                if len(candidate_heap) > 0 :
                    candidate_index =  heapq.heappop(candidate_heap)[1]
                    new_center_candidates.add(candidate_index)

                # Erase self.centers from self.nb to self.k -> to None 
                for i in range(self.nb, self.k):
                    self.centers[i]=None 

                # add candidate points as new centers of the clusters
                for new_center in new_center_candidates:
                    self.clusters.add_element_set_collection(new_center, self.nb)
                    if self.nb < self.k:
                        self.centers[self.nb] = new_center
                        self.true_rad[self.nb] = 0
                        self.nb += 1
                        self.nearest_neighbor_dict[new_center] = []

                # finally add remaining datapoints
                # add non-candidate data points
                for point in helper_array:
                    if point not in new_center_candidates:
                        self.fully_adv_k_center_add(point)

                return True
            #if in case of simple deletion
            return False 

class Fully_adv_cluster_cache(Fully_adv_cluster):
    def __init__(self, k, radius, array, nb_points, cluster_size):
        super().__init__(k, radius, array, nb_points, cluster_size)
        self.center_index_map = {}    # key: index of a center point, val: index of cluster

    def fully_adv_k_center_add(self, index) -> int:
        for i in range(self.nb):
            tmp = fully_adv_distance(self.array[index], self.array[self.centers[i]])
            if self.radius >= tmp:
                self.clusters.add_element_set_collection(index, i)
                self.true_rad[i] = max(tmp, self.true_rad[i])
                return i 

        # add element as a center or put it in a set of unclustered data points
        self.fully_adv_k_center_add_unclusterd_element(index)
        
        return self.nb

    def fully_adv_k_center_add_unclusterd_element(self, index) -> None:
        self.clusters.add_element_set_collection(index, self.nb)
        if self.nb < self.k:
            self.centers[self.nb] = index
            self.center_index_map[index] = self.nb
            self.true_rad[self.nb] = 0
            self.nb += 1

    def fully_adv_k_center_cache_recluster(self, cluster_index, cache, helper_array) -> None:
        if len(helper_array) == 0:
            return

        # randomly pick one data point as a new center
        new_centers = set()
        first_elm = helper_array.pop()

        self.fully_adv_k_center_add_unclusterd_element(first_elm)
        new_centers.add(first_elm)

        # loop through unclustered data points and select new candidates for centers
        num_new_center = self.k - cluster_index

        # listed_helper = list(helper_array)
        # random.shuffle(listed_helper)

        for center_candidate in helper_array.copy():
            if len(new_centers) < num_new_center:

                candidate_flag = True

                for c in new_centers:
                    if fully_adv_distance(self.array[center_candidate], self.array[c]) <= self.radius:
                        candidate_flag = False

                if candidate_flag:
                    self.fully_adv_k_center_add_unclusterd_element(center_candidate)
                    new_centers.add(center_candidate)
                    helper_array.remove(center_candidate)

            else:
                break

        # listed_helper = list(helper_array)

        # add elements in unclustered set to new clusters so that each element belong to the cluster where element that was in same cluster is a current center
        for x in helper_array.copy():
            # print("current element: ", x)
            for c in new_centers:
                if cache[x] == cache[c] and self.radius >= fully_adv_distance(self.array[x], self.array[c]):
                    self.clusters.add_element_set_collection(x, self.center_index_map.get(c))
                    helper_array.remove(x)
                    break

        # listed_helper = list(helper_array)

        # add still unclustered elements to cluster
        for unclusterd_x in helper_array:
            self.fully_adv_k_center_add(unclusterd_x)


    def fully_adv_k_center_delete(self, element_index, helper_array) -> None:
        size = int()
        cluster_index = self.clusters.get_set_index(element_index)
        self.clusters.remove_element_set_collection(element_index)

        # center of cluster deleted
        if cluster_index < self.k and element_index == self.centers[cluster_index]:
            self.nb = cluster_index
            helper_array.clear()

            # uncluster data points
            size, cache = self.clusters.cache_and_remove_all_elements(cluster_index, helper_array, size)
            random.shuffle(helper_array)

            #@TODO: change helper array to set 
            self.fully_adv_k_center_cache_recluster(cluster_index, cache, set(helper_array))
            
            return True
        
        #if in case of simple deletion
        return False 

def fully_adv_write_log(levels, nb_instances, cluster_index, nb_points, q) -> int:
    key = 'a' if q.type == "ADD" else 'd'
    if log_.has_log():
        result = fully_adv_get_index_smallest(levels, nb_instances)

        if result == nb_instances:
            print('Error, no feasible radius possible found after inserting', q.data_index)
            return 4 #only_bad_levels_error

        content = 'key: ' + str(key) + ' ' + 'data index: ' + \
            str(q.data_index) + ' ' + 'nb_points: ' + str(nb_points) + ' '\
            'result: ' + str(result) + ' ' + 'cluster_index: ' + str(cluster_index) + ' ' + 'radius: ' + str(levels[result].radius) + ' ' + 'true radius: ' + str(levels[result].fully_adv_compute_true_radius()) \
            + '\n'

        if log_.has_long_log():
            f = log_.get_log_file()
            f.write(content)

        else:
            f = log_.get_log_file()
            f.write(content)
    return 0

'''
    Apply query to existing clusters.
    
    params:
        levels - clustering environments
        nb_instances - number of clustering environments
        q - query
        helper_array - array storing clustering information (this is used in reclustering)

    return: fully_adv_write_log (denoting exit status of log), q (query information)
'''
def fully_adv_apply_one_query(levels, nb_instances, q, helper_array) -> tuple:

    # reset all the helper variables before applying query
    cluster_index = None

    if q.type == "ADD":
        sv.nb_points += 1

        # add a new data point to all clustering environments
        for i in range(nb_instances):
            cluster_index = levels[i].fully_adv_k_center_add(q.data_index)

    else:
        sv.nb_points -= 1

        reclustered_levels_list=[]
        # delete a data point from all clustering environments
        for i in range(nb_instances):
            reclustered_levels_list.append(levels[i].fully_adv_k_center_delete(q.data_index, helper_array))
        
        return fully_adv_write_log(levels, nb_instances, cluster_index, sv.nb_points, q), q , reclustered_levels_list


    return fully_adv_write_log(levels, nb_instances, cluster_index, sv.nb_points, q), q , []

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
        helper_array - helper array in which update information of data points will be stored

    return:
        nb_instances - number of dynamic clustering environments
        helper_array - helper array
'''
def fully_adv_initialise_level_array(levels, k, eps, d_min, d_max, nb_instances, points, nb_points, cluster_size, helper_array, cluster_type = "default") -> tuple:
    nb_instances = tmp = (1 + ceil( log(d_max / d_min) / log(1 + eps)))
    # helper_array = [None] * nb_points
    helper_array = []

    if cluster_type == "default":   # fully dynamic k-center cluster
        # assign new fully adv cluster to each index of array
        levels.append(Fully_adv_cluster(k, 0, points, nb_points, cluster_size))
        for _ in range(1, tmp):
            levels.append(Fully_adv_cluster(k, d_min, points, nb_points, cluster_size))
            d_min = (1 + eps) * d_min
    
    elif cluster_type == "nn":  # nearest neighbor
        # nearest_neighbor_dict = {}
        levels.append(Fully_adv_cluster_nearest_neighbor(k, 0, points, nb_points, cluster_size, {}))
        for _ in range(1, tmp):
            levels.append(Fully_adv_cluster_nearest_neighbor(k, d_min, points, nb_points, cluster_size, {}))
            d_min = (1 + eps) * d_min

    elif cluster_type == "cache":  # cache
        levels.append(Fully_adv_cluster_cache(k, 0, points, nb_points, cluster_size))
        for _ in range(1, tmp):
            levels.append(Fully_adv_cluster_cache(k, d_min, points, nb_points, cluster_size))
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

def fully_adv_k_center_run(levels, cache_levels, nb_instances, queries, helper_array, cache_helper_array):
    # ENVIRONMENT NUMBER 
    ENV_NUM=24
    
    q = query()
    q_num = 0

    joint_normalized_MI_vals = []
    cache_joint_normalized_MI_vals = []
    ARI_vals = []
    cache_ARI_vals = []
    ari_cont = []
    cache_ari_cont = []

    center_difference_counts=[]

    prev_set_same, prev_set_diff = set(), set()
    prev_cache_set_same, prev_cache_set_diff = set(), set()
    cluster_before_query = copy.deepcopy(levels[ENV_NUM].clusters.sets)
    cache_cluster_before_query = copy.deepcopy(cache_levels[ENV_NUM].clusters.sets)
    flag = False
    v_set= None
    cache_v_set = None

    while queries.get_next_query_set(q, levels[ENV_NUM].clusters) :
        #Count Query number
        q_num+=1

        centers_before = set(levels[ENV_NUM].centers)
        # apply a query
        exit_status, query_info, has_reclutered_list = fully_adv_apply_one_query(levels, nb_instances, q, helper_array)
        
        centers_after = set(levels[ENV_NUM].centers) 
        
        center_comparator = Center_comparator(centers_before, centers_after)
        
        center_diff_cnt = center_comparator.get_difference_count()
        # print("==========================")
        # print(center_comparator.get_set_difference())
        # print(center_diff_cnt)
        # print("==========================")


    #     cache_exit_status, cache_query_info, cache_has_reclutered_list = fully_adv_apply_one_query(cache_levels, nb_instances, q, cache_helper_array)
        
    #     # Flag is True when has_reclusterd_list[] exists and is true 
        reclustering_flag  = has_reclutered_list[ENV_NUM] if has_reclutered_list else False
        if reclustering_flag:
            center_difference_counts.append(center_diff_cnt)

    #     cache_reclustering_flag = cache_has_reclutered_list[ENV_NUM] if cache_has_reclutered_list else False

    #     # (re)formulate cluster comparison envrionment 
    #     cluster_after_query = levels[ENV_NUM].clusters.sets
    #     cache_cluster_after_query = cache_levels[ENV_NUM].clusters.sets

    #     comparison = Cluster_comparator(cluster_before_query, cluster_after_query)
    #     cache_comparison = Cluster_comparator(cache_cluster_before_query, cache_cluster_after_query)
        
    #     if flag:
    #         comparison.set_set_arr(v_set)
    #         cache_comparison.set_set_arr(cache_v_set)
        
    #     if reclustering_flag:
    #         comparison.make_contigency_table()
            
    #         # Normalized Mutual Information
    #         mutual_info = comparison.mutual_information()
    #         joint_entropy = comparison.joint_entropy()

    #         nmi_output = 0 if (mutual_info == 0 or joint_entropy ==0) else mutual_info / joint_entropy
    #         if nmi_output < 1.0:
    #             joint_normalized_MI_vals.append(nmi_output)
            
    #         # ARI1
    #         comparison.initialize_pairs_measure(prev_set_same, prev_set_diff)
    #         ari = comparison.adjusted_rand_index()
    #         if ari < 1.0:
    #             ARI_vals.append(ari)
    #         prev_set_same, prev_set_diff = comparison.get_pairs_lists()

    #         #ARI2
    #         ari_contingency_based = comparison.ari_contingency_table()
    #         if ari_contingency_based <1.0:
    #             ari_cont.append(ari_contingency_based)

    #     if cache_reclustering_flag:
    #         cache_comparison.make_contigency_table()

    #         # Normalized Mutual Information
    #         cache_mutual_info = cache_comparison.mutual_information()
    #         cache_joint_entropy = cache_comparison.joint_entropy()

    #         cache_nmi_output = 0 if (cache_mutual_info == 0 or cache_joint_entropy ==0) else cache_mutual_info / cache_joint_entropy
    #         cache_joint_normalized_MI_vals.append(cache_nmi_output)
            
    #         # ARI
    #         cache_comparison.initialize_pairs_measure(prev_cache_set_same, prev_cache_set_diff)
    #         ari = cache_comparison.adjusted_rand_index()
    #         cache_ARI_vals.append(ari)
    #         prev_cache_set_same, prev_cache_set_diff = cache_comparison.get_pairs_lists()

    #         # ari2
    #         cache_ari_contingency = cache_comparison.ari_contingency_table()
    #         if cache_ari_contingency <1.0:
    #             cache_ari_cont.append(cache_ari_contingency)

    #     v_set = comparison.get_set_arr()
    #     cache_v_set = cache_comparison.get_set_arr()
    #     flag= True


    viz.plot_clustering_similarity_graph(center_difference_counts, "Center Change Counter - FDKCC")
    print("average of center changes : {} ".format(sum(center_difference_counts)/len(center_difference_counts)))
    # print(q_num, " queries executed.")

    # # visualize similarity metrics
    # viz.plot_clustering_similarity_graph(joint_normalized_MI_vals, "Joint Normalized Mutual Information - FDKCC")
    # viz.plot_clustering_similarity_graph(cache_joint_normalized_MI_vals, "Joint NMI - Cache")

    # data = [("Joint Normalized Mutual Information", joint_normalized_MI_vals), 
    #         ("Joint NMI - Nearest Neighbor", cache_joint_normalized_MI_vals)]
    # viz.plot_multiple_clustering_similarity_graph(data)
    # print("average of NMI: ", sum(joint_normalized_MI_vals) / len(joint_normalized_MI_vals))
    # print("average of cache NMI: ", sum(cache_joint_normalized_MI_vals) / len(cache_joint_normalized_MI_vals))

    # viz.plot_clustering_similarity_graph(ARI_vals, "Clustering Similarity by ARI")
    # data = [("Clustering Similarity by ARI", ARI_vals),
    #         ("ARI - Cache", cache_ARI_vals)]

    # viz.plot_multiple_clustering_similarity_graph(data)
    # print("average of ARI: ", sum(ARI_vals) / len(ARI_vals))
    # print("average of cache ARI: ", sum(cache_ARI_vals) / len(cache_ARI_vals))

    # viz.plot_clustering_similarity_graph(ari_cont, "clustering similarity by contingency based ari")
    # data = [
    #     ("Clustering similarity by contingency based ari", ari_cont),
    #     ("ARI_contingency based - cache", cache_ari_cont)
    # ]
    # viz.plot_multiple_clustering_similarity_graph(data)
    # print("average of contingency_ARI: ", sum(ari_cont) / len(ari_cont))
    # print("average of contingency_cache ARI: ", sum(cache_ari_cont) / len(cache_ari_cont))

        
