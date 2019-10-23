from point import Geo_point, Timestamped_point

def sliding_import_points(path, window_length):

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
                timestamped_point = Timestamped_point(timestamp, timestamp+window_length, geo_point)

                point_array.append(timestamped_point)
                counter +=1

                if counter % 100000 == 0:
                    print(counter , "th line read... ")

            except:
                counter += 1
                print("Error in line " , counter)
                print(line)

            #Finally
            line = fp.readline()


    fp.close()

    return point_array
