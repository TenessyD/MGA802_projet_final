class SpaceBody():
    """
    Représente un corps céleste générique.

    Attributes:
        mass (float): La masse du corps céleste.
    """

    def __init__(self, mass=0):
        self.mass = mass


class Planet(SpaceBody):
    """
    Représente une planète.

    Attributes:
        mass (float): La masse de la planète.
        radius (float): Le rayon de la planète en mètres.
        color (str): La couleur de la planète.
    """

    def __init__(self,mass, radius=0,color='b'):
        super().__init__(mass)
        self.radius = radius    # [m]
        self.color = color


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
