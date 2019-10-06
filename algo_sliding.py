# import point

class Sliding_level:

    def __init__(self):
        self.k=int()
        self.radius=float()
        self.elements=[]
        self.attr_nb=[]
        self.repr=[]
        self.orphans=[]
        self.parents=[]
        self.first_attr=int()
        self.centers=[]
        self.cluster_nb=int()
        self.sp_points=[]
        self.first_point=int()
        self.last_point=int()
        self.nb_points=int()
        self.array=[]


def sliding_initialise_level(level, k, radius, array, nb_points) -> None :
    i = int()
    level.attr_nb=0
    level.k=k
    level.radius=radius
    level.elements= list(nb_points)
