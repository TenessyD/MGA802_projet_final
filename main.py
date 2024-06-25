from Astraios import *
import time

# ---------------------Création d'orbite---------------------

perigee = 200 * 10**3   # Altitude du périgée [m]
apogee = 200 * 10**3      # Altitude de l'apogée [m]
inclinaison = 45         # Inclinaison de l'orbite [°]

orbite_initiale = Orbite(perigee, apogee, inclinaison)
position_manoeuvre = Position_manoeuvre.apogee  # Position de la manoeuvre ('perigee' ou 'apogee')

#----------------------Desorbitation------------------------

# Création d'un satellite et de l'atmosphère
spoutnik = Satellite(1300, 0.5, 2)
atmosphere_terrestre = Atmosphere()
tether = Cable(5000,185, 35.26)
spoutnik_mag = SatelliteMagnetique(spoutnik.mass, spoutnik.surface, tether)
start = time.time()

# Affichage du temps de vie estimé
orbite_initiale.desorbitation(spoutnik_mag, orbite_initiale, position_manoeuvre, atmosphere_terrestre)
print(f"Duree de calcul : {time.time() - start}")
