# import point
import math
import utils
from utils import log_
from data_sliding import sliding_import_points, sliding_distance


class Sliding_level:

    def __init__(self,level=None, k=0,radius=0,array=None,nb_points=0):
        self.k=k #Maximum number of clusters allowed
        self.radius=radius #Cluster radius
        self.elements=[0]*nb_points #the ancestor of each element
        self.attr_nb=int() #Number of attraction points
        self.attr=[None]*(k+1) #index of all attraction points, looping array
        self.repr= [None]*(k+1) #index of all representative points
        self.orphans=[None]*(k+2) #index of all orphans
        self.parents=[None]*(k+2) #index of the dead parent of each orphan
        for i in range(0,k+2):
            self.orphans[i]= -1
            self.parents[i]= -1

        self.first_attr=0 #index of oldest attractor in attr
        self.centers= [None]*(k+1) #index of all clusters
        self.cluster_nb=0 #true number of cluster
        self.sp_points= [None]*(2*k+3) #true assignment of every attractor and orphan in the clustering
        self.first_point= 0 #oldest point
        self.last_point= 0 #newest point
        self.nb_points= nb_points #total number of points in array
        self.array=array #pointer to all points


    def remove_expired_orphans(self, first_point) -> None:
        for i in range(0, self.k+2):
            if -1 != self.orphans[i] and self.orphans[i] < first_point:
                self.orphans[i]= -1
                self.parents[i]= -1

    def create_orphan_simple(self, parent, orphan) -> None:
        if parent != orphan:
            for i in range(0, self.k+2):
                if -1 == self.orphans[i]:
                    self.orphans[i]= orphan
                    self.parents[i]= parent
                    return
            #should not be printed
            print("create_orphan_simple(): SHOULD NOT PRINT")

    def create_orphan_complex(self, parent, orphan) -> None:
        if parent != orphan:
            for i in range(0, self.k+2):
                if -1 == self.orphans[i]:
                    self.orphans[i]= orphan
                    self.parents[i]= parent
                    return
            self.remove_expired_orphans(self.attr[self.first_attr])

            for i in range(0, self.k+2):
                if -1 == self.orphans[i]:
                    self.orphans[i]= orphan
                    self.parents[i]= parent
                    return
            #should not be printed
            print("create_orphan_complex(): SHOULD NOT PRINT")

    def remove_expired_attraction(self) -> None:
        orphan=int()
        parent=int()

        while self.attr_nb and self.attr[self.first_attr] < self.first_point:
            orphan = self.repr[self.first_attr]
            parent = self.attr[self.first_attr]
            self.attr[self.first_attr] = -1
            self.repr[self.first_attr] = -1
            self.first_attr = (self.first_attr +1) % (self.k + 1)
            self.attr_nb -= 1
            if orphan >= self.first_point:
                self.create_orphan_simple(parent,orphan)


    def remove_expired_points(self, exp_date) -> None:
        self.remove_expired_orphans(exp_date)
        self.remove_expired_attraction()

    def add_cluster(self, element) -> None:
        if self.attr_nb > self.k:
            orphan = self.repr[self.first_attr]
            parent = self.attr[self.first_attr]
            self.first_attr = (self.first_attr +1) % (self.k + 1)
            self.attr_nb -= 1
            self.create_orphan_complex(parent,orphan)

        if self.attr_nb > self.k -1:
            self.remove_expired_orphans(self.attr[self.first_attr])

        self.elements[element] = element
        self.attr[(self.first_attr + self.attr_nb) % (self.k +1)] = element
        self.repr[(self.first_attr + self.attr_nb) % (self.k +1)] = element

        self.attr_nb +=1

        assert(self.attr_nb <= self.k +1 )

    def __compute_centers(self, element, elm_index) -> int:

        for i in range(0, self.cluster_nb):
            #just pass index of element maybe?
            tmp = sliding_distance(self.array[element],
                                   self.array[self.centers[i]])
            if self.radius >= tmp:
                self.sp_points[elm_index] = self.centers[i]
                return 0


        if self.cluster_nb == self.k:
            return 1

        self.centers[self.cluster_nb] = element
        self.cluster_nb += 1
        self.sp_points[elm_index] = element
        return 0


    def sliding_compute_centers(self) -> None:
        self.cluster_nb=0
        if self.attr_nb > self.k:
            return

        index= self.first_attr
        for i in range(0, self.attr_nb):
        # Oh neul eun yeo gi GGA ji
            self.centers[self.cluster_nb] = self.attr[index]
            self.cluster_nb += 1
            self.sp_points[index] = self.attr[index]

            index = (index+1)%(self.k+1)

        for i in range(0, self.k +2):
            if -1 != self.orphans[i]:
                if self.__compute_centers(self.orphans[i], i+ self.k +1):
                    self.centers[self.cluster_nb] = self.orphans
                    self.cluster_nb = self.k + 1
                    return


    def sliding_k_center_add(self, element) -> None:

        flag = 0
        d_min, tmp = float(), float()

        # array = Timestamped_point()
        array = self.array
        self.last_point = element + 1

        while (self.first_point <= element
        and array[element].in_date >= array[self.first_point].exp_date):

            self.remove_expired_points(self.first_point)

            index = self.first_attr
            for _ in range(0, self.attr_nb):
                tmp = sliding_distance(array[element], array[self.attr[index]])
                if self.radius >= tmp:
                    if not flag:
                        flag = 1
                        d_min=tmp
                        i_min=index
                    elif d_min > tmp :
                        d_min = tmp
                        i_min = index

                #update the for loop index
                index = (index+1)%(self.k+1)

            if not flag:
                self.add_cluster(element)
            else:
                self.elements[element] = self.attr[i_min]
                self.repr[i_min] = element


            #update the while loop condition
            self.first_point +=1

    def sliding_delete_level(self):
        self.elements = None
        self.attr = None
        self.repr = None
        self.orphans = None
        self.parents = None
        self.centers = None
        self.sp_points = None

    def sliding_compute_true_radius(self):
        true_radius = 0.0 
        i= self.first_point
        while i < self.last_point:
            index_cluster = self.sliding_find_cluster(i)
            index_center = self.centers[index_cluster]
            tmp = sliding_distance(self.array[i] , self.array[index_center])

            if true_radius < tmp :
                true_radius = tmp
        
        return true_radius

    def sliding_find_cluster(self, element):
        parent = self.elements[element]

        for i in range(0, self.cluster_nb):
            if parent == self.centers[i]:
                return i 
        
        for i in range(0, self.k +2 ):
            if self.orphans[i] != -1 and self.parents[i] == parent :
                center = self.sp_points[self.k+1+i]
                for j in range(0, self.cluster_nb):
                    if center == self.centers[j]:
                        return j 
                #Should terminate
                print("ERROR IN SLIDING_FIND_CLUSTER")
        print("ERROR IN SLIDING_FIND_CLUSTER")


def sliding_initialise_levels_array(levels, k, eps, d_min, d_max, nb_instances, array, nb_points)-> list:
    tmp = 1 + math.ceil(math.log(d_max / d_min) / math.log(1 + eps))
    nb_instances= tmp
    # levels = [None] * tmp
    init=Sliding_level(levels, k, 0, array, nb_points)
    levels.append(init)
    for i in range(0, tmp):
        #initialize each array
        level= Sliding_level(levels[i], k, d_min, array, nb_points)
        d_min = (1+eps) * d_min
        levels.append(level)
    
    #levels array is updated by "Pass by reference"
    return nb_instances 

    # need to put level objects in the levels array


def sliding_delete_levels_array(levels, nb_instances) -> None:
    for i in range(0, nb_instances):
        levels[i].sliding_delete_level()

    #maybe deletion and freeing of levels array can be simpler

    

def sliding_get_index_smallest(levels, nb_instances) -> int:
    upper_limit = levels[0].k +1
    for i in range(0, nb_instances):
        if (levels[i].attr_nb < upper_limit and
            levels[i].cluster_nb <upper_limit):
            return i

    return nb_instances

def sliding_write_log(levels, nb_instances, element) ->int:
    
    # print(log_)
    log = log_.get_log_file()
    if log_.has_log():
        result = sliding_get_index_smallest(levels, nb_instances)
        if result == nb_instances:
            log.write("Error no feasible radius possible found after inserting "+str(element))
            return 1



        if log_.has_long_log():
            logstr = "\na " + str(levels[result].last_point - 1) + " " + str(levels[result].last_point - levels[result].first_point) + " c" + str(result) + \
                " " + str(levels[result].radius) + " " + str(levels[result].sliding_compute_true_radius()) + " " + str(levels[result].cluster_nb)
            log.write(logstr)

        else:
            logstr = "\na " + str(levels[result].last_point - 1) + " " + str(levels[result].last_point - levels[result].first_point) + " c" + str(result) + \
                " " + str(levels[result].radius) + " " + str(levels[result].cluster_nb)
            log.write(logstr)

    return 0

#Have not checked sliding_compute_centers
def sliding_k_center_run(levels, nb_instances) -> None:
    for i in range(0, levels[0].nb_points):
        for j in range(0, nb_instances):
            levels[j].sliding_k_center_add( i )
        for j in range(0, nb_instances):
            levels[j].sliding_compute_centers()
        sliding_write_log(levels, nb_instances, i)

