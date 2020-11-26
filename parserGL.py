import sys
import os
import re

def function_ecriture(L,add):
    """
        Ecrit la sortie du parseur
    """
    addf=os.path.join(add, L[0]+".txt")
    with open(addf,"w", encoding="utf8", errors="ignore") as file :
        for i in L:
            file.write(i+"\n")

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

def recup_titre(liste):
    """
        Récupère le titre de l'article
    """
    is_in_title = False
    title = ""
    for i in liste:
        if is_in_title:
            print(re.search("[A-Z]\.", i))
            if len(i) == 0 or (len(i) == 1 and i[0].islower()) or "," in i or "∗" in i or "\\" in i or re.search("[A-Z]\.", i) != None:
                if len(i) == 0 and 2 <= len(title.split("\n")[-2].split(" ")) <= 3:
                    title = "\n".join(title.split("\n")[:-2])+"\n"
                break
            title += i + "\n"
        if len(i) > 0 and i[0].isupper() and title == "" and i.upper() != "LETTER" and not i.startswith("Communicated by"):
            is_in_title = True
            title += i + "\n"
    return title[:-1]

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Usage : python "+sys.argv[0]+" <-t|-x> <directory>")
    else:
        type_export = sys.argv[1]
        directory = sys.argv[2]
        if type_export != "-t" and type_export != "-x":
            print("Usage : python "+sys.argv[0]+" <-t|-x> <directory>")
        else:
            os.makedirs(os.path.join(directory, "output"), exist_ok=True)
            for f in os.listdir(directory):
                path = os.path.join(directory, f)
                if os.path.isfile(path) and f.split(".")[-1] == "txt":
                    lines = readLines(path)
                    print("Traitement :", f)
                    if type_export == "-t":
                        function_ecriture([".".join(f.split(".")[:-1]), recup_titre(lines), parseurAbstract(lines)], os.path.join(directory, "output"))
                    else:
                        function_ecriture([".".join(f.split(".")[:-1]), recup_titre(lines), parseurAbstract(lines)], os.path.join(directory, "output"))