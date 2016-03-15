import os
import networkx as nx
import csv
import test_networks as fil


konect = fil.getDataFromKonect()
snas =fil.getDataFromSnas()
print konect


with open('datas_networks.csv', 'w') as csvfile:
    fieldnames = ['name','nb_nodes','nb_edges','is_directed','is_multi','type','ref','density']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    files = "../work/files/"
    for dir in os.listdir(files):
        name = '-'.join(dir.split("-")[1:])
        network = nx.read_gexf(files+dir+"/"+name+".gexf")
        if network.number_of_nodes() <1000:
            dict_network={}
            dict_network['name'] = name
            dict_network['nb_nodes'] = network.number_of_nodes()
            dict_network['nb_edges'] = network.number_of_edges()
            dict_network['is_directed'] = network.is_directed()
            dict_network['is_multi'] = (type(network) in [nx.MultiGraph,nx.MultiDiGraph])
            dict_network['density']  = nx.density(network)
            print name
            try :
                cat = konect[name]["category"]
                dict_network['type']  = konect[name]["category"]
            except KeyError :
                pass
            writer.writerow(dict_network)








