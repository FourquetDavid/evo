import subprocess
import networkx as nx
import csv
import math
from lxml import etree
import os
import multiprocessing
from collections import defaultdict
import matplotlib.pyplot as plt

def write_edgelist(path_to_file):
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


def write_motifs(network, path_to_file):
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


def add_results(name_global, name_local, key_name, value_name, dictionnaire, path_to_file):
    print "adding_results", name_global, dictionnaire
    if not os.path.isfile(path_to_file + "_results.xml"):
        results = etree.Element('results')
        tree = etree.ElementTree(results)
    else:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(path_to_file + "_results.xml", parser)
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


def analyse_motifs(network, path_to_file):
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
    add_results("motifs", "motif", "number", "milo_score", motifs_dict, path_to_file)

def plot(name,data):
    fig, ax = plt.subplots()
    ax.plot(data,'o-')
    ax.set_ylabel('Normalized Z-score')
    plt.ylim(-0.75, 0.75)
    plt.xlim(-0.5,len(data))
    plt.xticks([])
    plt.yticks([-0.5,0,0.5])
    plt.grid(True)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.spines['left'].set_position(('outward', 50))
    #plt.show()
    plt.savefig("../classes/png/"+name+'.png')
    plt.close()
    print name+".png"


def write_class_motifs(path_to_file, is_directed,name):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(path_to_file + "_results.xml", parser)
        motifs = tree.getroot().find("motifs")
        dictionnaire_motifs = defaultdict(int)
        for element in motifs.findall("classe_milo"):
            motifs.remove(element)
        for motif in motifs.findall("motif"):
            number = motif.get("number")
            milo_score = motif.get("milo_score")
            dictionnaire_motifs[number] = milo_score
    except IOError :
        return
    dm = dictionnaire_motifs
    numero_classe = 0
    def r(a):return round(float(dm.get(a,'0')),2)
    def m(a): return float(dm.get(a,'0'))
    if is_directed == 'True':



            if (m("6") < -0.2 and m("36") < -0.2
                and m("38") > 0.2):
                numero_classe = 1
            if (m("6") < 0 and m("36") < 0 and m("12") < 0 and m("74") < 0 and m("14") < 0 and m("78") < 0
                and m("38") > 0.05 and m("108") > 0.05 and m("46") > 0.05):
                numero_classe = 2
            if (m("6") > 0 and m("36") > 0 and m("12") > 0 and m("74") > 0 and m("14") > 0 and m("78") > 0
                and m("38") < 0 and m("98") < 0 and m("108") < 0 and m("46") < 0
                and m("102") < 0 and m("110") < 0 and m("238") < 0):
                numero_classe = 4
            if (m("6") < 0 and m("36") < 0 and m("12") < 0 and m("74") < 0 and m("14") < 0 and m("78") < -0.2
                and m("38") > 0 and m("98") > 0 and m("108") > 0 and m("46") > 0
                and m("102") > 0 and m("110") > 0 and m("238") > 0.1):
                numero_classe = 3

            if numero_classe == 0:
                print "d",r("6"),r("36"),r("12"),r("74"),r("14"),r("78"),r("38"),r("98"),r("108"),r("46"),r("102"),r("110"),r("238")


            plot(name,[r("6"),r("36"),r("12"),r("74"),r("14"),r("78"),r("38"),r("98"),r("108"),r("46"),r("102"),r("110"),r("238")])


    else:

            if (m("4382") < -0.05 and m("4698") < -0.05
                and m("4958") > 0.05 and m("13278") > 0.05 and m("31710") > 0.05) or r("238")>0.3:
                numero_classe = 6

            if (m("238")> 0.2 and m("4958") > 0.05 and m("13278") > 0.05 ):
                numero_classe = 5

            if (m("4698") < -0.05 and m("13260") < -0.05  and m("31710") > 0.05):
                numero_classe = 7

            if (m("4382") >0.05 and m("13260") > 0.05
                and m("4958") < -0.05 and m("13278") < -0.05 and m("31710") < -0.05) or r("238")<-0.3:
                numero_classe = 8
            if numero_classe ==0:
                print "u",r("4382"),r("4698"),r("4958"),r("13260"),r("13278"),r("31710")
                print "u",r("78"),r("238")


            plot(name,[r("4382"),r("4698"),r("4958"),r("13260"),r("13278"),r("31710")])

    local_element = etree.Element("classe_milo")
    local_element.attrib["classe"] = str(numero_classe)
    motifs.append(local_element)
    f = open(path_to_file + "_results.xml", "w")
    tree.write(f, pretty_print=True)



def analysed(path_to_file):
    try:
        tree = etree.parse(path_to_file + "_results.xml")
        # print "parsed"
        return tree.getroot().find("motifs") is not None
    except IOError:
        return False


with open("../work/done.csv") as csvfile:
    network_dict = csv.DictReader(csvfile, delimiter=";")


    def calc_network(network):

        path_to_file = "../work/files/" + network['number'] + "-" + network['name'] + "/" + network['name']
        if int(network['nb_nodes']) < 1000:
            if not analysed(path_to_file):

                try:

                    pass
                    #print network['name']
                    # write_edgelist(path_to_file)
                    # write_motifs(network,path_to_file)
                    # analyse_motifs(network,path_to_file)
                except IOError:
                    pass
            else:
                print network['name']
                # print network['is_directed']
                write_class_motifs(path_to_file, network['is_directed'],network['name'].replace("_","-"))


    # pool = multiprocessing.Pool(40)
    # pool.map(calc_network, network_dict)
    for network in network_dict:
        calc_network(network)
