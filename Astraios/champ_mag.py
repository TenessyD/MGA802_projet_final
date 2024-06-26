import ppigrf
from math import cos, sin
from datetime import timedelta
from numpy import squeeze
from .constantes import *


class champ_mag:
    def __init__(self, date):
        self.date = date
        self.dt = 0

    def calculer_Bt(self, satellite, dt=0, vitesse=None):
        if vitesse is None:
            vitesse = satellite.angle_nord_vitesse
        self.dt += dt
        delta_j = self.dt // (24 * 3600)
        new_date = self.date + timedelta(delta_j)
        r = (satellite.get_r() - rayon_terre) // 1000
        theta = satellite.get_theta()
        phi = satellite.get_phi()

        [be, bn, bu] = ppigrf.igrf(phi, theta, r, new_date)  # utiliser igrf_gc plutot sauf que igrf_gc cest de la merde
        # cest surement des degre (à revoir donc)
        self.be = squeeze(be) / 10 ** 9
        self.bn = squeeze(bn) / 10 ** 9
        self.bu = squeeze(bu) / 10 ** 9

        self.bt = self.bn * sin(vitesse) + self.be * cos(vitesse) #pas sur des signe mais pas hyper important jpense
        #à verifier wolla surement alpha doit jouer un role mais je trouve pas
        #verifier signe entre les deux
        #pas sur que ce soit utile de les stocker en memoire mais why not

        return self.bt