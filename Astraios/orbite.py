from .constantes import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class Orbite:
    def __init__(self, h, inclinaison=0, dt=1000, temps_simu=800000):
        self.puissances = None
        self.rayon = None
        self.rayon_total = h + rayon_terre
        self.dt = dt
        self.inclinaison = inclinaison
        self.temps_simu = temps_simu
        self.erreur = False
        self.approche = None

    def calculer_temps_desorbitation_energie(self, satellite, atmosphere, champ_mag):
        # Initialisation des variables
        self.temps = []
        self.rayon = []
        self.puissances = []
        vitesse = []
        theta = [0]
        puissance = [0]
        puissance_max = [0]

        # Conditions de position initiales
        satellite.set_position(r=self.rayon_total)
        self.rayon.append(self.rayon_total)

        # Conditions de vitesse initiale
        vitesse.append(self.vitesse_kepler(self.rayon_total))
        self.temps.append(0)

        # Autres conditions positions initiales
        equateur = 0
        angle_nord_vitesse_initiale = np.pi/2 - self.inclinaison/180*np.pi
        Bt = champ_mag.calculer_Bt(satellite, vitesse=angle_nord_vitesse_initiale)

        i = 0

        # Tant que le satellite n'atteint pas 100 km
        pbar = tqdm(total=(self.rayon[0] - rayon_terre)//1000 - 100)
        progress = (self.rayon[0] - rayon_terre)//1000 - 100
        while self.rayon[i] > (100000 + rayon_terre):
            force_trainee = self.caluler_trainee(atmosphere, satellite, vitesse[i])
            # Calcul force mag
            force_mag = satellite.calculer_Fe(Bt, vitesse[i], Rc=satellite.cable.resistance_de_controle)*np.cos(satellite.cable.inclinaison_alpha)
            forces = [force_trainee, -force_mag] #force mag le signe t'a capté

            k1 = self.dr_dt(satellite, vitesse[i], forces)
            satellite.set_position(r=self.rayon[i]+k1*self.dt)
            k2 = self.dr_dt(satellite, vitesse[i], forces)

            self.rayon.append(self.rayon[i] + (k1 + k2) * self.dt / 2)
            if (delta_progression := progress - ((self.rayon[i+1] - rayon_terre)//1000 - 100)) > 0:
                progress -= delta_progression
                pbar.update(delta_progression)

            satellite.set_position(r=self.rayon[i+1])
            vitesse.append(self.vitesse_kepler(self.rayon[i+1]))

            angle = np.atan2(vitesse[i] * self.dt, self.rayon[i]) #possible de perfectionner parceque cest surement un peu chelou
            equateur += angle

            satellite.update_etat(equateur, self.inclinaison)

            Bt = champ_mag.calculer_Bt(satellite, dt=self.dt)

            vitesse_par_rapport_ch_mag = vitesse[i+1]-2*np.pi*self.rayon[i+1]*np.cos((11.5+self.inclinaison)/180*np.pi)
            puissance.append(force_mag*vitesse_par_rapport_ch_mag)

            gamma = mu_terre/self.rayon[i+1]**3
            fd_max = -2.31*gamma*satellite.cable.longueur_cable*(satellite.cable.mass_ballast + satellite.cable.mass/4)
            puissance_max.append(fd_max*vitesse_par_rapport_ch_mag)

            self.temps.append(self.temps[i] + self.dt)
            theta.append(satellite.get_theta())

            i += 1

        pbar.close()
        self.approche = 'energetique'
        self.puissances = [puissance[1:], puissance_max[1:]]
        return self.temps[-1] / (24 * 3600)

    def calculer_temps_desorbitation_PFD(self, satellite_magnetique, atmosphere, champ_mag):
        # Initialisation des variables
        temps = []
        rayon = []
        vitesse = []
        acceleration_radiale = []
        acceleration_tangentielle = []
        puissance = [0]
        puissance_max = [0]
        theta = [0]

        # Conditions de position initiales
        satellite_magnetique.set_position(r=self.rayon_total)
        rayon.append(self.rayon_total)

        # Conditions de vitesse initiale
        vitesse.append(np.sqrt(mu_terre / rayon[0]))
        temps.append(0)
        i = 0

        equateur = 0
        angle_nord_vitesse_initiale = np.pi/2 - self.inclinaison/180*np.pi

        # Calcul de la composante transversale du champ magnétique
        Bt = champ_mag.calculer_Bt(satellite_magnetique, vitesse=angle_nord_vitesse_initiale)

        # Tant que le satellite n'atteint pas 100 km
        while rayon[i] > (100000 + rayon_terre):

            # Force gravitationnelle et de trainee
            force_gravite = -mu_terre / (rayon[i] ** 2)

            # Calcul du champ magnétique
            force_lorentz = (- satellite_magnetique.calculer_Fe(Bt, vitesse[i], Rc=satellite_magnetique.cable.resistance_de_controle)*np.cos(satellite_magnetique.cable.inclinaison_alpha))

            # Calcul de la trainée atmosphérique
            densite_air = atmosphere.densite[int(rayon[i] - rayon_terre)//1000]
            force_trainee = 0.5 * densite_air * satellite_magnetique.surface * np.power(vitesse[i], 2) * satellite_magnetique.cx

            # Calcul des composantes radiales et tangentielle des forces
            force_radiale = force_gravite
            force_tangentielle = force_trainee + force_lorentz

            # Calcul de l'accélération radiale et tangentielle
            acceleration_radiale.append(force_radiale / satellite_magnetique.mass)
            acceleration_tangentielle.append(force_tangentielle / satellite_magnetique.mass)

            # Mise à jour de la vitesse et de l'altitude
            vitesse.append((vitesse[i] + acceleration_tangentielle[i] * self.dt))
            rayon.append(mu_terre/vitesse[i+1]**2)

            angle = np.atan2(vitesse[i] * self.dt, rayon[i])  # possible de perfectionner parceque cest surement un peu chelou
            equateur += angle

            satellite_magnetique.update_etat(equateur, self.inclinaison)

            Bt = champ_mag.calculer_Bt(satellite_magnetique, dt=self.dt)
            temps.append(temps[i] + self.dt)
            theta.append(satellite_magnetique.get_theta())

            vitesse_par_rapport_ch_mag = vitesse[i+1]-2*np.pi*rayon[i+1]*np.cos((11.5+self.inclinaison)/180*np.pi)
            puissance.append(-force_lorentz*vitesse_par_rapport_ch_mag)

            gamma = mu_terre/rayon[i+1]**3
            fd_max = -2.31*gamma*satellite_magnetique.cable.longueur_cable*(satellite_magnetique.cable.mass_ballast + satellite_magnetique.cable.mass/4)
            puissance_max.append(fd_max*vitesse_par_rapport_ch_mag)
            i += 1

        self.approche == 'pfd'
        self.afficher_puissances([puissance[1:], puissance_max[1:]])
        return temps[-1] / (24 * 3600)

    def vitesse_kepler(self, h):
        return np.sqrt(mu_terre / h)

    def caluler_trainee(self, atmosphere, satellite, vitesse):
        densite_air = atmosphere.densite[int(satellite.get_r() - rayon_terre) // 1000]
        force_trainee = 0.5 * densite_air * satellite.surface * np.power(vitesse, 2) * satellite.cx
        return force_trainee

    def dr_dt(self, satellite, vitesse, force):
        P_d = sum(force) * vitesse
        dr = - 2 / (mu_terre * satellite.mass) * satellite.get_r() ** 2 * (P_d)
        return dr

    def afficher_temps_desorbitation(self, donnees_sans_cable = False):
        # Affichage des trajectoires
        jour = []
        alt = []
        for j in range(len(self.temps)):
            jour.append(self.temps[j] / (24 * 3600))
            alt.append(self.rayon[j] - rayon_terre)
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_title('Altitude en fonction du temps')
        ax.set_xlabel('Temps [J]')
        ax.set_ylabel('Altitude [m]')
        ax.set_title('Durée de vie du satellite')
        if (self.approche == "energetique"):
            plt.title("Durée de vie du satellite calculée avec l'approche énergétique")
        elif (self.approche == "pfd"):
            plt.title("Durée de vie du satellite calculée avec le PFD")
        plt.plot(jour, alt)
        if donnees_sans_cable:
            donne = np.genfromtxt('data/donne_sans_cable.csv', delimiter=';')
            temps = donne[:, 0]
            rayon = donne[:, 1]
            jour_sc = []
            for j in range(len(temps)):
                jour_sc.append(temps[j] / (24 * 3600))
            plt.plot(jour_sc, rayon)
        plt.grid()
        plt.show()

    def afficher_puissances(self):
        # Affichage des trajectoires
        y = np.array(self.puissances).transpose()
        jour = []
        for j in range(1,len(self.temps)):
            jour.append(self.temps[j] / (24 * 3600))
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_title("Puissance dissipée par l'antenne électromgnétique")
        ax.set_xlabel('Durée [J]')
        ax.set_ylabel('Puissance [W]')
        ax.set_title("Puissance dissipée par l'antenne électromgnétique")
        plt.title("Puissance dissipée par l'antenne électromgnétique")

        plt.plot(jour, y[:, 0], label="puissance dissipée par le cable")
        plt.plot(jour, y[:, 1], label="puissance max à ne pas dépasser")

        plt.legend(loc='upper right')
        plt.grid()
        plt.show()

    def calculer_vitesse_initial(self):
        self.vitesse_initial = np.sqrt(mu_terre / self.rayon_total)
        return self.vitesse_initial