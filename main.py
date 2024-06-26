from datetime import datetime
from Astraios import *

# ---------------------Création d'orbite---------------------

altitude = 150 * 10 ** 3  # Altitude du périgée [m]
inclinaison = 30  # Inclinaison de l'orbite [°]

date = datetime(2021, 3, 28)
champ_magnetique = champ_mag(date)
atmosphere_terrestre = Atmosphere()

cable_mag = cable(5000, 185, 45)
satMag = satellite_magnetique(1300, 0.5, cable_mag)
orbite = Orbite(altitude, inclinaison, 300)
orbite.desorbitation_PFD(satMag, atmosphere_terrestre, champ_magnetique)
