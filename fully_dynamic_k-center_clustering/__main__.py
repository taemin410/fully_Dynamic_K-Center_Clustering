from algo_sliding import *
from algo_fully_adv import *
from algo_trajectories import *
from data_sliding import sliding_import_points
from data_fully_adv import *
from query import *

import sys
import argparse

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
    sliding_initialise_levels_array(levels, prog_args["k"], prog_args["epsilon"], prog_args["d_min"],
					prog_args["d_max"], nb_instances, array, size)

    sliding_k_center_run(levels, nb_instances)


def fully_adv_k_center(prog_args):

    nb_instances=int()
    size = int()
    array=None
    helper_array = None
    clusters_array = []


    size, array = fully_adv_import_points(prog_args["points_path"], prog_args['window_length'])

    queries = query_provider()


    queries.initialise_query_provider(prog_args["queries_path"])
    if prog_args["cluster_size"] == 0:
        prog_args["cluster_size"] = size

    fully_adv_initialise_level_array(clusters_array, prog_args["k"],
                                    prog_args["epsilon"], prog_args["d_min"],
                                	prog_args["d_max"],nb_instances, array,
                                    size, prog_args["cluster_size"], helper_array)

    fully_adv_k_center_run(clusters_array, nb_instances, queries, helper_array)


def arg_parse(prog_args):
    parser = argparse.ArgumentParser(description='Model selection')
    parser.add_argument('--sliding','-s', help="Run sliding window model", action='store_true' )
    parser.add_argument('--fullyadv','-f', help="Run sliding window model", action='store_true' )
    parser.add_argument('--packed','-p', help="Run sliding window model", action='store_true' )
    parser.add_argument('--trajectories','-t', help="Run sliding window model", action='store_true' )

    args = parser.parse_args()

    if args.sliding:
        print(parser.parse_args())
        sliding_k_center(prog_args)
    if args.fullyadv:
        print(parser.parse_args())
        fully_adv_k_center(prog_args)
    if args.packed:
        print()
    if args.trajectories:
        print()

def main():

    #
    #   INITIALIZE PROG_ARGS
    #
    prog_args={
        "k": 20,
        "epsilon": 0.1,
        "d_min" : 3,
        "d_max" : 10,
        "points_path" : "dataset/timestamped_gps_coordinate.txt",
        "queries_path" : "dataset/readable.txt",
        "cluster_size" : 2,
        "window_length" : 10
    }

    #
    #   READ USER INPUT  (DEFAULT path is set to dataset/timestamped_gps_coordinate.txt)
    #

    readpath = input("Path to the dataset (relative or full path) : ")
    window_length = input("if sliding window model Window length: ")

    if readpath:
        prog_args["points_path"]= readpath
    if window_length:
        prog_args["window_length"] = window_length


    #
    #   Run Argument parser
    #

    arg_parse(prog_args)

    print("Program terminates")

#run main()
main()
