import subprocess
import networkx as nx
import csv
import math
from lxml import etree
import os
import random


def write_edgelist():
    graphe = nx.read_gexf(path_to_file + ".gexf")
    if type(graphe) == nx.MultiDiGraph:
        print 'has_multiple_edges'
        graphe = nx.DiGraph(graphe)
    if type(graphe) == nx.MultiGraph:
        print 'has_multiple_edges'
        graphe = nx.Graph(graphe)

    for source, target in graphe.edges():
        graphe[source][target].clear()
        graphe[source][target]['weight'] = 1

    nx.write_weighted_edgelist(nx.convert_node_labels_to_integers(graphe), path_to_file + ".txt")


def write_motifs():
    if network['is_directed'] == 'True':
        print 'directed'
        if int(network['nb_edges']) > 100000:
            subprocess.call(["./mfinder1.21/mfinder", path_to_file + ".txt",
                             "-omat", "-s", "3", "-f", path_to_file + "_3", "-q", "-p", "5000"])
        else:
            subprocess.call(["./mfinder1.21/mfinder", path_to_file + ".txt",
                             "-omat", "-s", "3", "-f", path_to_file + "_3", "-q"])
    else:
        print 'undirected'
        if int(network['nb_edges']) > 100000:
            subprocess.call(["./mfinder1.21/mfinder", path_to_file + ".txt",
                             "-nd", "-omat", "-s", "3", "-f", path_to_file + "_3", "-q", "-p", "1001"])
            subprocess.call(["./mfinder1.21/mfinder", path_to_file + ".txt",
                             "-nd", "-omat", "-s", "4", "-f", path_to_file + "_4", "-q", "-p", "1001"])
        else:

            subprocess.call(["./mfinder1.21/mfinder", path_to_file + ".txt",
                             "-nd", "-omat", "-s", "3", "-f", path_to_file + "_3", "-q"])
            subprocess.call(["./mfinder1.21/mfinder", path_to_file + ".txt",
                             "-nd", "-omat", "-s", "4", "-f", path_to_file + "_4", "-q"])


def add_results(name_global, name_local, key_name, value_name, dictionnaire):
    print "adding_results", name_global, dictionnaire
    if not os.path.isfile(path_to_file + "_results.xml"):
        results = etree.Element('results')
        tree = etree.ElementTree(results)
    else:
        tree = etree.parse(path_to_file + "_results.xml")
        results = tree.getroot()
        try:
            results.remove(results.find(name_global))
        except TypeError:
            pass

    nouvel_element = etree.Element(name_global)
    results.append(nouvel_element)
    for key, value in dictionnaire.items():
        local_element = etree.Element(name_local)
        local_element.attrib[key_name] = str(key)
        local_element.attrib[value_name] = str(value)
        nouvel_element.append(local_element)
    f = open(path_to_file + "_results.xml", "w")
    tree.write(f, pretty_print=True)


def analyse_motifs():
    motifs_dict = {}
    if network['is_directed'] == 'True':
        with open(path_to_file + "_3_MAT.txt") as mat_file_3:
            for line in mat_file_3:
                linesplit = line.split(' ')
                if float(linesplit[2]) != 0:
                    numero = int(linesplit[0])
                    zscore = float(linesplit[4])
                    motifs_dict[numero] = zscore
    else:
        with open(path_to_file + "_3_MAT.txt") as mat_file_3:
            for line in mat_file_3:
                linesplit = line.split(' ')
                if float(linesplit[2]) != 0:
                    numero = int(linesplit[0])
                    nreal = int(linesplit[1])
                    nrand = float(linesplit[2])
                    srp = (nreal - nrand) / (nreal + nrand + 4)
                    motifs_dict[numero] = srp

        with open(path_to_file + "_4_MAT.txt") as mat_file_4:
            for line in mat_file_4:
                linesplit = line.split(' ')
                if float(linesplit[2]) != 0:
                    numero = int(linesplit[0])
                    nreal = int(linesplit[1])
                    nrand = float(linesplit[2])
                    srp = (nreal - nrand) / (nreal + nrand + 4)
                    motifs_dict[numero] = srp
    total = math.sqrt(sum([i ** 2 for i in motifs_dict.values()]))
    for key in motifs_dict:
        motifs_dict[key] /= total
    add_results("motifs", "motif", "number", "milo_score", motifs_dict)


def analysed():
    try:
        tree = etree.parse(path_to_file + "_results.xml")
        print "parsed"
        return tree.getroot().find("motifs") is not None
    except IOError:
        return False


with open("../work/done.csv") as csvfile:
    network_dict = csv.DictReader(csvfile, delimiter=";")
    number = 0
    for network in network_dict:
        print network['name']
        path_to_file = "../work/files/" + network['number'] + "-" + network['name'] + "/" + network['name']
        if int(network['nb_nodes']) < 1000 and not analysed() and 'Facebook' not in network['name']:
            print number
            number += 1
            try:
                write_edgelist()
                write_motifs()
                analyse_motifs()
            except IOError:
                pass
