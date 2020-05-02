import pytest
from fdkcc.set_ import Element_pointer, Set_, Set_collection

def test_element_pointer_class():
    setindex= 1
    pointer = 1
    elemptr = Element_pointer(setindex, pointer)
    assert elemptr.set_index == setindex
    assert elemptr.pointer == pointer

@pytest.fixture
def create_set_object():
    K=20
    CLUSTER_SIZE = 100
    ELEM_PTR_LIST = [Element_pointer(-1, -1) for _ in range(CLUSTER_SIZE)]

    setobj = Set_(K, CLUSTER_SIZE, 0, ELEM_PTR_LIST )

    return setobj

@pytest.fixture
def create_set_object_and_add_elements():
    K=20
    CLUSTER_SIZE = 100
    ELEM_PTR_LIST = [Element_pointer(-1, -1) for _ in range(CLUSTER_SIZE)]

    setobj = Set_(K, CLUSTER_SIZE, 0, ELEM_PTR_LIST )
    
    setobj.add_element_set(0)
    setobj.add_element_set(1)

    return setobj


def test_free_set(create_set_object):
    set_ = create_set_object

    set_.free_set()

    assert len(set_.elements) == 0 
    assert len(set_.elm_ptr) == 0 


def test_add_element_set(create_set_object):
    set_ = create_set_object

    set_.add_element_set(0)
    set_.add_element_set(1)

    assert set_.card == 2
    assert set_.elements[0] == 0
    assert set_.elements[1] == 1
    
    assert set_.elm_ptr[0].pointer == 0 
    assert set_.elm_ptr[1].pointer == 1 
    assert set_.elm_ptr[0].set_index == 0
    assert set_.elm_ptr[1].set_index == 0 
    

def test_remove_element_set(create_set_object_and_add_elements):
    set_ = create_set_object_and_add_elements

    set_.remove_element_set(0)

    assert set_.card == 1 
    assert set_.elm_ptr[0].set_index == -1 
    assert set_.elm_ptr[0].pointer == -1 
    assert set_.elm_ptr[1].pointer == 0 
    

@pytest.fixture
def setcol():
    return Set_collection(10, 100, 100)

def test_free_set_collection(setcol):

    setcol.free_set_collection()
    assert len(setcol.sets) == 0
    assert setcol.nb_sets == 0 

def test_add_element_set_collection(setcol):
    setcol.add_element_set_collection(10, 0)
    assert setcol.sets[0].elements[0] == 10 
    assert setcol.sets[0].elm_ptr[10].pointer == 0
    assert setcol.sets[0].elm_ptr[10].set_index == 0
    assert setcol.sets[0].card == 1
    

def test_remove_element_set_collection(setcol):
    setcol.add_element_set_collection(1, 0)
    setcol.add_element_set_collection(5, 0)
    setcol.add_element_set_collection(10, 0)

    setcol.remove_element_set_collection(5)

    assert setcol.sets[0].elm_ptr[5].pointer == -1
    assert setcol.sets[0].elm_ptr[5].set_index == -1
    assert setcol.sets[0].card == 2

    assert setcol.sets[0].elements[0] == 1
    assert setcol.sets[0].elements[1] == 10

def test_get_set_index(setcol):
    setcol.add_element_set_collection(5, 2)
    assert setcol.get_set_index(5) == 2 

def test_remove_all_elements_after_set(setcol):
    setcol.add_element_set_collection(1, 0)
    setcol.add_element_set_collection(5, 0)
    setcol.add_element_set_collection(10, 0)
    setcol.add_element_set_collection(2, 1)
    setcol.add_element_set_collection(3, 1)
    setcol.add_element_set_collection(4, 1)

    newarr= []
    newsize = setcol.remove_all_elements_after_set(0, newarr, len(newarr))
    assert newsize == 6
    assert setcol.sets[0].card == 0
    assert setcol.sets[1].card == 0 

def test_cache_and_remove_all_elements(setcol):
    setcol.add_element_set_collection(1, 0)
    setcol.add_element_set_collection(4, 1)

    newarr= []
    newsize, cache = setcol.cache_and_remove_all_elements(0, newarr, len(newarr))

    assert cache[1] == 0
    assert cache[4] == 1 

