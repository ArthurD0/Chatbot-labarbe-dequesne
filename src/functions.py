"""
Ce fichier contient les fonctionnalités demandés dans la première partie
"""

from src.base_functions import *
from src.tfidf_functions import *
from collections import OrderedDict
import os


def func1():
    # 1- Afficher la liste des mots les moins importants dans le corpus de document
    if not os.path.exists("./cleaned"):
        pre_traitement()

    directories = list_of_files("./cleaned", "txt")
    tdidf = computeTFIDF(directories)
    words = tdidf['words']
    matrice = tdidf['matrice']

    count = 0  # Compter le nombre de fois que tdidf est égale à 0
    no_importants = []  # Le tableau des mots moins importants

    for i in range(len(words)):
        count = 0
        for j in range(len(directories)):
            if matrice[i][j] == 0:
                count += 1

        # On retiens qu'un mot est moins important s'il apparaît dans moins d'un tiers de l'ensemble des fichiers
        if count <= len(directories)//3:
            no_importants.append(words[i])

    print("La liste des mots moins importants:")
    print(no_importants)


def func2():
    # Les mots avec le score le plus élévé
    if not os.path.exists("./cleaned"):
        pre_traitement()

    directories = list_of_files("./cleaned", "txt")
    tdidf = computeTFIDF(directories)
    words = tdidf['words']
    matrice = tdidf['matrice']

    maxi, i, j = 0, 0, 0
    actives = []

    for i in range(len(words)):
        for j in range(len(directories)):
            if maxi < matrice[i][j]:
                maxi = matrice[i][j]
                actives = [words[i]]
            elif maxi == matrice[i][j]:
                actives.append(words[i])

    print("Le(s) mot(s) avec le score elevé est(sont): ")

    for w in actives:
        print(w)


def func3():
    chirac_discours = ["Nomination_Chirac1.txt", "Nomination_Chirac2.txt"]

    directories = list_of_files("./cleaned", "txt")

    if not os.path.exists("./cleaned"):
        pre_traitement()

    wordDict = dict.fromkeys(set_of_words(directories), 0)

    for filename in chirac_discours:
        content = read_document("./cleaned/"+filename)
        wordCount = count_occurence(content)

        for word, val in wordCount.items():
            wordDict[word] += val

    sort = OrderedDict(
        sorted(wordDict.items(), key=lambda item: item[1], reverse=True))

    print("Les mots les plus répétés par Chirac sont:")
    for k, v in sort.items():
        if v >= 10:  # On affiche les mots qu'il a répété plus de 10 fois
            print(k)


def func4():
    if not os.path.exists("./cleaned"):
        pre_traitement()

    directories = list_of_files("./cleaned", "txt")
    files_with_nation = []

    max_occ = {"file": "", "val": 0}

    for filename in directories:
        content = read_document("./cleaned/"+filename)
        tab = content.split(" ")

        if "nation" in tab:
            files_with_nation.append(filename)
            wordDict = count_occurence(content)

            if max_occ["val"] < wordDict["nation"]:
                # On prend le fichier qui contient le plus nation et le nombre d'occurence
                max_occ["file"] = filename
                max_occ["val"] = wordDict["nation"]

    print("Le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation »:")
    pr_names = extract_name(files_with_nation)
    for n in pr_names:
        print(n)

    print()

    print("Le Présient qui l'a répété le plus de fois est:")
    pr = extract_name([max_occ['file']])
    print(pr[0])


def func5():
    if not os.path.exists("./cleaned"):
        pre_traitement()

    directories = list_of_files("./cleaned", "txt")

    for filename in directories:
        content = read_document("./cleaned/"+filename)
        tab = content.split(" ")
        found = ""

        if "climat" in tab:
            names = extract_name([filename])
            found = 'climat'
            break

        elif "écologie" in tab:
            names = extract_name([filename])
            found = 'écologie'
            break

    names = associate_names(names)[0]
    print("Le premier Président à avoir parler de %s est %s" % (found, names))


def func6():
    if not os.path.exists("./cleaned"):
        pre_traitement()

    directories = list_of_files("./cleaned", "txt")
    tdidf = computeTFIDF(directories)
    words = tdidf['words']
    matrice = tdidf['matrice']

    count = 0  # Compter le nombre de fois que tdidf est différent de 0
    all_words = []  # Le tableau des mots dits par tous les présidents

    for i in range(len(words)):
        count = 0
        for j in range(len(directories)):
            if matrice[i][j] > 0:
                count += 1
        # On retiens qu'un mot est moins important s'il apparaît dans moins d'un tiers de l'ensemble des fichiers
        if count != 0:
            all_words.append(words[i])

    print("Les mots que tous les présidents ont évoqué sont: ")
    for w in all_words:
        count = 0
        for filename in directories:
            content = read_document("./cleaned/"+filename)
            tab = content.split(" ")

            if w in tab:
                count += 1
        if count == len(directories):
            print(w)
