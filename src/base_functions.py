
import os
import re


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def extract_name(filenames):
    # Cette fonction permettra d'extraire le nom des presidents
    # à partir des noms des fichers textes fournis
    pr_names = list()

    directory = "./speeches"
    files_names = filenames if filenames else list_of_files(directory, "txt")

    for name in files_names:
        match = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", name)

        if match:  # Si le match est trouvé
            pr_names.append(match.group(1))

    # On retourne un ensemble contenant les noms des présidents
    return pr_names


def associate_names(names):
    # Cette fonction permettra d'associer un prénom aux noms
    names_dict = {"Chirac": "Jacques Chirac", "Giscard dEstaing": "Valéry Giscard d’Estaing",
                  "Mitterrand": "François Mitterrand", "Macron": "Emmanuel Macron",
                  "Sarkozy": "Nicolas Sarkozy", "Hollande": "François Hollande"}

    association = []
    for name in names:
        association.append(names_dict[name])

    return association


def show_names():
    # Affichage des noms
    names = associate_names(extract_name())
    # print(names)
    names_without_doubles = set(names)
    print(names_without_doubles)


def only_traitement(content):
    content = content.lower()  # Ecriture en minuscule

    # Retrait des ponctuactions
    content = re.sub("[^\w\s'\-]", "", content)

    # Retrait des apostrophes entre les mots
    content = re.sub(r"'", " ", content)

    # Retrait du tiret entre les mots et remplacement par espace
    content = re.sub(r"\b-\b", " ", content)

    # Retrait du tiret et remplacement par le vide
    content = re.sub(r"-", "", content)

    content = re.sub(r"[\s]+", " ", content)  # Tokenisation

    content = content.strip()

    return content


def pre_traitement():
    # Création du nouveau dossier
    if not os.path.exists("./cleaned"):
        os.mkdir("./cleaned")

    src_directory = "./speeches"
    dst_directory = "./cleaned"

    files_names = list_of_files(src_directory, "txt")

    for f_name in files_names:
        with open(src_directory+"/"+f_name, encoding='utf-8') as f:
            content = f.read()

            # Traitement du texte
            with open(dst_directory+"/"+f_name, "w", encoding='utf-8') as fw:
                content = only_traitement(content)

                fw.write(content)
