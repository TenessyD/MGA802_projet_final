"""
Programme principal pour la simulation de la désorbitation d'un satellite à l'aide d'un frein magnétique.

Ce programme permet de :
1. Lire les paramètres de simulation depuis un fichier YAML.
2. Demander à l'utilisateur de choisir une approche de calcul.
3. Créer les objets nécessaires à la simulation (orbite, satellite, câble, matériaux).
4. Calculer et afficher les résultats de la simulation.

Modules utilisés:
    - datetime: Pour manipuler les dates.
    - frein_magnetique: Module customisé pour le freinage magnétique.
    - frein_magnetique.LecteurYAML: Classe pour lire le fichier YAML.
    - os: Pour manipuler les chemins de fichiers.

Auteur: Raphaël Barral, Fabien Bertrand, Ténessy De Faria
Date: 2024-07-08
"""

from datetime import datetime
from frein_magnetique import *
import os

approche = None

input("Entrez les paramètres de simulation dans le fichier data.yaml puis appuyez sur 'Entrée'")
print('Quelle approche souhaitez-vous utiliser pour effectuer les calculs ?')
print('1. Approche énergétique')
print('2. Approche basée sur le principe fondamental de la dynamique (PFD)')

while True:
    choix = input()
    if choix == '1':
        approche = 'energetique'
        break
    elif choix == '2':
        approche = 'pfd'
        break

# ---------------------Lecture du YAML---------------------
whole_path = os.path.join(os.path.abspath(os.path.curdir), "data.yaml")
parser = LecteurYAML(whole_path)
parsed_data = parser.read_yaml()

# ---------------------Création d'orbite---------------------
altitude = parsed_data['orbite']['altitude']
inclinaison = parsed_data['orbite']['inclinaison']  # Inclinaison de l'orbite [°]
dt = parsed_data['orbite']['dt']

# ---------------------Caractéristiques du satelitte---------------------
masse_satelitte = parsed_data['satelitte_magnetique']['masse']
surface_de_trainee = parsed_data['satelitte_magnetique']['surface_de_trainee']

# ---------------------Caractéristiques du cable---------------------
longueur = parsed_data['satelitte_magnetique']['cable']['longueur']
section = parsed_data['satelitte_magnetique']['cable']['section']
masse_ballaste = parsed_data['satelitte_magnetique']['cable']['ballast_mass']
resistance_de_controle = parsed_data['satelitte_magnetique']['cable']['resistance_de_controle']

# --------------------- Date ---------------------
year = parsed_data['date']['year']
month = parsed_data['date']['month']
day = parsed_data['date']['day']

date = datetime(year, month, day)
champ_magnetique = Champ_mag(date)
atmosphere_terrestre = Atmosphere()

copper = Materiau(densite_cuivre, resistance_linéaire_cuivre)
alu = Materiau(densite_alu, resistance_linéaire_alu)
cable_mag = Cable(longueur, section, alu, mass_ballast=masse_ballaste, Rc=resistance_de_controle)
satMag = Satellite_magnetique(masse_satelitte, surface_de_trainee, cable_mag)
orbite = Orbite(altitude, inclinaison, dt=dt)


satMag.calcul_des_masses()
print(f"L'altitude initiale du satellite est {altitude:0.0f} m")
print(f'La vitesse initiale du satellite est {orbite.calculer_vitesse_initial():0.2f} m/s-1')

temps_deorb = orbite.calculer_temps_desorbitation(satMag, atmosphere_terrestre, champ_magnetique, approche)
print(f'Le temps de désorbitation est de {temps_deorb:0.2f} jours.')

if input('Afficher courbe du temps de désorbitation (o/n)') == 'o':
    orbite.afficher_temps_desorbitation(donnees_sans_cable=False)

if input('Afficher courbe de puissance dissipée par le cable (o/n)') == 'o':
    orbite.afficher_puissances()

if filename := input('Entrez le nom du fichier de sortie (Laissez vide pour ne pas sauvegarder les données)'):
    parametres = {
        'altitude': [altitude],
        'inclinaison': [inclinaison],
        'dt': [dt],
        'masse_satelitte': [masse_satelitte],
        'surface_de_trainee': [surface_de_trainee],
        'longueur_cable': [longueur],
        'section_cable': [section],
        'masse_ballaste': [masse_ballaste],
        'resistance_de_controle': [resistance_de_controle]
    }
    orbite.save_data(filename)

