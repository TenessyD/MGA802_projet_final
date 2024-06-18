# Ce fichier contient les constantes de la librairie
from enum import Enum

# Constante représentant le paramètre gravitationnel standard de la Terre en m^3/s^2
mu_terre = 3.986e14

# Constante représentant le rayon moyen de la Terre en mètres
rayon_terre = 6.371e6

# Enumération des types de manoeuvres possibles
class Type_manoeuvre(Enum):
    """
    Enumération des types de manoeuvres possibles.

    Les types de manoeuvres possibles sont:
        - 'prograde': Manoeuvre dans le sens direct de l'orbite.
        - 'retrograde': Manoeuvre dans le sens rétrograde de l'orbite.
        - 'radiale': Manoeuvre radiale, orientée vers ou à partir du centre de la Terre.
    """
    prograde = 'prograde',   # Manoeuvre dans le sens direct de l'orbite
    retrograde = 'retrograde',  # Manoeuvre dans le sens rétrograde de l'orbite
    radiale = 'radiale'   # Manoeuvre radiale, orientée vers ou à partir du centre de la Terre

# Enumération des positions de manoeuvres possibles
class Position_manoeuvre(Enum):
    """
    Enumération des positions de manoeuvres possibles.

    Les positions de manoeuvres possibles sont:
        - 'apogee': Manoeuvre effectuée à l'apogée de l'orbite.
        - 'perigee': Manoeuvre effectuée au périgée de l'orbite.
    """
    apogee = 'apogee',   # Manoeuvre effectuée à l'apogée de l'orbite
    perigee = 'perigee'   # Manoeuvre effectuée au périgée de l'orbite
