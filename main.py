from datetime import datetime
from Astraios import *

# ---------------------Création d'orbite---------------------

altitude = 200 * 10 ** 3  # Altitude du périgée [m]
inclinaison = 0  # Inclinaison de l'orbite [°]

date = datetime(2021, 3, 28)
champ_magnetique = champ_mag(date)
atmosphere_terrestre = Atmosphere()


copper = materiau(8933, 17*10**-9)
alu = materiau(2700, 27.4*10**-9)
cable_mag = cable(5000, 10, alu, 0)
satMag = satellite_magnetique(1000, 0.5, cable_mag)
satMag.calcul_des_masses(10)
orbite = Orbite(altitude, inclinaison, 300)
orbite.desorbitation_PFD(satMag, atmosphere_terrestre, champ_magnetique)
