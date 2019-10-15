import point
# import utils

INIT_ARRAY_SIZE = 100000

BUFSIZ= 100

def packed_distance(a, b) -> double:

    return point.euclidean_distance(a,b)


def packed_read_point(string, p) -> bool:

    tmp = string.split("\t")

    if not tmp:
        return False

    #tokenize and check for format of Geo_point p
    p = tmp

    if not p.longitude:
        return False

    if not p.latitude:
        return False

    return True


def packed_import_points(point_array, nb_element, path)-> bool:

    buffer = [0]*BUFSIZ
    line = 1
    current = 0
    max_array = INIT_ARRAY_SIZE

    f = open(path, "r")
    f1 = f.readlines()
    for x in f1:
        point_array.append(x)

    f.close()

    nb_element = current

    #reading buffers from packed_read_point
    # not finished

    return True

def packed_print_points(parray, nb_element) -> None:

    Geo_point array = parray
    for i in range(0, nb_element):
        print(i, array[i].longitude, array[i].latitude)
        #should check for printing message format
