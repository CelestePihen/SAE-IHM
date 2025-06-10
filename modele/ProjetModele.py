from modele.ProduitModele import Produit
import json, os, shutil
from PyQt6.QtCore import pyqtSignal, QObject
from datetime import datetime
from dataclasses import asdict

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
            
class ModeleProjet(QObject):
    projet_modifie: pyqtSignal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.projet_courant: Projet = None
        self.produits_disponibles: list[Produit] = self._charger_produits_disponibles()
        self.dossier_projets: str = "projets"
        os.makedirs(self.dossier_projets, exist_ok=True)
    
    def _charger_produits_disponibles(self) -> list[Produit]:
        """Charge la liste des produits disponibles depuis le fichier JSON"""
        produits: list = []
        try:
            with open('liste_produits.json', 'r', encoding='utf-8') as f:
                data: dict = json.load(f)
            
            # on parcourt chaque catégorie avec ses produits
            for categorie, noms_produits in data.items():
                for nom in noms_produits:
                    produits.append(Produit(nom, categorie))    
            return produits
        except Exception as e:
            print(f"Erreur lors du chargement des produits: {e}")
            return [Produit("Bigorneaux", "Poissons"), Produit("Agneau", "Viandes"), Produit("Abricot", "Fruits")]
    
    def nouveau_projet(self, nom: str, auteur: str, nom_magasin: str, adresse_magasin: str) -> bool:
        """Crée un nouveau projet"""
        if self._projet_existe(nom):
            return False
        
        # strftime permet de formater la date sous format année-mois-jour heure:minute:seconde
        self.projet_courant = Projet(
            nom=nom, auteur=auteur,
            date_creation=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            nom_magasin=nom_magasin, adresse_magasin=adresse_magasin
        )
        self.projet_modifie.emit()
        return True
    
    def charger_plan_image(self, chemin_image: str) -> bool:
        """Charge un plan avec son image associé pour le projet"""
        if not self.projet_courant:
            return False
        
        dossier_projet: str = os.path.join(self.dossier_projets, self.projet_courant.nom)
        os.makedirs(dossier_projet, exist_ok=True)
        
        nom_image = os.path.basename(chemin_image)
        nouveau_chemin: str = os.path.join(dossier_projet, nom_image)
        shutil.copy2(chemin_image, nouveau_chemin)
        
        self.projet_courant.plan_image = nouveau_chemin
        self.projet_modifie.emit()
        return True
    
    def definir_quadrillage(self, x: int, y: int, taille_case: int):
        """Définit les paramètres du quadrillage"""
        if self.projet_courant:
            self.projet_courant.quadrillage_x = x
            self.projet_courant.quadrillage_y = y
            self.projet_courant.taille_case = taille_case
            self.projet_modifie.emit()
    
    def ajouter_produit_magasin(self, nom_produit: str) -> bool:
        """Ajoute un produit au magasin"""
        if not self.projet_courant:
            return False
        
        # permet de trouver le produit dans la liste de produits grâce à son nom
        produit_source: Produit = None
        for p in self.produits_disponibles:
            if p.nom == nom_produit:
                produit_source = p
                break
        
        if not produit_source:
            return False
        
        # permet de vérifier s'il n'est pas déjà ajouté
        for p in self.projet_courant.produits:
            if p.nom == nom_produit:
                return False
        
        # ajoute le produit
        nouveau_produit: Produit = Produit(produit_source.nom, produit_source.categorie)
        self.projet_courant.produits.append(nouveau_produit)
        self.projet_modifie.emit()
        return True
    
    def positionner_produit(self, nom_produit: str, x: int, y: int) -> bool:
        """Positionne un produit sur le quadrillage"""
        if not self.projet_courant:
            return False
        
        for produit in self.projet_courant.produits:
            if produit.nom == nom_produit:
                produit.position_x = x
                produit.position_y = y
                self.projet_modifie.emit()
                return True
        return False
    
    def sauvegarder_projet(self) -> bool:
        """Sauvegarde le projet courant"""
        if not self.projet_courant:
            return False
        
        dossier_projet = self.dossier_projets / self.projet_courant.nom
        os.makedirs(dossier_projet, exist_ok=True)
        
        # permet de sauvegarder le projet dans un fichier JSON
        # asdict convertit un Projet (l'objet) en dictionnaire
        fichier_projet: str = os.path.join(dossier_projet, f"{self.projet_courant.nom}.json")
        with open(fichier_projet, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.projet_courant), f, ensure_ascii=False, indent=2)
        
        return True
    
    def charger_projet(self, nom_projet: str) -> bool:
        """Charge un projet existant"""
        fichier_projet: str = os.path.join(self.dossier_projets, nom_projet, f"{nom_projet}.json")
        if not os.path.exists(fichier_projet):
            return False
        
        with open(fichier_projet, 'r', encoding='utf-8') as f:
            data: dict = json.load(f)
        
        # on refait les objets Produit à partir des données
        # **p_data permet de décomposer le dictionnaire en arguments
        produits: list[Produit] = []
        for p_data in data.get('produits', []):
            produits.append(Produit(**p_data))
        
        data['produits'] = produits
        # **data permet de décomposer le dictionnaire en arguments
        self.projet_courant = Projet(**data)
        self.projet_modifie.emit()
        return True
    
    def lister_projets(self) -> list[str]:
        """Liste les projets disponibles dans le dossier projets"""
        projets: list = []
        for nom_dossier in os.listdir(self.dossier_projets):
            chemin_dossier = os.path.join(self.dossier_projets, nom_dossier)
            if os.path.isdir(chemin_dossier):
                fichier_projet = os.path.join(chemin_dossier, f"{nom_dossier}.json")
                if os.path.exists(fichier_projet):
                    projets.append(nom_dossier)
        return projets
    
    def supprimer_projet(self, nom_projet: str) -> bool:
        """Supprime un projet"""
        try:
            dossier_projet = self.dossier_projets / nom_projet
            if os.path.exists(dossier_projet):
                shutil.rmtree(dossier_projet)
                if self.projet_courant and self.projet_courant.nom == nom_projet:
                    self.projet_courant = None
                    self.projet_modifie.emit()
                return True
        except Exception:
            pass
        return False
    
    def _projet_existe(self, nom: str) -> bool:
        """Vérifie si un projet existe déjà"""
        return nom in self.lister_projets()