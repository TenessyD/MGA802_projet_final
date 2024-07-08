from math import cos, pi, atan2
from ai import cs

class SpaceBody():
    """
    Représente un corps céleste générique.

    Attributes:
        mass (float): La masse du corps céleste.
    """

    def __init__(self, mass=0):
        self.mass = mass

class Satellite(SpaceBody):
    """
    Représente un satellite en orbite autour d'un corps céleste.

    Attributes:
        mass (float): La masse du satellite.
        cx (int): Le coefficient de traînée sans dimension.
        surface (float): La surface transversale du satellite en mètres carrés.
    """
    def __init__(self, mass, cross_surface, cx=2):
        """
        Initialise un satellite avec sa masse, sa surface transversale et son coefficient de traînée.

        Args:
            mass (float): La masse du satellite en kilogrammes.
            cross_surface (float): La surface transversale du satellite en mètres carrés.
            cx (int, optional): Le coefficient de traînée sans dimension (par défaut 2).
        """
        super().__init__(mass)
        self.cx = cx                # [sans dimension]
        self.surface = cross_surface      # [m²]

class Cable:
    """
    Représente un câble utilisé par un satellite.

    Attributes:
        longueur_cable (float): La longueur du câble en mètres.
        section (float): La section transversale du câble en mètres carrés.
        materiau (Materiau): Le matériau dont est composé le câble.
        inclinaison_alpha (float): L'inclinaison du câble en degrés.
        mass_ballast (float): La masse du ballast en kilogrammes.
        resistance_de_controle (float): La résistance de contrôle en ohms.
    """
    def __init__(self, longueur_cable, section, materiau, inclinaison_alpha=35.26, mass_ballast = 10, Rc = 0):
        """
        Initialise un câble avec ses propriétés.

        Args:
            longueur_cable (float): La longueur du câble en mètres.
            section (float): La section transversale du câble en millimètres carrés.
            materiau (Materiau): Le matériau dont est composé le câble.
            inclinaison_alpha (float, optional): L'inclinaison du câble en degrés (par défaut 35.26).
            mass_ballast (float, optional): La masse du ballast en kilogrammes (par défaut 10).
            Rc (float, optional): La résistance de contrôle en ohms (par défaut 0).
        """
        self.mass_ballast = mass_ballast
        self.materiau = materiau
        self.longueur_cable = longueur_cable
        self.section = section*10**-6 #mm2 to m2
        self.mass = self.materiau.densite*self.longueur_cable*self.section
        self.volume = self.section*self.longueur_cable
        self.resistance = self.materiau.resistance/self.section*self.longueur_cable or 1
        self.inclinaison_alpha = inclinaison_alpha/180*pi
        self.resistance_de_controle = Rc

class Satellite_magnetique(Satellite):
    """
    Représente un satellite équipé d'un câble pour freinage magnétique.

    Attributes:
        cable (Cable): Le câble utilisé par le satellite.
        position (list): La position du satellite en coordonnées sphériques [r, theta, phi].
        angle_nord_vitesse (float): L'angle entre la vitesse et le nord.
    """

    def __init__(self, mass, cross_surface, cable, position=None, cx=2):
        """
        Initialise un satellite magnétique avec ses propriétés.

        Args:
            mass (float): La masse du satellite en kilogrammes.
            cross_surface (float): La surface transversale du satellite en mètres carrés.
            cable (Cable): Le câble utilisé par le satellite.
            position (list, optional): La position initiale du satellite [r, theta, phi] (par défaut [0, 0, 0]).
            cx (int, optional): Le coefficient de traînée sans dimension (par défaut 2).
        """
        super().__init__(mass, cross_surface, cx)
        if position is None:
            position = [0, 0, 0]
        self.__position = position #r, theta, phi
        self.angle_nord_vitesse = 0
        self.cable = cable
    def calculer_Fe(self, Bt, Vo, Rc=0):
        """
        Calcule la force électromagnétique exercée sur le satellite.

        Args:
            Bt (float): L'induction magnétique en teslas.
            Vo (float): La vitesse du satellite en m/s.
            Rc (float, optional): La résistance de contrôle en ohms (par défaut 0).

        Returns:
            float: La force électromagnétique en newtons.
        """
        return float(-1*self.cable.longueur_cable**2*Bt**2*Vo*cos(self.cable.inclinaison_alpha)/(self.cable.resistance+Rc))

    def set_position(self, r=None, theta=None, phi=None):
        """
        Définit la position du satellite.

        Args:
            r (float, optional): La distance radiale en mètres.
            theta (float, optional): L'angle polaire en radians.
            phi (float, optional): L'angle azimutal en radians.
        """
        if r is None:
            r = self.__position[0]
        if theta is None:
            theta = self.__position[1]
        if phi is None:
            phi = self.__position[2]
        self.__position = [r, theta, phi]

    def get_r(self):
        """
        Obtient la distance radiale du satellite.

        Returns:
            float: La distance radiale en mètres.
        """
        return self.__position[0]

    def get_theta(self):
        """
        Obtient l'angle polaire du satellite.

        Returns:
            float: L'angle polaire en radians.
        """
        return self.__position[1]

    def get_phi(self):
        """
        Obtient l'angle azimutal du satellite.

        Returns:
            float: L'angle azimutal en radians.
        """
        return self.__position[2]

    def update_etat(self, position_sur_equateur, inclinaison_orbite):
        """
        Met à jour l'état du satellite en fonction de sa position sur l'équateur et de l'inclinaison de l'orbite.

        Args:
            position_sur_equateur (float): La position sur l'équateur en radians.
            inclinaison_orbite (float): L'inclinaison de l'orbite en degrés.
        """
        old_position = self.__position
        x, y, z = cs.sp2cart(old_position[0], 0, position_sur_equateur)
        matrice_de_rotation = cs.mx_rot_x(inclinaison_orbite / 180 * pi)
        x, y, z = cs.mx_apply(matrice_de_rotation, x, y, z)
        r, theta, phi = cs.cart2sp(x, y, z)
        theta = theta # = pi / 2 - theta dans le cas de la colatitude

        self.set_position(r, theta, phi)

        d_theta = theta - old_position[1]
        d_phi = phi - old_position[2]

        self.angle_nord_vitesse = atan2(d_phi, d_theta)

    def calcul_des_masses(self):
        """
        Calcule et affiche les différentes masses et résistances du satellite et du câble.
        """
        print(f'Resistance = {self.cable.resistance:0.1f} ohms')
        print(f'Section du cable = {self.cable.section*10**6:0.2f} mm^2')
        print(f'Masse total satellite = {self.mass:0.0f} kg')
        print(f'Masse cable = {self.cable.mass:0.2f} kg')
        masse_cable_systeme = self.cable.mass+self.cable.mass_ballast
        print(f'Masse cable + systeme de deployement = {masse_cable_systeme:0.2f} kg')
        print(f'Pourcentage de la masse totale = {masse_cable_systeme/self.mass*100:0.2f} %')
