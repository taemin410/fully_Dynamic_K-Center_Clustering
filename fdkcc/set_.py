from data_fully_adv import fully_adv_distance

NOT_IN_SET = -1
        
class Element_pointer:
    def __init__(self, set_index=-1, pointer=-1):
        self.set_index = set_index
        self.pointer = pointer

class Set_:
    def __init__(self, max_size, range_, set_index, elem_pointer):
        assert range_ >= max_size
        self.index = set_index
        self.card = 0
        self.max_card = max_size
        self.range = range_
        self.elements = [None for _ in range(max_size)] # integer array
        self.elm_ptr = elem_pointer  # element pointer array shared by all the sets

    def free_set(self) -> None:
        self.elements = []
        self.elm_ptr = []

    '''
        Add new element to this set. Here, element represents the index of the data point.

        params:
            element - index of the data point within data point obj array.

        return:
            None
    '''
    def add_element_set(self, element) -> None:
        assert element < self.range
        assert -1 == self.elm_ptr[element].set_index
        assert self.card < self.max_card

        self.elements[self.card] = element
        self.elm_ptr[element].set_index = self.index
        self.elm_ptr[element].pointer = self.card
        self.card += 1

    def remove_element_set(self, element) -> None:
        assert self.index == self.elm_ptr[element].set_index
        assert 0 < self.card

        position = self.elm_ptr[element].pointer
        self.card -= 1
        self.elm_ptr[element].set_index = NOT_IN_SET
        self.elm_ptr[element].pointer = NOT_IN_SET
        self.elements[position] = self.elements[self.card]
        self.elm_ptr[self.elements[position]].pointer = position

class Set_collection:
    def __init__(self, n, max_size, range_):
        self.sets = initialise_set_n_common(n, max_size, range_) # array of set
        self.max_size = max_size
        self.nb_sets = n

    def free_set_collection(self) -> None:
        self.sets = []
        self.nb_sets = 0

    '''
        Add new element to corresponding cluster.

        params:
            element - data_index of next query obj (data_index denotes the random query index from query text)
            set_index - index of the set (index of cluster within the cluster array)

        return:
            None
    '''
    def add_element_set_collection(self, element, set_index) -> None:
        assert set_index < self.nb_sets
        self.sets[set_index].add_element_set(element)

    def remove_element_set_collection(self, element) -> None:
        assert NOT_IN_SET != self.sets[0].elm_ptr[element].set_index
        self.sets[self.sets[0].elm_ptr[element].set_index].remove_element_set(element)

    def get_set_index(self, element) -> int:
        return self.sets[0].elm_ptr[element].set_index

    def remove_all_elements_after_set(self, set_index, array, size) -> int:
        size = 0
        while set_index < self.nb_sets:
            for iter_set in range(self.sets[set_index].card):
                array.append(self.sets[set_index].elements[iter_set])
                
                self.sets[set_index].elm_ptr[array[size]].pointer = NOT_IN_SET
                self.sets[set_index].elm_ptr[array[size]].set_index = NOT_IN_SET
                
                size += 1

            self.sets[set_index].elements = [None] * self.max_size
            self.sets[set_index].card = 0
            set_index += 1

        return size

    def cache_and_remove_all_elements(self, set_index, array, size) -> tuple:
        size = 0
        cache = {}

        while set_index < self.nb_sets:
            for iter_set in range(self.sets[set_index].card):
                elm = self.sets[set_index].elements[iter_set]
                array.append(elm)
                cache[elm] = set_index
                self.sets[set_index].elm_ptr[array[size]].pointer = NOT_IN_SET
                self.sets[set_index].elm_ptr[array[size]].set_index = NOT_IN_SET

                size += 1

            self.sets[set_index].elements = [None] * self.max_size
            self.sets[set_index].card = 0
            set_index += 1

        return size, cache

    def selective_remove_all_elements_after_set(self, set_index, centers, radius, data_array, array, size) -> int:
        size = 0
        # num_unclustered = 0
        deleted_index = set()
        deleted_center = centers[set_index]
        
        # uncluster data points only in overlapping clusters 
        while set_index < self.nb_sets - 1:
            if centers[set_index] !=None:
                distance = fully_adv_distance(data_array[deleted_center], data_array[centers[set_index]])
                if  distance < 2 * radius or distance == 0:    
                    for iter_set in range(self.sets[set_index].card):
                        current_elm = self.sets[set_index].elements[iter_set]
                        array.append(current_elm)
                        
                        self.sets[set_index].elm_ptr[current_elm].pointer = NOT_IN_SET
                        self.sets[set_index].elm_ptr[current_elm].set_index = NOT_IN_SET
                        
                        size += 1

                    deleted_index.add(set_index)
                    self.sets[set_index].elements = [None] * self.max_size
                    self.sets[set_index].card = 0

            set_index += 1

        # unclustered data points
        for iter_set in range(self.sets[set_index].card):
            current_elm = self.sets[set_index].elements[iter_set]
            array.append(current_elm)
            
            self.sets[set_index].elm_ptr[current_elm].pointer = NOT_IN_SET
            self.sets[set_index].elm_ptr[current_elm].set_index = NOT_IN_SET
            
            size += 1

        self.sets[set_index].elements = [None] * self.max_size
        self.sets[set_index].card = 0
        
        return size, deleted_index

    def has_element_set_collection(self, element) -> int:
        return NOT_IN_SET != self.sets[0].elm_ptr[element].set_index


'''Should Not be included in Set_ or Set_collection'''
def initialise_set_n_common(n, max_size, range_) -> list:
    set_coll = []
    elem_ptr_list = [Element_pointer(-1, -1) for _ in range(range_)]

    for i in range(0, n):
        set_coll.append(Set_(max_size, range_, i, elem_ptr_list))
    return set_coll

def free_set_n_common(n_common_set, n) -> None:
    for i in range(n):
        n_common_set[i].free_set()




