import matplotlib.pyplot as plt
import numpy as np

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
    Visualize the scatter plotting graph of clustering.

    params:
        clustering_env - clustering environment containing all the information of the clustering.
'''
def plot_clustering(clustering_env):
    pass 