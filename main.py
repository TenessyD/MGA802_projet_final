from datetime import datetime
from Astraios import *
from Astraios.LecteurYAML import LecteurYAML
import os

approche = None

input('Entrez les données dans le fichier data.yaml puis appuyez sur Entrée')
print('Quelle méthode souhaitez-vous utiliser')
print('1. Méthode énergétique')
print('2. Méthode par le principe fondamental de la dynamique (PFD)')

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
champ_magnetique = champ_mag(date)
atmosphere_terrestre = Atmosphere()

copper = materiau(densite_cuivre, resistance_linéaire_cuivre)
alu = materiau(densite_alu, resistance_linéaire_alu)
cable_mag = cable(longueur, section, alu, mass_ballast=masse_ballaste, Rc=resistance_de_controle)
satMag = satellite_magnetique(masse_satelitte, surface_de_trainee, cable_mag)
orbite = Orbite(altitude, inclinaison, dt=dt)

satMag.calcul_des_masses()
print(f"L'altitude initiale du satellite est {altitude+rayon_terre}")
print(f'La vitesse initiale du satellite est {orbite.calculer_vitesse_initial()}')

orbite.calculer_temps_desorbitation(satMag, atmosphere_terrestre, champ_magnetique, approche)

if input('Afficher courbe de desorbitation (o/n)') == 'o':
    orbite.afficher_temps_desorbitation(donnees_sans_cable=False)

if input('Afficher courbe de puissance dissipée par le cable (o/n)') == 'o':
    orbite.afficher_puissances()
if filename := input('Entrez le nom du fichier de sortie (Laissez vide pour ne pas sauvegarder les données)'):
    orbite.save_data(filename)

