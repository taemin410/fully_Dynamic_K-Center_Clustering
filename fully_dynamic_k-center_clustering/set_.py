NOT_IN_SET = -1

class Element_pointer:
    def __init__(self):
        self.set_index = 0
        self.pointer = 0

class Set_:
    def __init__(self, max_size, range_, set_index):
        assert range_ >= max_size
        self.index = set_index
        self.card = 0
        self.max_card = max_size
        self.range = range_
        self.elements = [None] * (max_size)  # integer array
        self.elm_ptr = [-1] * (range_) # element pointer array

    def free_set(self) -> None:
        self.elements = [] 
        self.elm_ptr = []

    def add_element_set(self, element) -> None:
        assert element < self.range
        assert -1 == self.elm_ptr[element].set_index
        assert self.card < self.max_card

        self.elements[self.card] = element
        self.elm_ptr[element].set_index = self.index
        self.elm_ptr[element].pointer = self.card
        self.card += 1

    def remove_element_set(self, element) -> None:
        #@TODO: verify whehter set.set_index => self.index 
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
        self.sets = [] # array of set
        self.nb_sets = n 

    def free_set_collection(self) -> None:
        self.sets = []
        self.nb_sets = 0

    def add_element_set_collection(self, element, set_index) -> None:
        assert set_index < self.nb_sets
        self.sets[set_index].add_element_set(element)

    def remove_element_set_collection(self, element) -> None:
        assert NOT_IN_SET != self.sets[0].elm_ptr[element].set_index
        self.sets[self.sets[0].elm_ptr[element].set_index].remove_element_set(element)

    def get_set_index(self, element) -> int:
        return self.sets[0].elm_ptr[element].set_index

    def remove_all_elements_after_set(self, set_index, array, size) -> None:
        size = 0
        while set_index < self.nb_sets:
            for iter_set in range(self.sets[set_index].card):
                array[size] = self.sets[set_index].elements[iter_set]
                self.sets[set_index].elm_ptr[array[size]].pointer = NOT_IN_SET
                self.sets[set_index].elm_ptr[array[size]].set_index = NOT_IN_SET
                size += 1

            self.sets[set_index].card = 0
            set_index += 1

    def has_element_set_collection(self, element) -> int:
        return NOT_IN_SET != self.sets[0].elm_ptr[element].set_index


'''Should Not be included in Set_ or Set_collection'''
def initialise_set_n_common(self, n, max_size, range_) -> list:
    set_coll = []
    _set = Set_(max_size, range_, 0)
    set_coll.append(_set)

    for i in range(1, n):
        new_set = Set_(max_size, range_, i)
        new_set.elm_ptr = set_coll[0].elm_ptr
        set_coll.append(new_set)

    return set_coll

def free_set_n_common(self, n_common_set, n) -> None:
    for i in range(n):
        n_common_set[i].free_set()




