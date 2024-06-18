import ppigrf
import pandas as pd

class ChampMagnetique:
    date=[2010,5,10] #date [aaaa,mm,jj], utilisé pour la modélisation magnétique
    def __init__(self, latitude, longitude, altitude):
        """
        Initialise une instance de ChampMagnetique avec une latitude, une longitude, une altitude et une année données.

        :param latitude: Latitude en degrés
        :param longitude: Longitude en degrés
        :param altitude: Altitude en mètres
        """
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


    def estimer_intensite(self):
        """
        Estime l'intensité du champ magnétique en fonction de la position en utilisant le modèle IGRF.

        :return: Intensité du champ magnétique en nanoTesla (nT) dans 3 directions [Be,Bn,Bu]

        "Be" représente le champ magnétique dans la direction est, par rapport à un ellipsoïde de référence.
        "Bn" représente le champ magnétique dans la direction nord, par rapport à un ellipsoïde de référence.
        "Bu" représente le champ magnétique dans la direction vers le haut, par rapport à un ellipsoïde de référence.
        """
        B=ppigrf.igrf(self.longitude, self.latitude, self.altitude,pd.Timestamp(self.date[0],self.date[1],self.date[2]))
        return B

#test=ChampMagnetique(45.508889,-73.554167,10000000)
#print(test.estimer_intensite())