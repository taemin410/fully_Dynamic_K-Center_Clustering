import point

INIT_ARRAY_SIZE = 100000

def fully_adv_distance(x, y):
	return point.euclidean_distance(x, y)

def fully_adv_import_points(path, window_length):

    point_array=[]

    with open(path) as fp:
        line = fp.readline()
        while line:
            splitted_array = line.split('\t')
            timestamp = int(splitted_array[0])

            lati_loni_array = splitted_array[1].split(' ')
            latitude = float(lati_loni_array[0])
            longitude = float(lati_loni_array[1])

            geo_point = Geo_point(latitude, longitude)
            # timestamped_point = Timestamped_point(timestamp, timestamp+window_length, geo_point)

            point_array.append(geo_point)
    fp.close()

    return point_array
