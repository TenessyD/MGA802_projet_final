import ppigrf
from math import cos, sin, pi
from datetime import timedelta
from numpy import squeeze
from .constantes import *


class champ_mag:
    """
    Classe pour calculer le champ magnétique terrestre ressenti par un satellite.

    Attributes
    ----------
    date : datetime.date
        La date initiale pour les calculs du champ magnétique.
    dt : int
        Le temps écoulé depuis la date initiale, en secondes.
    be : float
        La composante est du champ magnétique en Tesla.
    bn : float
        La composante nord du champ magnétique en Tesla.
    bu : float
        La composante radiale du champ magnétique en Tesla.
    bt : float
        La composante tangente du champ magnétique en Tesla.

    Methods
    -------
    calculer_Bt(satellite, dt=0, vitesse=None)
        Calcule la composante tangente du champ magnétique en fonction de la position
        et de la vitesse angulaire du satellite.
    """

    def __init__(self, date):
        """
        Initialise la classe champ_mag avec la date donnée.

        Parameters
        ----------
        date : datetime.date
            La date initiale pour les calculs du champ magnétique.
        """
        self.date = date
        self.dt = 0

    def calculer_Bt(self, satellite, dt=0, vitesse=None):
        """
        Calcule la composante tangente du champ magnétique en fonction de la position
        et de la vitesse angulaire du satellite.

        Parameters
        ----------
        satellite : object
            Objet représentant le satellite avec les méthodes get_r, get_theta, et get_phi
            qui retournent respectivement le rayon, l'angle polaire et l'angle azimutal
            du satellite.
        dt : int, optional
            Temps écoulé en secondes à ajouter à `self.dt` (default is 0).
        vitesse : float, optional
            Vitesse angulaire du satellite par rapport au nord (default is None).
            Si None, utilise `satellite.angle_nord_vitesse`.

        Returns
        -------
        float
            La composante tangente du champ magnétique en Tesla.
        """
        if vitesse is None:
            vitesse = satellite.angle_nord_vitesse
        self.dt += dt
        delta_j = self.dt // (24 * 3600)
        new_date = self.date + timedelta(delta_j)
        r = (satellite.get_r() - rayon_terre) // 1000
        theta = satellite.get_theta()*180/pi
        phi = satellite.get_phi()*180/pi
        if phi >=180:
            phi  = phi-360

        [be, bn, bu] = ppigrf.igrf(phi, theta, r, new_date)  # utiliser igrf_gc plutot sauf que igrf_gc cest de la merde
        # cest surement des degre (à revoir donc)
        self.be = squeeze(be) / 10 ** 9
        self.bn = squeeze(bn) / 10 ** 9
        self.bu = squeeze(bu) / 10 ** 9

        self.bt = self.bn * sin(vitesse) + self.be * cos(vitesse)  # pas sur des signe mais pas hyper important jpense
        # à verifier wolla surement alpha doit jouer un role mais je trouve pas
        # verifier signe entre les deux
        # pas sur que ce soit utile de les stocker en memoire mais why not

        return self.bt
