from .constantes import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm, gui

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

    def calculer_temps_desorbitation(self, satellite, atmosphere, champ_mag, approche):
        # Initialisation des variables
        nouvelle_vitesse = None
        nouveau_rayon = None
        self.approche = approche
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
        pbar = tqdm(total=(self.rayon[0] - rayon_terre)//1000 - 100,colour='blue')
        progress = (self.rayon[0] - rayon_terre)//1000 - 100
        while self.rayon[i] > (100000 + rayon_terre):
            force_trainee = self.caluler_trainee(atmosphere, satellite, vitesse[i])
            # Calcul force mag
            force_mag = satellite.calculer_Fe(Bt, vitesse[i], Rc=satellite.cable.resistance_de_controle)*np.cos(satellite.cable.inclinaison_alpha)
            forces = [force_trainee, -force_mag]

            if self.approche == 'energetique':
                k1 = self.dr_dt(satellite, vitesse[i], forces)
                satellite.set_position(r=self.rayon[i]+k1*self.dt)
                k2 = self.dr_dt(satellite, vitesse[i], forces)
                nouveau_rayon = self.rayon[i] + (k1 + k2) * self.dt / 2
                nouvelle_vitesse = self.vitesse_kepler(nouveau_rayon)
            elif self.approche == 'pfd':
                nouvelle_vitesse = vitesse[i] + sum(forces)/satellite.mass * self.dt
                nouveau_rayon = mu_terre / nouvelle_vitesse ** 2

            vitesse.append(nouvelle_vitesse)
            self.rayon.append(nouveau_rayon)

            if (delta_progression := progress - ((self.rayon[i+1] - rayon_terre)//1000 - 100)) > 0:
                progress -= delta_progression
                pbar.update(delta_progression)

            angle = np.atan2(vitesse[i] * self.dt, self.rayon[i]) #possible de perfectionner parceque cest surement un peu chelou
            equateur += angle

            satellite.set_position(r=self.rayon[i+1])
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
        self.puissances = [puissance[1:], puissance_max[1:]]
        return self.temps[-1] / (24 * 3600)

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
            filename = None
            if self.approche == 'energetique':
                filename = 'data/donne_sans_cable_energie.csv'
            elif self.approche == 'pfd':
                filename = 'data/donne_sans_cable_PFD.csv'
            donne = np.genfromtxt(filename, delimiter=';')
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