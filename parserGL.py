import sys
import os
import re
import xml.etree.cElementTree as ET
import shutil

def function_ecriture(L,add):
    """
        Ecrit la sortie du parseur
    """
    addf=os.path.join(add, L[0]+".txt")
    with open(addf,"w", encoding="utf8", errors="ignore") as file :
        for i in L:
            file.write(i+"\n")

def function_exportXML(L,add):
    """
        Export en XML
    """
    addf=os.path.join(add, L[0]+".xml")
    article = ET.Element("article")
    ET.SubElement(article, "preamble").text = L[0]
    ET.SubElement(article, "titre").text = L[1]
    ET.SubElement(article, "auteur").text = L[2]
    ET.SubElement(article, "abstract").text = L[3]
    ET.SubElement(article, "introduction").text = L[4]
    ET.SubElement(article, "corps").text = L[5]
    ET.SubElement(article, "conclusion").text = L[6]
    ET.SubElement(article, "discussion").text = L[7]
    ET.SubElement(article, "biblio").text = L[8]
    export = ET.ElementTree(article)
    export.write(addf, encoding="utf8")

def readLines(fileName):
    """
        Lit un fichier en retournant une liste de ses lignes
    """
    with open(fileName, "r", encoding="utf8", errors='ignore') as file:
        return [i.replace("\n", "") for i in file.readlines()]
        
def recup_titre(liste):
    """
        Récupère le titre de l'article
    """
    global debut_it
    debut_it = 0
    is_in_title = False
    title = ""
    for i in liste:
        if is_in_title:
            if len(i) == 0 or (len(i) == 1 and i[0].islower()) or "," in i or "∗" in i or "\\" in i or re.search("[A-Z]\.", i) != None:
                if len(i) == 0 and 2 <= len(title.split("\n")[-2].split(" ")) <= 3:
                    title = "\n".join(title.split("\n")[:-2])+"\n"
                break
            title += i + "\n"
        if len(i) > 0 and i[0].isupper() and title == "" and i.upper() != "LETTER" and not i.startswith("Communicated by"):
            is_in_title = True
            title += i + "\n"
        debut_it += 1
    return title[:-1]

def parseurAbstract(List):
    """
        Récupère le résumé de l'article
    """
    global fin_it
    fin_it = -1
    containAbstract = False
    abstract = ""

    for x in List:
        if(containAbstract):
            if x == '1' or x.startswith('Introduction'):
                break
            abstract += x + "\n"
        else:
            fin_it += 1
        if(re.search('Abstract|In the article',x)!=None):
            containAbstract = True
            s = re.split('Abstract|In the article',x)
            if(s[1]!=None):
                abstract += s[1] + "\n"
    return abstract[:-1]


def recup_auteur(liste):
    """
        Récupère les auteurs et leur adresse de l'article
    """
    final_String = ''
    recup_titre(liste)
    parseurAbstract(liste)
    for i in range(debut_it, fin_it):
        final_String += liste[i] + "\n"
    return final_String[:-1]

def references(liste):
    """
        Récupère la bibliographie de l'article
    """
    biblio = ""
    inBiblio = False
    
    for i in liste:
        if inBiblio and len(i) > 3:
            biblio += i + "\n"
        if("References" in i or "REFERENCES" in i or "R EFERENCES" in i and len(i) <=11):
            if len(i) > 3:
                biblio += i + "\n"
            inBiblio = True
                
    return biblio[:-1]

def menu(directory):
    files = []
    files_dir = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory, i)) and i.split(".")[-1] == "txt"]
    while True:
        print("\nFichiers :")
        for i, f in enumerate(files_dir):
            print(i+1,"-", f, ("- Selectionné" if f in files else ""))
        print(i+2, "- Lancer le parser")
        try:
            choix = int(input("Choix : "))
        except:
            choix = -1
        if choix == i+2:
            return files
        elif 0 < choix < i+2:
            if files_dir[choix-1] in files:
                files.remove(files_dir[choix-1])
            else:
                files.append(files_dir[choix-1])

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
            for f in menu(directory):
                path = os.path.join(directory, f)
                lines = readLines(path)
                print("Traitement :",f)
                content = [".".join(f.split(".")[:-1]), recup_titre(lines), recup_auteur(lines), parseurAbstract(lines), "", "", "", "", references(lines)]
                if type_export == "-t":
                    function_ecriture(content, os.path.join(directory, "output"))
                else:
                    function_exportXML(content, os.path.join(directory, "output"))