# Projet-Python-V2
![GitHub contributors](https://img.shields.io/github/contributors/Gabe-MGNT/Projet-Python-V2?label=Contributeur)

---
# Sommaire :
1. [Guide Utilisateur ](#user)
2. [Guide développeur ](#dev)
3. [Analyse résultat ](#analyse)

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
<p>Qui récupèrera le fichier en .csv et celui en .json</p>
<br>
<p>Une fois le projet cloné, les packages requis installés, les données récupérées, le projet s'éxécute tel que :</p>
<code>
$ python main.py
</code>
<br>
<p>Et le dashboard peut s'afficher en cliquant sur le lien d'hébergement local.</p>



### Utilisation
<p>Le projet vous permet d'intéragir avec différents graphiques.</p>
<p>Il y a des sliders permettant de changer l'intervalle temporel, l'année et des menus pour choisir les pays dont l'on souhaite visionner les données.</p>

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

<p>main.py reste inchangé et permet juste l'exécution du dashboard depuis la racine du projet.</p>



<a name="analyse"></a>
# Analyse des résultats

<p>Ce dashboard a pour but d'exploiter les données sur le chomage en France et d'en tirer une analyse.</p>

<p>Le chomage de manière générale semble n'avoir fait qu'augmenter jusqu'à 2018 pour redescendre en 2020, qui semblait repartir sur une bonne lancée, mais l'arrivée de la crise du COVID en 2021 à bousculer cet équilibre.</p>
<p>A ce moment l'économie française est au ralenti, et beaucoup de personnes ne peuvent plus travailler, c'est pour cela qu'on observe une augmentation du chomage en général à ce moment-là, et toute la France ressent les effets de cette crise.</p>

<p>Ensuite la carte nous permet de voir que les régions les plus affectées en temps normal se situe en dehors de la couronne parisienne, et que donc le chômage semble être plus élevé dans le reste de la France et principalement dans le centre, le Sud et le Nord.</p>
<p>Par contre, lors du COVID c'est finalement cette couronne parisienne qui a été le plus touché, de par la concentration de population qui y est installé, c'était donc la région la plus fragile à de tels bousculements.</p>

<p>Et en se penchant sur l'évolution temporelle des relevés, grâce aux tendances on peut y distinguer les plus gros chocs des ces dernières années : la crise 2008 et la crise Covid.</p>
<p>Mais aussi voir l'entrée en vigueur de la loi travail en 2015, qui montre avoir eu un certains impacts sur un chômage dont la France n'arrivait pas à se débarrasser depuis la crise de 2008.</p>

---




