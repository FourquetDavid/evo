"""

@author: David
inspired by Telmo Menezes's work : telmomenezes.com
"""

import sys
import matplotlib
matplotlib.use('Agg')
import numpy as np
from multiprocessing import Pool
import network_evaluation as ne
import genetic_algorithm as ga
import warnings
import os
import random
np.seterr('ignore')

warnings.filterwarnings("ignore")
'''
This is the main file of the program :
it stores datas from the real network necessary to the chosen evaluation method
define the genetic algorithm and its grammar
and call it
'''






def main():

    number_of_nodes = int(sys.argv[1])
    name = sys.argv[2]
    resdir = sys.argv[3]
    #network_name = name.replace(".gexf","")
    network_name = name
    data_path = name
    #data_path = "data/"+network_name
    #res_path = "data/"+network_name+"_"+str(number_of_nodes)+"_u"
    
    #if not os.path.isfile(res_path+'_stats.txt'):
    if not os.path.exists(resdir):
        os.mkdir(resdir)
    results_path = resdir + "/result.xml" #sys.argv[3] #res_path+"_results.xml"
    stats_path = resdir + "/stats.txt" #res_path+'_stats.txt'
    dot_path = resdir + "/trees.jpeg"
    nb_generations = 40
    freq_stats = 5


    evaluation_method = "communities_degrees_distances_clustering_importance"
    tree_type = "with_constants"
    extension = ".gexf"
    multiprocessing = False
    dynamic = False



    print network_name
    network_type = "directed_unweighted"
    evaluation_method = "degrees_communities_distances_clustering_importance"

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
            extension=extension,
            number_of_nodes = number_of_nodes
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
    #files =[file for file in os.listdir("data") if ".gexf" in file]
#    files = [sys.argv[2]]
#    random.shuffle(files)
#   try :
#        multiproc = sys.argv[2]
#    except :
#        multiproc = False

#    if not multiproc :
#        for file in files :
    main()
#    else :

#        pool = Pool(16)
#        pool.map(main, files)
#        pool.close()
