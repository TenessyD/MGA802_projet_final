# Projet : Modélisation de la vitesse de désorbitation d'un satellite en LEO doté d'un frein électromagnétique.

Ce projet a pour objectif d'estimer le temps de désorbitation d'un satellite en orbite basse terrestre en considérant les forces de traînée 
atmosphérique et électromagnétique agissant sur le satellite. Le dispositif considéré pour bénéficier de la traînée électromagnétique est 
décrit par l'article [1].

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

## Documentation
Toute la documentation nécessaire pour comprendre la structure du module est disponible dans l'onglet `build` de ce dépot GitHub.
Vous pouvez y accéder en ouvrant le fichier "index.html" dans votre navigateur se trouvant dans le dossier 'build/html'.

### Classes et méthodes clés :

#### Classe 'Satellite' :
La classe "Satellite" représente un satellite en orbite autour d'une planète. Cet objet possède des attributs caractéristiques 
d'un satellite, tels que sa masse en kg, son coefficient de traînée 'cx' (sans dimension) et sa surface transversale en mètres carrés. 
Le coefficient de traînée est fixé par défaut à 2 si l'utilisateur ne dispose pas de cette donnée pour le satellite sur lequel il 
souhaite effectuer des simulations.

#### Classe 'Cable' :
La classe "Cable" est utilisée pour instancier un objet représentant le dispositif accroché au satellite pour bénéficier de la traînée électromagnétique,
le "Terminator Tether". Cet objet possède les attributs caractéristiques du dispositif, à savoir : la longueur du câble en mètres, 
la masse de ballast en kg, le matériau de fabrication qui est lui-même défini par une densité et une résistance en ohms, ainsi que sa section en m^2.

#### Classe 'Satellite_magnetique' : 
La sous-classe "Satellite_magnetique" hérite de "Satellite" et est utilisée pour représenter spécifiquement les satellites bénéficiant d'une antenne 
électromagnétique. En plus des attributs d'un satellite "classique", cette classe possède des attributs supplémentaires tels que l'objet "Cable" 
vu précédemment et un attribut "position" qui permet de définir, à chaque étape de calcul de trajectoire, les coordonnées du satellite dans l'espace. 
Contrairement à un satellite classique qui n'est pas impacté par le champ magnétique terrestre, il est nécéssaire de connaitre à chaque instant la position
d'un satellite magnétique dans l'espace pour calculer la norme du champ auquel il est soumi en un point souhaité et donc, la trainée électromgnétique associée.

#### Classe 'Orbite' : 
L'objet "Orbite" permet de modéliser les orbites circulaire autour d'un corps céleste, tel que la Terre. 
Cette classe est utilisée pour définir les paramètres d'une orbite tel que son altitude ou son inclinaison. 
Elle possède les méthodes grâce auxquelles sont calculées et affichées les temps de désorbitation pour un 
satellite donnée. Elle possède donc un 3ème attribut 'dt' correspondant à l'intervalle de temps entre chaque nouveau calcul
de trajectoire avec l'approche énergétique et/ou basé sur le PFD. 
Toute étape du programme nécessitant des calculs (norme d'une force, trajectoire, vitesse) utilise cet objet et ces méthodes.

#### calculer_temps_desorbitation(self, satellite, atmosphere, champ_mag, approche)
La méthode "calculer_temps_desorbitation()" simule la désorbitation du satellite magnétique en orbite. Elle possède un paramètre "approche"
permettant de calculer la trajectoire du satellite à chaque intervalle de temps "dt" basée sur une approche énergétique (th. de l'énergie mécanique)
ou sur une approche basée sur PFD (seconde loi de Newton). Elle considère la force gravitationnelle, la traînée atmosphérique et magnétique. Cette méthode
possède une boucle sur qui calcule à chaque itération le rayon de la nouvelle orbite calculée à chaque intervalle de temps 'dt'.
Les paramètres de la désorbitation sont spécifiés comme suit :
- `satellite` : Instance de la classe `Satellite` représentant le satellite en orbite.
- `atmosphere` : Instance de la classe `Atmosphere` représentant l'atmosphère terrestre.
- `champ_mag` : Instance de la classe `ChampMagnetque` représentant un modèle du champ magnétque terrestre.
- `approche` : Permet de spécifier l'approche souhaitée pour la réalisation des calculs ('pfd' ou 'energetique').

### Objet Atmosphere :
L'objet "Atmosphere" est issu de la bibliothèque "Astraios" écrite par Timothée Thomas, il modélise l'atmosphère terrestre. 
Ce dépôt est accessible à l'adresse suivante : https://github.com/Timotraque/MGA802_projet.
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
- [1] Forward, R. L., Hoyt, R. P., & Uphoff, C. W. (2000). Terminator TetherTM: A spacecraft deorbit device. Journal of Spacecraft and Rockets, 37(2), 187-19.
- [2] Alexander M. Jablonski; DRDC Ottawa TM 2008-097; Defence R&D Canada – Ottawa; June 2008.
- [3] Victor U. J. Nwankwo, (2021), Atmospheric drag effects on modelled low Earth orbit (LEO) satellites during the July 2000 Bastille Day event in contrast to an interval of geomagnetically quiet condition.
- [4] Dépôt de Timothée Thomas : https://github.com/Timotraque/MGA802_projet
- [5] Dépôt de Thomas Martin : https://github.com/thomasorb/deorb/tree/main
