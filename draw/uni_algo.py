"""

@author: David
inspired by Telmo Menezes's work : telmomenezes.com
"""

import sys
import numpy as np

import network_evaluation as ne
import genetic_algorithm as ga
import warnings
np.seterr('ignore')

warnings.filterwarnings("ignore")
'''
This is the main file of the program :
it stores datas from the real network necessary to the chosen evaluation method
define the genetic algorithm and its grammar
and call it
'''





def main():
    arguments = sys.argv
    network_name = arguments[1]
    is_directed = arguments[2]
    network_number = arguments[3]
    data_path = arguments[4] #data_path = "../work/files/" + network_number + "-" + network['name'] + "/" + network['name']
    results_path = data_path+"_results.xml"
    stats_path = data_path+'_stats.txt'
    dot_path = data_path+'_trees.jpeg'
    nb_generations = arguments[5]
    freq_stats = arguments[6]


    #evaluation_method = "communities_degrees_distances_clustering_importance"
    tree_type = "with_constants"
    extension = ".gexf"
    multiprocessing = False
    dynamic = False



    print network_name
    if is_directed == "True" :
        network_type = "directed_unweighted"
        evaluation_method = "degrees_distances_clustering_importance"
    else :
        network_type = "undirected_unweighted"
        evaluation_method = "communities_degrees_distances_clustering_importance"

    ne.get_datas_from_real_network(data_path,
                           results_path,
                           name=network_name,
                           evaluation_method=evaluation_method,
                           dynamic=dynamic)



    genome = ga.new_genome(
        results_path,
        name=network_name,
        data_path=data_path,
        evaluation_method=evaluation_method,
        dynamic=dynamic,
        tree_type=tree_type,
        network_type=network_type,
        extension=extension
    )

                # optional arguments for evolve :
                # *nb_generations : number of generations of the evolution
                #                   possible values : int > 0 : default : 100
                # *freq_stats : number of generations between two prints of statistics
                #                   possible values : int > 0 : default : 5
                # *stats_path : path to the file where the stats will be printed
                # *multiprocessing : will use or not multiprocessing
                #                possible values : True False


    ga.evolve(genome, stats_path=stats_path, dot_path=dot_path, nb_generations=nb_generations, freq_stats=freq_stats,
        multiprocessing=multiprocessing)


if __name__ == "__main__":
    main()
