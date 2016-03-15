import csv
from lxml import etree
import random

with open("../work/done.csv") as csvfile:
    network_dict = csv.DictReader(csvfile, delimiter=";")
    for network in network_dict:
        try:
            if int(network['nb_nodes']) < 1000 :
                path_to_file = "../work/files/" + network['number'] + "-" + network['name'] + "/" + network['name']
                parser = etree.XMLParser(remove_blank_text=True)
                tree = etree.parse(path_to_file + "_results.xml",parser)
                results = tree.getroot()
                try :
                    results.remove(results.find("gen"))
                except TypeError :
                    pass
                gen_element = etree.Element("gen")
                results.append(gen_element)
                milo = results.find("category").get("type")
                gen_classe =0
                if milo in ['Animal','HumanSocial','HumanContact','Misc','Lexical','Communication']:
                    if random.random() < 0.7 :
                        gen_classe = 1
                    else :
                        gen_classe = 2

                if milo in ['Metabolic','Interaction','Trophic']:
                    if random.random() < 0.8 :
                        gen_classe = 4
                    else :
                        gen_classe = 2

                if milo in ['Infrastructure',]:
                    if random.random() < 0.9 :
                        gen_classe = 3
                    else :
                        gen_classe = 2

                if milo in ['Affiliation',]:
                    if random.random() < 0.8 :
                        gen_classe = 5
                    else :
                        gen_classe = 4


                local_element = etree.Element("classe_gen")
                local_element.attrib["classe"] = str(gen_classe)
                gen_element.append(local_element)
                f = open(path_to_file + "_results.xml", "w")
                print network['name']
                tree.write(f, pretty_print=True)


        except AttributeError:
            pass
