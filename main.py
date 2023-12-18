from src.functions import *
from src.functions2 import *


if __name__ == '__main__':
    partie = 0
    while not 1 <= partie <= 2:
        partie = input("Choisir un mode:\n\n"
                       "1- Fonctionnalités de la partie 1\n"
                       "2- Mode Chatbot\n\n"
                       )
        try:
            partie = int(partie)
            if partie == 1:  # Tester les fonctionnalités
                choix = 0
                while not 1 <= choix <= 5:
                    choix = input("Choisir une fonctionnalité:\n\n"
                                  "1- Afficher les mots moins importants\n"
                                  "2- Afficher le(s) mot(s) avec le score TD-IDF elevé\n"
                                  "3- Afficher le(s) mot(s) le(s) plus répété(s) par le président Chirac\n"
                                  "4- Afficher le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois\n"
                                  "5- Afficher le premier président à parler du climat et/ou de l’écologie\n"
                                  )
                    try:
                        choix = int(choix)
                        if choix == 1:
                            func1()
                        elif choix == 2:
                            func2()
                        elif choix == 3:
                            func3()
                        elif choix == 4:
                            func4()
                        elif choix == 5:
                            func5()
                        else:
                            choix = 0
                    except:
                        choix = 0
            elif partie == 2:
                question = input("Entrez votre question: ")
                reponse = affiner_reponse(question)
                print("Reponse:")
                print()
                print(reponse)
        except:
            partie = 0
