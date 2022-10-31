# Projet-Python-V2
![GitHub contributors](https://img.shields.io/github/contributors/Gabe-MGNT/Projet-Python-V2?label=Contributeur)

---
# Sommaire :
1. [Guide Utilisateur ](#user)
2. [Analyse résultat ](#analyse)
3. [Guide développeur ](#dev)
---
<br>

<a name="user"></a>
# Guide Utilisateur


### Présentation
<p>Voici un dashboard permettant de visualiser l'évolution du chômage dans les zones d'emplois entre 2003 et 2022.</p>
<p>Ce projet utilise des données fournies par l'INSEE</p>

<br>

### Données utilisées 
<p>Les données utilisées pour étudier le chômage proviennent de l'INSEE, accessible depuis ce lien : <a>https://www.insee.fr/fr/statistiques/fichier/1893230/chomage-zone-t1-2003-t2-2022.xlsx</a>
</p>
<p>Pour ce qui est des données géolocalisées, on les récupère avec ce lien : <a>https://www.insee.fr/fr/statistiques/fichier/4652957/fonds_ze2020_2022.zip</a>
Ainsi, nous ferons le lien entre ces 2 fichiers plus tard dans les scripts python.</p>

<br>

### Installation
<p>Pour installer ce projet, il faut cloner le projet à l'aide de la commande</p>
<br>
<code>
$ git clone URLProjet
</code>
<br>
<p>Ensuite, il faut d'abord installer les packages additionnels requis contenus dans requirement.txt, avec la commande :</p>
<br>
<code>
$ python -m pip install -r requirements.txt
</code>

<br>

### Démarrage
<p>Avant de pouvoir l'éxécuter il faut récupérer les données statiques avec :</p>
<code>
$ python get_data.py
</code>
<br>
<p>Une fois le projet cloné, et les packages requis installé, le projet s'éxécute tel que :</p>
<code>
$ python main.py
</code>

<br>

### Utilisation
<p>Le projet vous permet d'intéragir avec différents graphiques.</p>

---

<a name="analyse"></a>
# Analyse des résultats
<p>Le chomage de manière générale semble n'avoir fait qu'augmenter jusqu'à 2018 pour redescendre en 2020.</p>
<p>L'arrivée de la crise du COVID en 2021 à bousculer cet équilibre.</p>

<p>De plus la carte permet de voir que les régions les plus affectées en temps normal se situe en dehors de la couronne parisienne</p>
<p>Par contre, lors du COVID c'est finalement cette couronne parisienne qui a été le plus touché.</p>

---
<a name="dev"></a>
# Guide développeur

<p>
Le code du projet est organisé tel que :
</p>
<br>- main.py : éxécute le dashboard
<br>- get_data.py : récupère les données depuis les urls connus.
<br>- /app/app.py : Contient les fichiers de déclarations des graphiques et de l'agencement visuel

<p>Si des modifications doivent être faites, cela se passe donc dans le fichier app.py</p>
<p>L'ajout et déclaration de graphique se fait au début du fichier.</p>
<p>L'ajout du graphique dans le dashbaord visuel, se fait dans la déclaration du layout </p>
<p>Et si un graphique nécessite une mise à jour, cela se fait donc à la fin dans les callbacks.</p>





