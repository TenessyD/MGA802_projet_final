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

class cable:
    def __init__(self, longueur_cable, section, materiau, inclinaison_alpha=35.26, mass_ballast = 10, Rc = 0):
        self.mass_ballast = mass_ballast
        self.materiau = materiau
        self.longueur_cable = longueur_cable
        self.section = section*10**-6 #mm2 to m2
        self.mass = self.materiau.densite*self.longueur_cable*self.section
        self.volume = self.section*self.longueur_cable
        self.resistance = self.materiau.resistance/self.section*self.longueur_cable or 1
        self.inclinaison_alpha = inclinaison_alpha/180*pi
        self.resistance_de_controle = Rc

class satellite_magnetique(Satellite):

    def __init__(self, mass, cross_surface, cable, position=None, cx=2):
        super().__init__(mass, cross_surface, cx)
        if position is None:
            position = [0, 0, 0]
        self.__position = position #r, theta, phi
        self.angle_nord_vitesse = 0
        self.cable = cable
    def calculer_Fe(self, Bt, Vo, Rc=0):
        return float(-1*self.cable.longueur_cable**2*Bt**2*Vo*cos(self.cable.inclinaison_alpha)/(self.cable.resistance+Rc))

    def set_position(self, r=None, theta=None, phi=None):
        if r is None:
            r = self.__position[0]
        if theta is None:
            theta = self.__position[1]
        if phi is None:
            phi = self.__position[2]
        self.__position = [r, theta, phi]

    def get_r(self):
        return self.__position[0]

    def get_theta(self):
        return self.__position[1]

    def get_phi(self):
        return self.__position[2]

    def update_etat(self, position_sur_equateur, inclinaison_orbite):
        old_position = self.__position
        x, y, z = cs.sp2cart(old_position[0], 0, position_sur_equateur)
        matrice_de_rotation = cs.mx_rot_x(inclinaison_orbite / 180 * pi)
        x, y, z = cs.mx_apply(matrice_de_rotation, x, y, z)
        r, theta, phi = cs.cart2sp(x, y, z)
        theta = theta # = pi / 2 - theta dans le cas de la colatitude

        self.set_position(r, theta, phi)

        d_theta = theta - old_position[1]
        d_phi = phi - old_position[2]

        self.angle_nord_vitesse = atan2(d_phi, d_theta) #ya erreur jpense

    def calcul_des_masses(self):
        print(f'Resistance = {self.cable.resistance} ohms')
        print(f'Section du cable = {self.cable.section*10**6:0.2f} mm^2')
        print(f'Masse total satellite = {self.mass} kg')
        print(f'Masse cable = {self.cable.mass} kg')
        masse_cable_systeme = self.cable.mass+self.cable.mass_ballast
        print(f'Masse cable + systeme de deployement = {masse_cable_systeme} kg')
        print(f'Pourcentage = {masse_cable_systeme/self.mass*100:0.2f} %')
