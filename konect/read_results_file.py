import csv
from lxml import etree
from collections import defaultdict


with open("../work/done.csv") as csvfile:

    network_dict = csv.DictReader(csvfile, delimiter=";")
    dictionnaire_estrada = {}
    dictionnaire_milo = {}
    dictionnaire_milo_estrada ={}
    dictionnaire_gen_category ={}
    dictionnaire_gen_estrada ={}
    dictionnaire_gen_milo ={}
    dictionnaire_complet={}

    def add(dico,key,key2):
        if key not in dico :dico[key] ={}
        if key2 not in dico[key]: dico[key][key2] =0
        dico[key][key2]+=1


    for network in network_dict:
        try:
            if int(network['nb_nodes']) < 1000 :
                path_to_file = "../work/files/" + network['number'] + "-" + network['name'] + "/" + network['name']
                tree = etree.parse(path_to_file + "_results.xml")
                results = tree.getroot()
                category = str(results.find("category").get("type"))
                gen2 = results.find("gen")
                gen = str(gen2.find("classe_gen").get("classe"))

                #print gen
                add(dictionnaire_gen_category,gen,category)
            #if results.find("motifs") is not None or results.find("estrada_score") is not None :

                if results.find("estrada_score") is not None :
                    classe = str(results.find("estrada_score").find("classe").get("score"))

                    #print("['"+classe+"' , '"+category+"' , 1]")
                    add(dictionnaire_estrada,classe,category)
                    add(dictionnaire_gen_estrada,classe,gen)
                if  results.find("motifs") is not None:
                    milo = results.find("motifs").find("classe_milo")

                    if milo is not None :
                        milo_classe = str(milo.get("classe"))
                        add(dictionnaire_gen_milo,milo_classe,gen)
                        add(dictionnaire_milo,milo_classe,category)

                if results.find("motifs") is not None and results.find("estrada_score") is not None :
                    #print "1"
                    estrada_classe = str(results.find("estrada_score").find("classe").get("score"))
                    milo_classe = str(results.find("motifs").find("classe_milo").get("classe"))
                    add(dictionnaire_milo_estrada,milo_classe,estrada_classe)

                    dictionnaire_complet[network['name']]={}
                    dictionnaire_complet[network['name']]["ep"]=round(float(results.find("estrada_score").find("eplus").get("score")),2)
                    dictionnaire_complet[network['name']]["em"]=round(float(results.find("estrada_score").find("eminus").get("score")),2)
                    dictionnaire_complet[network['name']]["mclass"]=milo_classe
                    dictionnaire_complet[network['name']]["eclass"]=estrada_classe




        except AttributeError:
            pass
def print_pdf():
    for network,data in dictionnaire_complet.iteritems() :
            name = network.replace("_","-")
            print("\\tableline{"+name+"}{"+str(data["ep"])+"}{"+str(data["em"])+"}{"+data["eclass"]+"}{"+name+"}{"+data["mclass"]+"}\\\\")

def print_estrada():
    for classe,item in dictionnaire_estrada.iteritems() :
                for category,number in item.iteritems():
                    print("['"+category+"' , '"+classe+"' , "+str(number)+"],")

def print_milo():
    for classe,item in dictionnaire_milo.iteritems() :
                for category,number in item.iteritems():
                    print("['"+category+"' , '"+classe+"' , "+str(number)+"],")

def print_milo_estrada():
    for classe,item in dictionnaire_milo_estrada.iteritems() :
                for category,number in item.iteritems():
                    print("['"+category+"' , '"+classe+"' , "+str(number)+"],")

def print_2(dictionnaire):
    for classe,item in dictionnaire.iteritems() :
                for category,number in item.iteritems():
                    print("['"+category+"' , '"+classe+"' , "+str(number)+"],")

def print_gen():
    print_2(dictionnaire_gen_estrada)

    print_2(dictionnaire_gen_category)
    print_2(dictionnaire_gen_milo)

print_pdf()