import math
from src.base_functions import list_of_files


def read_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def count_occurence(text):
    # Compter l'occurence des mots dans un texte
    tab = text.split(" ")
    directories = list_of_files("./cleaned", "txt")
    wordDict = dict.fromkeys(set_of_words(directories), 0)

    for word in tab:
        wordDict[word] += 1

    return wordDict


def set_of_words(directories):
    # Retourne l'ensemble des mots de tous les fichiers

    wordSet = set()

    for filename in directories:
        content = read_document("./cleaned/"+filename)
        tab = content.split(" ")
        wordSet = wordSet.union(set(tab))

    return wordSet


def computeTF(wordDict, tab):
    # Calcule TF
    tfDict = {}
    tabCount = len(tab)

    for word, count in wordDict.items():
        tfDict[word] = count/float(tabCount)

    return tfDict


def computeIDF(directories):
    N = len(directories)

    # Déterminons l'ensemble des mots
    wordSet = set_of_words(directories)

    IDFDict = dict.fromkeys(wordSet, 0)

    for filename in directories:
        content = read_document("./cleaned/"+filename)
        wordDict = count_occurence(content)

        for word, val in wordDict.items():
            if val > 0:
                IDFDict[word] += 1

    for word, val in IDFDict.items():
        IDFDict[word] = math.log10(N / float(val))

    return IDFDict


def computeTFIDF(directories):
    wordSet = set_of_words(directories)
    wordSetList = list(wordSet)
    wordSetList.sort()

    idfs = computeIDF(directories)

    tfidf = [[0]*len(directories) for _ in range(len(wordSet))]

    i, j = 0, 0

    for filename in directories:
        content = read_document("./cleaned/"+filename)
        wordDict = count_occurence(content)

        tf = computeTF(wordDict, content.split(" "))

        i = 0
        for word in wordSetList:
            tfidf[i][j] = tf[word] * idfs[word]
            i += 1
        j += 1

    return {"words": wordSetList, "matrice": tfidf, "directories": directories}


def transposer_matrice(m):
    # Transposer la matrice

    # Nombre de lignes et de colonnes de la matrice
    rows, cols = len(m), len(m[0])

    # Créer une nouvelle matrice transposée avec des dimensions inversées
    transpose = [[0 for _ in range(rows)] for _ in range(cols)]

    # Remplir la matrice transposée avec les éléments de la matrice d'origine
    for i in range(rows):
        for j in range(cols):
            transpose[j][i] = m[i][j]

    return transpose
