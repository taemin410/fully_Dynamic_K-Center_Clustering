from algo_sliding import *
from algo_fully_adv import *
from algo_trajectories import *
from data_sliding import sliding_import_points
from data_fully_adv import *
from query import *


def sliding_k_center(prog_args):

    array = sliding_import_points("../dataset/timestamped_gps_coordinate.txt" , 10)

    print("Import ended! ")
    nb_instances=int()
    size = int()
    array=None

    levels = Sliding_level(array=array)
    sliding_initialise_levels_array(levels, prog_args["k"], prog_args["epsilon"], prog_args["d_min"],
					prog_args["d_max"], nb_instances, array, size)

    sliding_k_center_run(levels, nb_instances)

    

def fully_adv_k_center(prog_args):
    array = fully_adv_import_points(prog_args["points_path"])

    queries = query_provider("path", "fd", 100, 0, 0)

    nb_instances=int()
    size = int()
    array=None
    helper_array = None
    clusters_array=[]

    queries.initialise_query_provider(prog_args["queries_path"])
    if prog_args["cluster_size"] == 0:
        prog_args["cluster_size"] = size

    fully_adv_initialise_level_array(clusters_array, prog_args["k"],
                                    prog_args["epsilon"], prog_args["d_min"],
                                	prog_args["d_max"],nb_instances, array,
                                    size, prog_args["cluster_size"], helper_array)

    fully_adv_k_center_run(clusters_array, nb_instances, queries, helper_array)


prog_args={
    "k": 5,
    "epsilon": 0.01,
    "d_min" : 3,
    "d_max" : 10,
    "points_path" : "1.log",
    "queries_path" : "queries.dat",
    "cluster_size" : 2
}

sliding_k_center(prog_args)

# fully_adv_k_center(prog_args)



# void sliding_k_center(struct program_args *prog_args)
# {
# 	Sliding_level *levels;
# 	void *array;
# 	unsigned int size, nb_instances;
# 	sliding_import_points(&array, &size, prog_args->points_path,
# 			      prog_args->window_length);
# 	printf("import ended!\n");
# 	sliding_initialise_levels_array(&levels, prog_args->k,
# 					prog_args->epsilon, prog_args->d_min,
# 					prog_args->d_max, &nb_instances, array,
# 					size);
# 	sliding_k_center_run(levels, nb_instances);
# 	free(array);
# 	sliding_delete_levels_array(levels, nb_instances);
# }
#
# void fully_adv_k_center(struct program_args *prog_args)
# {
# 	Fully_adv_cluster *clusters_array;
# 	void *array;
# 	struct query_provider queries;
# 	unsigned int size, nb_instances;
# 	unsigned int *helper_array;
# 	fully_adv_import_points(&array, &size, prog_args->points_path);
# 	printf("import ended!\n");
# 	initialise_query_provider(&queries, prog_args->queries_path);
# 	if (0 == prog_args->cluster_size)
# 		prog_args->cluster_size = size;
# 	fully_adv_initialise_level_array(&clusters_array, prog_args->k,
# 					 prog_args->epsilon, prog_args->d_min,
# 					 prog_args->d_max, &nb_instances, array,
# 					 size, prog_args->cluster_size,
# 					 &helper_array);
# 	fully_adv_k_center_run(clusters_array, nb_instances, &queries,
# 			       helper_array);
# 	free(array);
# 	fully_adv_delete_level_array(clusters_array, nb_instances,
# 				     helper_array);
# 	free_query_provider(&queries);
# }
#
# void packed_k_center(struct program_args *prog_args)
# {
# 	Packed_level *levels;
# 	void *array;
# 	struct query_provider queries;
# 	unsigned int size, nb_instances;
# 	packed_import_points(&array, &size, prog_args->points_path);
# 	printf("import ended!\n");
# 	initialise_query_provider(&queries, prog_args->queries_path);
# 	packed_initialise_levels_array(&levels, prog_args->k,
# 				       prog_args->epsilon, prog_args->d_min,
# 				       prog_args->d_max, &nb_instances, array,
# 				       size);
# 	packed_k_center_run(levels, nb_instances, &queries);
# 	free(array);
# 	packed_free_levels_array(levels, nb_instances);
# 	free_query_provider(&queries);
# }
#
# void trajectories_k_center(struct program_args *prog_args)
# {
# 	Trajectory_level *clusters_array;
# 	Trajectory *array;
# 	struct query_provider queries;
# 	unsigned int size, *helper_array, nb_instances;
# 	trajectories_import_points(&array, &size, prog_args->points_path);
# 	printf("import ended!\n");
# 	initialise_query_provider(&queries, prog_args->queries_path);
# 	trajectories_initialise_level_array(&clusters_array, prog_args->k,
# 					    prog_args->epsilon,
# 					    prog_args->d_min, prog_args->d_max,
# 					    &nb_instances, array, size,
# 					    &helper_array);
# 	trajectories_k_center_run(clusters_array, nb_instances, &queries,
# 				  helper_array);
# 	trajectories_delete_level_array(clusters_array, nb_instances,
# 					helper_array);
# 	free_query_provider(&queries);
# 	trajectories_delete_points(array);
# }
#
# void trajectories_parallel_k_center(struct program_args *prog_args)
# {
# 	Trajectory *array;
# 	struct query_provider queries;
# 	unsigned int size;
# 	trajectories_import_points(&array, &size, prog_args->points_path);
# 	printf("import ended!\n");
# 	initialise_query_provider(&queries, prog_args->queries_path);
# 	trajectories_parallel_initialise_level_array(prog_args->k,
# 						     prog_args->epsilon,
# 						     prog_args->d_min,
# 						     prog_args->d_max,
# 						     array, size,
# 						     prog_args->nb_thread);
# 	trajectories_parallel_k_center_run(&queries);
# 	trajectories_parallel_delete_level_array();
# 	free_query_provider(&queries);
# 	trajectories_delete_points(array);
# }
#
# int main(int argc, char *argv[])
# {
# 	struct program_args prog_args;
# 	srand48(time(NULL));
# 	srand((unsigned int)time(NULL));
# 	if (parse_options(argc, argv, &prog_args))
# 		return 0;
# 	if (prog_args.long_log)
# 		enable_long_log(prog_args.log_file);
# 	else
# 		enable_log(prog_args.log_file);
# 	switch (prog_args.algo) {
# 	case SLIDING_K_CENTER:
# 		printf("Sliding window algorithm chosen\n");
# 		sliding_k_center(&prog_args);
# 		break;
# 	case FULLY_ADV_K_CENTER:
# 		printf("Fully adversary algorithm chosen\n");
# 		fully_adv_k_center(&prog_args);
# 		break;
# 	case PACKED_K_CENTER:
# 		printf("Packed fully adversary algorithm chosen\n");
# 		packed_k_center(&prog_args);
# 		break;
# 	case TRAJECTORIES_K_CENTER:
# 		printf("Trajectories fully adversary algorithm chosen\n");
# 		if (prog_args.parallel)
# 			trajectories_parallel_k_center(&prog_args);
# 		else
# 			trajectories_k_center(&prog_args);
# 		break;
# 	default:
# 		fprintf(stderr, "Unknow algorithm\n");
# 		return EXIT_FAILURE;
# 	}
# 	disable_log();
# 	if (has_time_log())
# 		disable_time_log();
# 	return EXIT_SUCCESS;
# }
