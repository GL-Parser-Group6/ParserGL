import sys
import os
import re
import xml.etree.cElementTree as ET

def function_ecriture(L,add):
    """
        Ecrit la sortie du parseur
    """
    addf=os.path.join(add, L[0]+".txt")
    with open(addf,"w", encoding="utf8", errors="ignore") as file :
        for i in L:
            file.write(i+"\n")

def function_exportXML(L,add):
    addf=os.path.join(add, L[0]+".xml")
    article = ET.Element("article")
    ET.SubElement(article, "preamble").text = L[0]
    ET.SubElement(article, "titre").text = L[1]
    ET.SubElement(article, "auteur").text = L[2]
    ET.SubElement(article, "abstract").text = L[3]
    ET.SubElement(article, "biblio").text = L[4]
    export = ET.ElementTree(article)
    export.write(addf, encoding="utf8")

def readLines(fileName):
    """
        Lit un fichier en retournant une liste de ses lignes
    """
    with open(fileName, "r", encoding="utf8", errors='ignore') as file:
        return [i.replace("\n", "") for i in file.readlines()]

def parseurAbstract(List):
    """
        Récupère le résumé de l'article
    """

    containAbstract = False
    abstract = ""

    for x in List:
        if(containAbstract):
            if x == '1' or x.startswith('Introduction'):
                break
            abstract += x
        if(re.search('Abstract|In the article',x)!=None):
            containAbstract = True
            s = re.split('Abstract|In the article',x)
            if(s[1]!=None):
                abstract += s[1]
                
    return abstract

def references(liste):
    biblio = ""
    inBiblio = False
    
    for i in liste:
        if inBiblio and len(i) > 3:
            biblio += i
        if("References" in i or "REFERENCES" in i or "R EFERENCES" in i and len(i) <=11):
            if len(i) > 3:
                biblio += i
            inBiblio = True
                
    return biblio

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Usage : python "+sys.argv[0]+" <-t|-x> <directory>")
    else:
        type_export = sys.argv[1]
        directory = sys.argv[2]
        if type_export != "-t" and type_export != "-x":
            print("Usage : python "+sys.argv[0]+" <-t|-x> <directory>")
        else:
            if os.path.exists(os.path.join(directory, "output")):
                shutil.rmtree(os.path.join(directory, "output"))
            os.makedirs(os.path.join(directory, "output"))
            for f in os.listdir(directory):
                path = os.path.join(directory, f)
                if os.path.isfile(path) and f.split(".")[-1] == "txt":
                    lines = readLines(path)
                    print("Traitement :",f)
                    content = [".".join(f.split(".")[:-1]), recup_titre(lines), recup_auteur(lines), parseurAbstract(lines), references(lines)]
                    if type_export == "-t":
                        function_ecriture(content, os.path.join(directory, "output"))
                    else:
                        function_exportXML(content, os.path.join(directory, "output"))