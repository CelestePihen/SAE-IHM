class Produit:
    def __init__(self, nom: str, categorie: str, position_x: int = -1, position_y: int = -1):
        self.nom = nom
        self.categorie = categorie
        self.position_x = position_x
        self.position_y = position_y
    
    def est_positionne(self) -> bool:
        return self.position_x >= 0 and self.position_y >= 0