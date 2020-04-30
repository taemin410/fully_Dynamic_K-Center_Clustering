import point
# import utils

LIMIT_CHARACTER_LINE = 10000000

class Trajectory:

    def __init__(self):
        self.max_length=0
        self.current=0
        self.points=[]



def hausdorff_distance(a, b) -> float :
    cmax= 0
    for i in range(0, a.current):
        cmin = euclidean_distance(a.points[i], b.points[0])
        for j in range(0, b.current):
            tmp = euclidean_distance(a.points[i], b.points[j])
            if tmp < cmax:
                break
            if tmp < cmin:
                cmin= tmp

        if cmin > cmax:
            cmax = cmin

    return cmax

def trajectories_distance(a,b) -> float:
    return max(hausdorff_distance(a, b), hausdorff_distance(b, a))


def trajectories_read_first_line(f, buffer, nb_elements, nb_points) -> bool:
    # f = open(path, "r")

    tmp = buffer.split("\t\n")

    for i in tmp:
        print(i)


def read_point_trajectory(point) -> bool:
    #reading point string to double format
    longitude = point.longitude
    latitude = point.latitude

    coordinates = (longitude, latitude)
    #where does the coordinates be sent?

    if coordinates:
        return True

    return False

#Reading file and parsing should be done after we look at the data file ...
# def read_trajectory(trajectory, buffer, points, nb_points):



def add_point_trajectory(t) -> int:
    t.current += 1
    return t.current

def trajectories_delete_points(array) -> None:
    array=[]
    free(array)
    # import gc
    # gc.collect()
