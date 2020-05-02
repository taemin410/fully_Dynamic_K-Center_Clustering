import point

INIT_ARRAY_SIZE = 100000

BUFSIZ= 100

def packed_distance(a, b) -> float:

    return point.euclidean_distance(a,b)


def packed_import_points(path):

    point_array=[]
    counter = 0

    with open(path) as fp:
        line = fp.readline()
        while line:

            try:
                splitted_array = line.split('\t')
                timestamp = int(splitted_array[0])

                lati_loni_array = splitted_array[1].split(' ')
                latitude = float(lati_loni_array[0])
                longitude = float(lati_loni_array[1])

                geo_point = Geo_point(latitude, longitude)

                point_array.append(geo_point)
                counter +=1

                if counter % 100000 == 0:
                    print(counter , " lines read... ")
                line = fp.readline()

            except:
                counter += 1
                print("Error in line " , counter)
                print(line)

                line = fp.readline()


    fp.close()

    return point_array


def packed_print_points(parray, nb_element) -> None:

    array = parray
    for i in range(0, nb_element):
        print(i, array[i].longitude, array[i].latitude)
        #should check for printing message format
