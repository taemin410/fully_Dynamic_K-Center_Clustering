

def sliding_import_points(path):

    point_array=[]

    f = open(path, "r")
    f1 = f.readlines()
    for x in f1:
        point_array.append(x)

    f.close()

    return point_array
