from modele.produit import Produit

class Projet:
    def __init__(self, nom: str, auteur: str, date_creation: str, 
                 nom_magasin: str, adresse_magasin: str, plan_image: str = "",
                 quadrillage_x: int = 0, quadrillage_y: int = 0, 
                 taille_case: int = 30, produits: list[Produit] = None):
        self.nom = nom
        self.auteur = auteur
        self.date_creation = date_creation
        self.nom_magasin = nom_magasin
        self.adresse_magasin = adresse_magasin
        self.plan_image = plan_image
        self.quadrillage_x = quadrillage_x
        self.quadrillage_y = quadrillage_y
        self.taille_case = taille_case
        
        if produits is not None:
            self.produits = produits
        else:
            self.produits = []