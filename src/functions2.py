from src.base_functions import *
from src.tfidf_functions import *
import math


def tokenizer_question(texte):
    # Tokenization de la question
    texte = only_traitement(texte)

    return texte.split(" ")


def intersect_question_corpus(question):
    directories = list_of_files("./cleaned", "txt")

    words_set = set_of_words(directories)

    question_set = set(tokenizer_question(question))

    return question_set.intersection(words_set)


def compute_TDIDF_question(question):
    directories = list_of_files("./cleaned", "txt")

    wordSet = set_of_words(directories)
    wordSetList = list(wordSet)
    wordSetList.sort()

    tfidf_corpus = computeTFIDF(directories)
    matrix = tfidf_corpus['matrice']

    # transposer la matrice
    matrix = transposer_matrice(matrix)

    # Calculer TF de la question
    token = tokenizer_question(question)

    intersect = intersect_question_corpus(question)
    wordDict = dict.fromkeys(wordSet, 0)

    for w in token:
        if w in intersect:
            wordDict[w] += 1
    # Calcul propement dit
    n = len(token)

    tfDict = {}

    for word, count in wordDict.items():
        tfDict[word] = count/float(n)

    idfs = computeIDF(directories)

    # Calcul tf-idf
    tfidf = [0]*len(wordDict)

    i = 0
    for word in wordSetList:
        tfidf[i] = tfDict[word] * idfs[word]
        i += 1

    return tfidf


def produit_scalaire(vecteur1, vecteur2):
    # Assurer que les deux vecteurs ont la même longueur
    if len(vecteur1) != len(vecteur2):
        raise ValueError("Les vecteurs doivent avoir la même longueur")

    # Calculer le produit scalaire
    resultat = sum(x * y for x, y in zip(vecteur1, vecteur2))

    return resultat


def norme_vecteur(vecteur):
    # Calculer la somme des carrés des composantes du vecteur
    somme_carres = sum(x**2 for x in vecteur)

    # Calculer la racine carrée de la somme des carrés
    norme = math.sqrt(somme_carres)

    return norme


def calcul_similarity(v1, v2):
    return produit_scalaire(v1, v2)/(norme_vecteur(v1)*norme_vecteur(v2))


def find_pertinent(matrix_corpus, matrix_question, filenames):
    # Trouver le nom du fichier avec plus de pertinence
    v = []
    for matrix in matrix_corpus:
        r = calcul_similarity(matrix, matrix_question)
        v.append(r)

    return filenames[max(range(len(v)), key=lambda i: v[i])]


def generer_reponse(question):
    directories = list_of_files("./cleaned", "txt")

    # TF IDF du corpus
    tfidf_corpus = computeTFIDF(directories)
    tfidf_corpus['matrice'] = transposer_matrice(tfidf_corpus['matrice'])

    # TF IDF de la question
    tfidf_question = compute_TDIDF_question(question)

    # Le fichier pertinent
    fichier = find_pertinent(tfidf_corpus['matrice'],
                             tfidf_question, tfidf_corpus['directories'])

    # Ensemble des mots du corpus
    wordSet = set_of_words(directories)
    wordSetList = list(wordSet)
    wordSetList.sort()

    # Le mot avec score élévé
    mot = wordSetList[max(range(len(tfidf_question)),
                          key=lambda i: tfidf_question[i])]

    print("Document pertinent retourné: "+fichier)
    print()
    print("Mot ayant le TF-IDF le plus élevé: "+mot)

    # Retrouver la réponse
    with open("./speeches/"+fichier) as f:
        texte = f.read()

    match = re.search(r'[^.]*\bclimat\b[^.]*\.',
                      texte, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(0)
    else:
        return ""


def affiner_reponse(question):
    # Liste de propositions non exhaustives
    question_starters = {
        "comment": "Après analyse, ",
        "pourquoi": "Car, ",
        "peux-tu": "Oui, bien sûr!"
    }

    starter = tokenizer_question(question)[0]
    res = generer_reponse(question)
    res.strip()

    if starter in question_starters.keys():
        return question_starters[starter] + res
    else:
        return res
