import pandas as pd
import numpy as np

class Atmosphere:
    """    Classe représentant les propriétés de l'atmosphère terrestre.
    Le modèle établit utilise le modèle de Jacchia-Lineberry pour calculer
    la densite de l'atmosphère en ultra-haute altitude. Cet objet permet donc de
    d'obtenir une densité atmospherique pertinente pour le calcul de la trainée induite
    sur le satellite en orbite basse (LEO).

    Attributes:
        temperature (float): Température de l'atmosphère terrestre (en Kelvin).
        densite (float): Liste des densités de l'air à différentes altitudes (en kg/m^3).
    """

    def __init__(self):
        """     Initialise une instance de la classe Atmosphere.

        - Calcul de la température de l'atmosphère.
        - Calcul des densités d'air à différentes altitudes.        """
        self.temperature = self.calculer_temperature()
        self.densite = self.calculer_densites()

    def calculer_densite_air(self, altitude):
        """
        Calcule la densité de l'air à une altitude donnée, repose sur un modèle d'atmosphère jusqu'à 100km et un modèle
        au delà de 100km d'altitude (pertinent jusqu'à environ 1000km). Voir bibliographie pour plus d'informations.

        Args:
            altitude (int): Altitude à laquelle calculer la densité (en mètres).

        Returns:
            rho (float): Densité de l'air à l'altitude donnée (en kg/m^3).
        """
        if altitude < 100000:
            # Constantes de l'atmosphère standard
            p0 = 101325  # Pression atmosphérique au niveau de la mer en Pa
            T0 = 288.15  # Température au niveau de la mer en K
            L = 0.0065  # Variation de température avec l'altitude en K/m
            R = 8.31447  # Constante des gaz parfaits en J/(mol*K)
            M = 0.0289644  # Masse molaire de l'air en kg/mol
            g = 9.80665  # Accélération gravitationnelle en m/s^2

            # Calcul de la température à l'altitude donnée
            T = T0 - L * altitude

            # Calcul de la pression à l'altitude donnée
            p = p0 * np.float_power((1 - ((L * altitude) / T0)), g * M / (R * L))

            # Calcul de la densité de l'air à l'altitude donnée
            rho = p * M / (R * T)
            rho = rho.item()

        elif altitude >= 100000:
            m = 27 - 0.012 * ((altitude / 1000) - 200)

            # En utilisant la température en très haute atmosphère
            H = self.temperature / m   # [km]

            rho = 6 * (1 / np.power(10, 10)) * np.exp(-((altitude / 1000) - 175) / H)       # [kg / m3]
            rho = rho.item()

        return rho

    def calculer_densites(self):
        """
        Calcule les densités de l'air à différentes altitudes.

        Returns:
            densites_air (float): Liste des densités de l'air à différentes altitudes (en kg/m^3).
        """
        altitude_max = int(1000000)  # 1000 km en mètres
        intervalle = 1000  # Intervalle en mètres
        densites_air = [self.calculer_densite_air(altitude) for altitude in
                        range(0, altitude_max + intervalle, intervalle)]

        return densites_air

    def calculer_temperature(self, annee=2023, mois=4, jour=1, heure=0.0):
        """
        Calcule la température de l'atmosphère terrestre.

        Args:
            annee (int): Année pour laquelle calculer la température (par défaut 2023).
            mois (int): Mois pour lequel calculer la température, commençant par 1 = janvier jusqu'à 12 = décembre (par défaut 4).
            jour (int): Jour pour lequel calculer la température, commençant par 1 jusqu'à 31 suivant les mois (par défaut 1).
            heure (float): Heure du jour pour laquelle calculer la température, de 0.0 à 23.5 (par défaut 0.0).

        Returns:
            T (float): Température de l'atmosphère terrestre (en Kelvin).
        """

        fichier_f10_7 = pd.read_excel('data/flux_solaire_data.xlsx')
        f_10_7 = float(fichier_f10_7[(fichier_f10_7['Année'] == annee) & (fichier_f10_7['Mois'] == mois)]['Flux ajusté'])   # [W.m-2.Hz-1]

        fichier_Ap = pd.read_excel('data/geomagnetic_data_gfz.xlsx')
        Ap = float(fichier_Ap[(fichier_Ap['year'] == annee) & (fichier_Ap['month'] == mois) & (fichier_Ap['day']==jour) & (fichier_Ap['hour_h']==heure)]['ap'])

        T = 900 + 2.5 * (f_10_7 - 70) + 1.5 * Ap    # [K]

        return T
