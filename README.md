# Projet : Modélisation de la vitesse de désorbitation d'un satellite en LEO doté d'un frein électromagnétique.

Ce projet a pour objectif d'estimer le temps de désorbitation d'un satellite en orbite basse terrestre en considérant les forces de traînée 
atmosphérique et électromagnétique agissant sur le satellite. Le dispositif considéré pour bénéficier de la traînée électromagnétique est 
décrit par l'article [1].

## Documentation
Toute la documentation nécessaire pour comprendre la structure des modules est disponible dans l'onglet `docs` de ce dépot GitHub.
Il suffit d'ouvrir le fichier `index.html` du dossier dans `docs/_build/html`.

## Dépendances 
L'exécution du programme necessite l'installation des bibliothèques suivantes :
- pandas
- matplotlib
- openpyxl
- ai.cs
- ppigrf
- numpy
- PyYAML
- tqdm

Elles peuvent être installées automatiquement à l'aide de la commande :  
``pip install -r requirements.txt``

## Utilisation 
Avant d'exécuter le programme à partir du fichier 'main.py', il est nécessaire d'entrer les paramètres de la simulation dans le 
fichier 'data.yaml' en précisant les caractéristiques du satellite et de l'antenne électromagnétique (masse, longueur, cx, etc). 
Ensuite, l'utilisateur doit indiquer les paramètres de l'orbite initiale ainsi qu'une date pour bénéficier d'un modèle atmosphérique 
et magnétique fidèle à la réalité. Enfin, il suffit d'indiquer dans la console l'approche souhaitée pour la réalisation des calculs 
(énergétique ou basée sur le PFD).

### Objet SpaceBody :
Le premier objet de cette librairie est 
L'objet `SpaceBody` est une classe de base utilisée dans la bibliothèque Astraios pour représenter divers corps célestes
tels que les planètes, les satellites et d'autres éléments naturels ou artificiels en orbite. Cette classe contient 
notamment un argument `mass` qui représente la masse du corps. Seuls les corps célestes de type 'SpaceBody' peuvent utiliser 
la méthode Two_body_problem().

#### Planet 
La sous-classe `Planet` hérite de `SpaceBody` et est utilisée pour représenter spécifiquement une planète dans le système. 
En plus de la masse héritée, cette classe a des attributs supplémentaires tels que `radius` pour le rayon de la planète 
en mètres et `color` pour la couleur utilisée dans les visualisations.

#### Satellite 
La sous-classe `Satellite` hérite également de `SpaceBody` et est utilisée pour représenter un satellite en orbite autour
d'une planète ou d'une autre entité céleste. En plus de la masse héritée, cette classe a des attributs supplémentaires 
tels que `cx` pour le coefficient de traînée sans dimension et `surface` pour la surface transversale du satellite en mètres carrés.
Habituellement, un satellite possède un coefficient de traînée de 2 si il n'a pas été évalué lors de la phase de conception.

### Objet Orbit : 
L'objet `Orbit` est une classe centrale dans la bibliothèque Astraios qui permet de modéliser les orbites elliptiques 
autour d'un corps céleste, tel que la Terre. Cette classe est utilisée pour définir les paramètres d'une orbite, effectuer
des manoeuvres orbitales et simuler la désorbitation d'un satellite. Toute étape du programme nécessitant des calculs (trajectoire,
vitesse) doit utiliser cet objet et ces méthodes.

#### init() 
Le constructeur de la classe `Orbit` permet d'initialiser un objet orbite avec les paramètres spécifiés :
- `perigee` : Altitude du périgée en mètres.
- `apogee` : Altitude de l'apogée en mètres.
- `inclinaison` : Inclinaison de l'orbite en degrés (par défaut 0).
- `dt` : Intervalle de temps pour la simulation en secondes (par défaut 1000).
- `temps_simu` : Durée de la simulation en secondes (par défaut 800000).

#### plot_orbit()
Cette méthode permet de tracer l'orbite elliptique dans un système de coordonnées tridimensionnel. Elle affiche également le périgée et l'apogée de l'orbite.

#### manoeuvre()
La méthode `manoeuvre` permet d'effectuer une manoeuvre orbitale en modifiant la vitesse orbitale du satellite. Les paramètres de la manoeuvre sont spécifiés comme suit :
- `delta_v` : Changement de vitesse en mètres par seconde.
- `direction` : Direction de la manoeuvre ('prograde', 'retrograde' ou 'radiale').
- `position` : Position de la manoeuvre ('perigee' ou 'apogee').

#### desorbitation()
La méthode `desorbitation` simule la désorbitation du satellite en orbite. Elle calcule la trajectoire du satellite en tenant compte de la force gravitationnelle, de la traînée atmosphérique et éventuellement d'une propulsion supplémentaire. Les paramètres de la désorbitation sont spécifiés comme suit :
- `satellite` : Instance de la classe `Satellite` représentant le satellite en orbite.
- `position` : Position de la manoeuvre de désorbitation ('perigee' ou 'apogee').
- `atmosphere` : Instance de la classe `Atmosphere` représentant l'atmosphère terrestre.
- `plot_orbit` : Optionnel, si True, affiche la trajectoire du satellite en orbite (par défaut False).
- `force_propulsion` : Optionnel, force de propulsion supplémentaire en newtons (par défaut 0).

### Objet Atmosphere :
L'objet `Atmosphere` est une classe utilisée dans la bibliothèque Astraios pour modéliser l'atmosphère terrestre. 
Cette classe fournit des fonctionnalités pour calculer la température et la densité de l'air à différentes altitudes.
Ce modèle d'atmosphère utilise principalement celui de Jacchia-Lineberry [1].

#### calculer_temperature()
Cette méthode calcule la température de l'atmosphère terrestre à une date et une heure spécifiques en utilisant les données
de flux solaire et géomagnétique. Les paramètres optionnels permettent de spécifier la date et l'heure pour lesquelles 
la température doit être calculée. Les données de rayonnement F10.7 cm sont issues de [2] et pour le paramètre Ap de [3].

#### calculer_densite_air()
Cette méthode calcule la densité de l'air à une altitude donnée en utilisant des modèles atmosphériques standard pour la
altitude et le modèle de Jacchia-Lineberry au delà de 180km. Elle prend en paramètre l'altitude en mètres et renvoie la 
densité de l'air en kg/m³. Elle nécessite le calcul préalable de la température à l'altitude désirée.

#### calculer_densites()
Cette méthode fait appel à la méthode calculer_densite_air() pour remplir un tableau de densite de l'air.

## Sources 
[1] Forward, R. L., Hoyt, R. P., & Uphoff, C. W. (2000). Terminator TetherTM: A spacecraft deorbit device. Journal of Spacecraft and Rockets, 37(2), 187-19.
[2] Alexander M. Jablonski; DRDC Ottawa TM 2008-097; Defence R&D Canada – Ottawa; June 2008. 
[3] Victor U. J. Nwankwo, (2021), Atmospheric drag effects on modelled low Earth orbit (LEO) satellites during the July 2000 Bastille Day event in contrast to an interval of geomagnetically quiet condition.
[4] Dépôt de Timothée Thomas : https://github.com/Timotraque/MGA802_projet
[5] Dépôt de Thomas Martin : https://github.com/thomasorb/deorb/tree/main
