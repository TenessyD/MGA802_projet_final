import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import art3d
from .constantes import *



class Two_body_problem:
    """
    Représente un problème à deux corps impliquant deux corps célestes.

    Cet objet est particulièrement pertinent pour visualiser l'intéraction entre deux corps
    de masse comparable dans l'espace. Cette intéraction ne prends nullement en compte les interactions
    atmosphériques ou électro-magnétiques entre les corps.
    """

    def __init__(self, corps_a, corps_b, rayon=0, excent=0):
        """
        Initialise le problème à deux corps avec les paramètres donnés.

        Args:
            corps_a (SpaceBody): Objet représentant le premier corps céleste.
            corps_b (SpaceBody): Objet représentant le deuxième corps céleste.
            rayon (float): Paramètre de rayon pour la visualisation de l'orbite (par défaut 0).
            excent (float): Paramètre d'excentricité pour la visualisation de l'orbite, compris entre 0 et 1 (par défaut 0).
        """
        self.corps_a = corps_a
        self.corps_b = corps_b
        self.rayon = rayon
        self.excent = excent

    def show(self):
        """
        Visualise le problème à deux corps en traçant les corps célestes et leurs orbites en deux dimensions.
        """
        # Position centrée de la planète dans le plan orbital
        position_planete_a = (0, 0)
        position_planete_b = (0, self.rayon)
        # Création de la figure
        fig, ax = plt.subplots()

        # Cercle représentant la planète
        cercle_planete_a = plt.Circle(position_planete_a, self.corps_a.radius, color=self.corps_a.color)
        cercle_orbite = plt.Circle(position_planete_a, self.rayon, color='k', fill=False)
        cercle_planete_b = plt.Circle(position_planete_b, self.corps_b.radius, color=self.corps_b.color)

        # Ajout de la planète à la figure
        ax.add_patch(cercle_orbite)
        ax.add_patch(cercle_planete_a)
        ax.add_patch(cercle_planete_b)

        plt.xlim(xmin=-2 * self.rayon, xmax=2 * self.rayon)
        plt.ylim(ymin=-2 * self.rayon, ymax=2 * self.rayon)

        ax.axis("equal")
        plt.show()


class Orbite:
    """
    Représente la trajectoire orbitale d'un corps céleste.

    Cet objet est nécessaire pour visualiser les trajectoires d'un satellite autour de la Terre,
    il permet également de calculer la trajectoire de désorbitation et d'éstimer le temps de vie
    du satellite. Celui-ci est défini par le temps nécessaire pour que le rayon de l'oribte d'un satellite
    soumis aux frottements atmosphériques atteigne l'altitude de 100km au dessus du niveau de la mer.
    """

    def __init__(self, perigee, apogee, inclinaison=0, dt=1000, temps_simu=800000):
        """
        Initialise l'Orbite avec les paramètres donnés.
        Le temps de simulation contenu dans la variable temps_simu doit être suffisamment
        importante pour permettre la visualisation de la totalité de la trajectoire, traçant ainsi l'orbite.

        Args:
            perigee (float): Altitude du périgée au dessus de la mer (en mètres).
            apogee (float): Altitude de l'apogée au dessus de la mer (en mètres).
            inclinaison (float): Inclinaison orbitale en degrés (par défaut 0).
            dt (int): Intervalle de temps pour la simulation en secondes (par défaut 1000).
            temps_simu (int): Durée de la simulation en secondes (par défaut 800000).
        """

        if perigee <= apogee:
            self.perigee = perigee
            self.apogee = apogee
            self.dt = dt
            self.inclinaison = inclinaison
            self.temps_simu = temps_simu
            self.erreur = False
            self.a = (perigee + apogee + 2 * rayon_terre) / 2       # [m] demi grand-axe
        else:
            print("Echec, l'altitude de périgée doit être inférieure à l'apogée")
            self.erreur = True

    def plot_orbit(self):
        """
        Trace l'orbite en 3D avec le périgée et l'apogée, l'excentricité et l'inclinaison.

        Si aucune erreur n'est détectée lors de l'initialisation de l'orbite, cette méthode trace
        l'orbite elliptique en trois dimensions avec le périgée et l'apogée. Elle affiche également
        une coupe de la surface terrestre dans le plan de l'orbite.

        Raises:
            RuntimeError: Si l'altitude du périgée n'est pas inférieure ou égale à celle de l'apogée.

        """

        if not self.erreur:

            # Calcul de l'excentricité de l'orbite
            eccentricity = (self.apogee - self.perigee) / (self.apogee + self.perigee + 2 * rayon_terre)

            # Calcul de l'angle de l'inclinaison en radians
            inclination_rad = np.radians(self.inclinaison)

            # Générer des angles de 0 à 2pi pour tracer l'orbite
            angles = np.linspace(0, 2 * np.pi, 1000)

            # Calcul des coordonnées polaires
            r = self.a * (1 - eccentricity ** 2) / (1 + eccentricity * np.cos(angles))
            theta = angles

            # Conversion des coordonnées polaires en coordonnées cartésiennes
            x = r * np.cos(theta)
            y = r * np.sin(theta) * np.cos(inclination_rad)
            z = r * np.sin(theta) * np.sin(inclination_rad)

            # Rotation de l'orbite autour de l'axe z pour positionner le périgée
            rotation_angle = np.arctan2(y[0], x[0])
            x, y = x * np.cos(rotation_angle) - y * np.sin(rotation_angle), x * np.sin(rotation_angle) + y * np.cos(rotation_angle)

            # Calcul des coordonnées du périgée et de l'apogée
            x_perigee, y_perigee, z_perigee = self.a * (1 - eccentricity), 0, 0
            x_apogee, y_apogee, z_apogee = -self.a * (1 + eccentricity), 0, 0

            # Création de la figure 3D
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection='3d')

            # Tracer l'orbite
            ax.plot(x, y, z, label='Orbite elliptique')
            ax.scatter(x_perigee, y_perigee, z_perigee, color='blue', label='Périgée')
            ax.scatter(x_apogee, y_apogee, z_apogee, color='red', label='Apogée')

            # Ajouter un cercle représentant une coupe de la surface terrestre dans le plan de l'orbite

            earth_circle = Circle((0, 0), rayon_terre, color='green', alpha=0.3)
            ax.add_patch(earth_circle)
            art3d.pathpatch_2d_to_3d(earth_circle, z=0, zdir="z")

            # Paramètres esthétiques
            ax.set_xlabel('Distance X (km)')
            ax.set_ylabel('Distance Y (km)')
            ax.set_zlabel('Distance Z (km)')
            ax.set_title('Orbite elliptique')
            ax.scatter(0, 0, 0, color='green', label='Terre')
            ax.legend()

            texte_r_perigee = str(self.perigee)
            texte_r_apogee = str(self.apogee)
            texte = f"rayon perigee : {texte_r_perigee}\nrayon apogee : {texte_r_apogee}"
            ax.text(0, 0, s=texte, z=0)

            plt.show()

        else:
            print("Echec, l'altitude de périgée doit être inférieure à l'apogée")

    def manoeuvre(self, delta_v, direction, position):
        """
        Effectue une manoeuvre de changement de vitesse et renvoie une nouvelle orbite.

        Cette méthode calcule les nouveaux paramètres de l'orbite suite à une manoeuvre de changement de vitesse.
        La manoeuvre peut être effectuée à l'apogée ou au périgée.

        Args:
            delta_v (float): Variation de la vitesse orbitale.
            direction (str): Direction de la manoeuvre, peut être 'prograde', 'rétrograde' ou 'radiale'.
            position (str): Position initiale de la trajectoire, peut être 'périgée' ou 'apogée'.

        Returns:
            nouvelle_orbite (Orbite): Nouvelle orbite calculée après la manoeuvre.
        """

        # Calcul de la vitesse orbitale initiale
        match position:
            case Position_manoeuvre.perigee:
                v_initiale = np.sqrt(mu_terre / (self.perigee))

            case Position_manoeuvre.apogee:
                v_initiale = np.sqrt(mu_terre / (self.apogee))

        # Calcul de la variation de vitesse en fonctipon des paramètres de manoeuvre
        match direction:
            case Type_manoeuvre.prograde:
                v_finale = v_initiale + delta_v

            case Type_manoeuvre.retrograde:
                v_finale = v_initiale - delta_v

            # La manoeuvre radiale n'est pas encore codée
            case Type_manoeuvre.radiale:
                new_perigee = self.perigee
                new_apogee = self.apogee

        # Calcul des nouveaux rayons d'orbite
        match position:
            case Position_manoeuvre.perigee:
                r_perigee = self.perigee
                r_apogee = np.power(r_perigee * v_finale, 2) / (2 * mu_terre - r_perigee * np.power(v_finale, 2))

            case Position_manoeuvre.apogee:
                r_apogee = self.apogee
                r_perigee = np.power(r_apogee * v_finale, 2) / (2 * mu_terre - r_apogee * np.power(v_finale, 2))

        # Echange les points de perigee et d'apogee si nécessaire
        if r_apogee < r_perigee:
            dumy = r_apogee
            r_apogee = r_perigee
            r_perigee = dumy

        # Création et retour de la nouvelle orbite
        nouvelle_orbite = Orbite(r_perigee, r_apogee, self.inclinaison)
        return nouvelle_orbite

    def desorbitation(self, satellite, orbite, position, atmosphere, plot_orbit=False, force_propulsion=0):
        """
        Calcule et affiche le temps de désorbitation du satellite en orbite.

        Args:
            satellite (Satellite): Objet Satellite représentant le satellite en orbite.
            orbite (Orbite): Objet Orbite représentant l'orbite du satellite.
            position (Position_manoeuvre): Position initiale de la trajectoire (perigee ou apogee).
            atmosphere (Atmosphere): Objet Atmosphere contenant les données atmosphériques.
            plot_orbit (Bool): Booléen indiquant s'il faut afficher la trajectoire en 3D (par défaut False).
            force_propulsion (float): Force de propulsion pour la désorbitation, en Newton (par défaut 0).

        Returns:
            temps_final (float): Temps écoulé jusqu'à la fin de la désorbitation (en jours).
        """

        # Initialisation des variables
        temps = []
        rayon = []
        vitesse = []
        acceleration_radiale = []
        acceleration_tangentielle = []
        acceleration = []

        # Conditions de position initiales
        match position:
            case Position_manoeuvre.perigee:
                rayon.append(self.perigee + rayon_terre)
            case Position_manoeuvre.apogee:
                rayon.append(self.apogee + rayon_terre)

        # Conditions de vitesse initiale
        vitesse.append(np.sqrt(mu_terre * ((2 / rayon[0]) - 1 / orbite.a)))
        temps.append(0)

        i = 0

        # Tant que le satellite n'atteint pas 100 km
        while rayon[i] > (100000 + rayon_terre):

            # Force gravitationnelle et de trainee
            force_gravite = -mu_terre / (rayon[i] ** 2)

            # Calcul de la force de trainée
            densite_air = atmosphere.densite[int(rayon[i] - rayon_terre)//1000]
            force_trainee = 0.5 * densite_air * satellite.surface * np.power(vitesse[i], 2) * satellite.cx

            # Calcul des composantes radiales et tangentielle des forces
            force_radiale = force_gravite
            force_tangentielle = force_propulsion + force_trainee

            # Calcul de l'accélération radiale et tangentielle
            acceleration_radiale.append(force_radiale / satellite.mass)
            acceleration_tangentielle.append(force_tangentielle / satellite.mass)

            # Accélération = (somme des forces / masse), ne prends pas en compte la difference
            # de masse au cours de la manoeuvre
            acceleration.append((force_gravite + force_propulsion) / satellite.mass)

            # Mise à jour de la vitesse et de l'altitude
            vitesse.append((vitesse[i] + acceleration_tangentielle[i] * self.dt))
            rayon.append((2 * mu_terre * orbite.a) / (orbite.a * np.power(vitesse[i], 2) + mu_terre))
            temps.append(temps[i] + self.dt)
            i += 1

        # Affichage des trajectoires
        jour = []
        alt = []
        for j in range(len(temps)):
            jour.append(temps[j] / (24 * 3600))
            alt.append(rayon[j] - rayon_terre)
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_title('Altitude en fonction du temps')
        ax.set_xlabel('Temps [J]')
        ax.set_ylabel('Altitude [m]')
        ax.set_title('Durée de vie du satellite')
        plt.title('Durée de vie du satellite')
        plt.plot(jour, alt)
        plt.grid()
        plt.show()

        if plot_orbit :
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(rayon * np.cos(temps), rayon * np.sin(temps), np.zeros_like(temps), label='Trajectoire du satellite')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('Trajectoire du satellite en orbite')
            plt.legend()
            plt.show()

        return jour[len(jour)-1]
    