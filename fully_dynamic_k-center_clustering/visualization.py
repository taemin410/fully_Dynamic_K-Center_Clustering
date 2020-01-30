import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

'''
    Plot the similarity of the clustering graph.

    params:
        vals - similarity values (float array)
        y_label - label of y

    return:
'''
def plot_clustering_similarity_graph(vals, y_label):
    x = np.arange(len(vals))
    plt.plot(x, vals, label = y_label) 
        
    plt.xlabel('number of queries') 
    plt.ylabel('clustering similarity') 
    plt.title('Similarity b/w two clusterings') 
    
    plt.legend() 
     
    plt.show()



'''
    Plot multiple similarity of the clustering graphs.

    params:
        data - array of tuples 
            [(ylabel, values)]
    return:
'''
def plot_multiple_clustering_similarity_graph(data):
    x = np.arange(len(data[0][1]))

    for datum in data:
        ylabel = datum[0]
        vals = datum[1]

        plt.plot(vals, label=ylabel)


    plt.xlabel('number of queries') 
    plt.ylabel('clustering similarity') 
    plt.title('Similarity b/w two clusterings')

    plt.legend()
    plt.show()





'''
    Visualize the scatter plotting graph of clustering.

    params:
        levels - clustering levels
        index - index of optimal clustering environment
'''
def plot_clustering(levels, index):
    opt_cluster = levels[index].clusters.sets
    opt_cluster_array = []
    geo_dataframe = []

    # remove unnecessary None type values
    for i in range(len(opt_cluster)):
        elm_arr = set(opt_cluster[i].elements)
        elm_arr.discard(None)
        opt_cluster_array.append(elm_arr)

    # parse the geo point data and append it into geo point dataframe
    for cluster_index in range(len(opt_cluster_array)):
        for data_index in opt_cluster_array[cluster_index]:
            current_geo_obj = levels[index].array[data_index]
            current_lat = current_geo_obj.latitude
            current_long = current_geo_obj.longitude
            
            geo_data_arr = [current_lat, current_long, cluster_index]
            geo_dataframe.append(geo_data_arr)

    
    df = pd.DataFrame(geo_dataframe, columns = ["latitude", "longitude", "cluster_index"])
    df.plot.scatter(x = "latitude", y = "longitude", c= "cluster_index", cmap= plt.cm.RdYlGn)
    plt.show()



    




    