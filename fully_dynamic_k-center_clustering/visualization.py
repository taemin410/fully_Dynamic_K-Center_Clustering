import matplotlib.pyplot as plt
import numpy as np


def plot_clustering_similarity_graph(vals):
    x = np.arange(len(vals))
    plt.plot(x, vals, label = "MI") 
        
    plt.xlabel('number of queries') 
    plt.ylabel('clustering similarity') 
    plt.title('Similarity b/w two clusterings') 
    
    plt.legend() 
     
    plt.show() 