import sys
import os
import re

def function_ecriture(L,add):  # prend en arg avec une liste avec L[0]=nom L[1]=titre ...
    addf=os.path.join(add, L[0]+".txt")
    with open(addf,"w", encoding="utf8", errors="ignore") as file :
        for i in L:
            file.write(i+"\n")

def readLines(fileName):
    with open(fileName, "r", encoding="utf8", errors='ignore') as file:
        return [i.replace("\n", "") for i in file.readlines()]

def parseurAbstract(List):

    containAbstract = False
    abstract = ""

    for x in List:
        if(containAbstract):
            if(x == '1'):
                break
            abstract += x
        if(re.search('Abstract|In the article',x)!=None):
            containAbstract = True
            s = re.split('Abstract|In the article',x)
            if(s[1]!=None):
                abstract += s[1]
                
    return abstract

def recup_titre(liste):
    return liste[0]

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage : python "+sys.argv[0]+" <directory>")
    else:
        directory = sys.argv[1]
        os.makedirs(os.path.join(directory, "output"), exist_ok=True)
        for f in os.listdir(directory):
            path = os.path.join(directory, f)
            if os.path.isfile(path) and f.split(".")[-1] == "txt":
                lines = readLines(path)
                print("Traitement :", f)
                function_ecriture([".".join(f.split(".")[:-1]), recup_titre(lines), parseurAbstract(lines)], os.path.join(directory, "output"))

