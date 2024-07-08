class Materiau:
    """
    Classe représentant un matériau avec sa densité et sa résistance linéaire.

    Attributs:
        densite (float): La densité du matériau en kg/m^3.
        resistance (float): La résistance linéaire du matériau en ohms par mètre.
    """
    def __init__(self, densite, resistance):
        """
        Initialise un objet Materiau.

        Args:
            densite (float): La densité du matériau en kg/m^3.
            resistance (float): La résistance linéaire du matériau en ohms par mètre.
        """
        self.densite = densite
        self.resistance = resistance