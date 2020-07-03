from algo_sliding import *
from algo_fully_adv import *
from algo_trajectories import *
from data_sliding import sliding_import_points
from data_fully_adv import *
from query import *

import sys
import argparse
import tensorflow as tf
"""
__main__.py

__main__.py file is executed with command 'python fully_dynamic_k-center_clustering/ '


main()


"""

def sliding_k_center(prog_args):

    nb_instances=int()
    size = int()
    array=None

    size, array = sliding_import_points(prog_args["points_path"] , prog_args["window_length"])
    print("Import ended! ")


    levels = []
    nb_instances = sliding_initialise_levels_array(levels, prog_args["k"], prog_args["epsilon"], prog_args["d_min"],
					prog_args["d_max"], nb_instances, array, size)

    sliding_k_center_run(levels, nb_instances)

    print("sliding model finished")


def fully_adv_k_center(prog_args):

    nb_instances=int()
    size = int()
    array=None
    helper_array = None
    cache_helper_array = None
    clusters_array = []
    cache_clusters_array = []
    
    print("importing geo points...")
    size, array = fully_adv_import_points(prog_args["points_path"], prog_args['window_length'])
    print("geo point array successfully built!")

    print("initializing queries and query provider...")
    queries = query_provider()
    queries.initialise_query_provider(prog_args["queries_path"])
    if prog_args["cluster_size"] == 0:
        prog_args["cluster_size"] = size
    print("query provider successfully initialized!")

    print("building cluster array...")
    nb_instances, helper_array = fully_adv_initialise_level_array(clusters_array, prog_args["k"],
                                    prog_args["epsilon"], prog_args["d_min"],
                                	prog_args["d_max"],nb_instances, array,
                                    size, prog_args["cluster_size"], helper_array)

    print("building new algorithm based cluster array...")
    nb_instances, cache_helper_array = fully_adv_initialise_level_array(cache_clusters_array, prog_args["k"],
                                    prog_args["epsilon"], prog_args["d_min"],
                                	prog_args["d_max"],nb_instances, array,
                                    size, prog_args["cluster_size"], cache_helper_array, cluster_type="selective")

    print("fully adv environment successfully intialized!")

    print("running fully adv k center...")
    fully_adv_k_center_run(clusters_array, cache_clusters_array, nb_instances, queries, helper_array, cache_helper_array)

    # fully_adv_center_run(clusters_array, nb_instances, queries, helper_array)

def arg_parse(prog_args):
    parser = argparse.ArgumentParser(description='Model selection')
    parser.add_argument('--sliding','-s', help="Run sliding window model", action='store_true' )
    parser.add_argument('--fullyadv','-f', help="Run Fully Adversarial Model", action='store_true' )

    args = parser.parse_args()

    if args.sliding:
        window_length = input("if sliding window model Window length: ")
        if window_length:
            prog_args["window_length"] = window_length

        print(parser.parse_args())
        sliding_k_center(prog_args)
    if args.fullyadv:
        print(parser.parse_args())
        fully_adv_k_center(prog_args)

def main(prog_args):

    #
    #   INITIALIZE PROG_ARGS
    #

    #
    #   READ USER INPUT  (DEFAULT path is set to dataset/timestamped_gps_coordinate.txt)
    #


    #
    #   Split large query data points into smaller parts
    # 
    count = 0 
    File_object = open("dataset/smaller_queries.txt", "w")

    query = []
    with open('dataset/readable.txt','r') as f:
        for line in f:
            if count > 10000:
                break
            File_object.write(line)
            # query.append(line)
            count += 1

        # random.shuffle(query)
        # for i in query:
        #     File_object.write(i)

    File_object.close()
    f.close()

    prog_args["queries_path"] = "dataset/smaller_queries.txt"
    # readpath = input("Path to the dataset (relative or full path) : ")
    # if readpath:
    #     prog_args["points_path"]= readpath

    #
    #   Run Argument parser
    #
    arg_parse(prog_args)
    print("Program terminates")


#
#RUN SCRIPT HERE 
#
prog_args={
    "k": 20,
    "epsilon": 0.1,
    "d_min" : 1,
    "d_max" : 80,
    "points_path" : "dataset/xaa.txt",
    "queries_path" : "dataset/readable.txt",
    "cluster_size" : 10000,
    "window_length" : 1000
}

from timeit import default_timer as timer
#run main()
from torch.utils.tensorboard import SummaryWriter

fws = SummaryWriter("./tmp/line", 'timecompute',filename_suffix='selective')

# fw = tf.summary.create_file_writer("./tmp/")
for k in range(10, 110, 10):
    prog_args["k"] = k
    start = timer()
    main(prog_args)
    end = timer()
    time = end - start
    fws.add_scalar("time", time, k)

    
