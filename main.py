from Astraios import *
import time

# ---------------------Création d'orbite---------------------

perigee = 200 * 10**3   # Altitude du périgée [m]
apogee = 600 * 10**3    # Altitude de l'apogée [m]
inclinaison = 0         # Inclinaison de l'orbite [°]

orbite_initiale = Orbite(perigee, apogee, inclinaison )


# ---------------------Manoeuvre orbitale---------------------
delta_v = 1000  # Changement de vitesse en m/s
direction = Type_manoeuvre.prograde  # Direction de la manoeuvre ('prograde', 'retrograde' ou 'radiale')
position_manoeuvre = Position_manoeuvre.apogee  # Position de la manoeuvre ('perigee' ou 'apogee')

nouvelle_orbite = orbite_initiale.manoeuvre(delta_v, direction, position_manoeuvre)

# Affichage du nouvel orbite
nouvelle_orbite.plot_orbit()


#-----------------------Desorbitation------------------------
# Création d'un satellite et de l'atmosphere
spoutnik = Satellite(100, 0.5, 2)
atmosphere_terrestre = Atmosphere()

start = time.time()
# Affichage du temps de vie estimé
orbite_initiale.desorbitation(spoutnik, orbite_initiale, position_manoeuvre, atmosphere_terrestre)
print(f"Duree de calcul : {time.time() - start}")
