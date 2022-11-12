import requests

"""Récupère les donées depuis l'url"""
url = 'https://www.insee.fr/fr/statistiques/fichier/1893230/chomage-zone-t1-2003-t2-2022.xlsx'
r = requests.get(url, allow_redirects=True)

open('data/chomage-zone-t1-2003-t2-2022(copie de get_data).xlsx', 'wb').write(r.content)
