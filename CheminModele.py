from ProjetModele import ProjetModele, Projet

class CheminModele:
    """Modèle pour le calcul du chemin optimal"""
   
    def __init__(self, projetModele: ProjetModele):
        self.projetModele: ProjetModele = projetModele
        self.projet: Projet = projetModele.projet_courant
        self.grille_accessible: list[list[bool]] = self._generer_grille_accessible()
   
    def _generer_grille_accessible(self) -> list[list[bool]]:
        """Génère une grille des cases accessibles basée sur les positions inaccessibles du projet"""
        if not self.projet.quadrillage_x or not self.projet.quadrillage_y:
            return []
       
        grille: list[list[bool]] = []
        for y in range(self.projet.quadrillage_y):
            ligne: list[bool] = []
            for x in range(self.projet.quadrillage_x):
                # Convertir les listes en tuples pour la comparaison
                position_actuelle = (x, y)
                est_inaccessible = False
                
                for pos_inaccess in self.projet.positions_inaccessibles:
                    # Gérer les cas où pos_inaccess peut être une liste ou un tuple
                    if isinstance(pos_inaccess, list):
                        pos_tuple = tuple(pos_inaccess)
                    else:
                        pos_tuple = pos_inaccess
                    
                    if position_actuelle == pos_tuple:
                        est_inaccessible = True
                        break
                
                ligne.append(not est_inaccessible)
            grille.append(ligne)
        
        return grille
   
    def calculer_chemin_optimal(self, liste_courses: list[str]) -> list[tuple[int, int]]:
        """Calcule le chemin optimal pour une liste de courses en utilisant les points début/fin du projet"""
        if not self.projet.produits or not liste_courses:
            return []
       
        # trouver les positions des produits demandés
        positions_produits: list[tuple[int, int]] = []
        for nom_produit in liste_courses:
            for produit in self.projet.produits:
                if produit.nom == nom_produit and produit.est_positionne():
                    positions_produits.append((produit.position_x, produit.position_y))
                    break
       
        if not positions_produits:
            return []
       
        # Conversion des listes en tuples si nécessaire
        point_debut = tuple(self.projet.debut) if isinstance(self.projet.debut, list) else self.projet.debut
        point_fin = tuple(self.projet.fin) if isinstance(self.projet.fin, list) else self.projet.fin
        
        # vérifier que les points début et fin sont valides
        if not self._est_position_valide(point_debut) or not self._est_position_valide(point_fin):
            return []
       
        # Algorithme de recherche du plus proche voisin (glouton)
        chemin_complet: list = []
        position_actuelle: tuple[int, int] = point_debut
        produits_restants: list[tuple[int, int]] = positions_produits.copy()
       
        while produits_restants:
            # trouver le produit le plus proche
            produit_proche: tuple[int, int] = None
            distance_min: float = float('inf')
            
            for produit_pos in produits_restants:
                distance: float = self._dijkstra_distance(position_actuelle, produit_pos)
                if distance < distance_min:
                    distance_min = distance
                    produit_proche = produit_pos
           
            if produit_proche is None:
                break
                
            # calculer le chemin vers ce produit
            chemin_vers_produit: list[tuple[int, int]] = self._dijkstra(position_actuelle, produit_proche)
            
            if chemin_vers_produit:
                # éviter la duplication du point de départ sauf pour le premier segment
                if chemin_complet:
                    chemin_complet.extend(chemin_vers_produit[1:])
                else:
                    chemin_complet.extend(chemin_vers_produit)
                position_actuelle = produit_proche
           
            produits_restants.remove(produit_proche)
       
        # aller à la sortie (caisse)
        chemin_vers_fin: list[tuple[int, int]] = self._dijkstra(position_actuelle, point_fin)
        if chemin_vers_fin and len(chemin_vers_fin) > 1:
            chemin_complet.extend(chemin_vers_fin[1:])
       
        return chemin_complet
    
    def _est_position_valide(self, position: tuple[int, int]) -> bool:
        """Vérifie si une position est valide dans la grille"""
        x, y = position
        if not self.projet.quadrillage_x or not self.projet.quadrillage_y:
            return False
            
        # Vérifier les limites
        if not (0 <= x < self.projet.quadrillage_x and 0 <= y < self.projet.quadrillage_y):
            return False
        
        return True  # La position est valide si on arrive ici
    
    def _dijkstra_distance(self, debut: tuple[int, int], fin: tuple[int, int]) -> float:
        """Calcule la distance réelle entre deux points avec Dijkstra"""
        chemin: list[tuple[int, int]] = self._dijkstra(debut, fin)
        return len(chemin) - 1 if chemin else float('inf')
   
    def _dijkstra(self, debut: tuple[int, int], fin: tuple[int, int]) -> list[tuple[int, int]]:
        """Implémente l'algorithme de Dijkstra pour trouver le plus court chemin"""
        distances = {}
        precedents = {}
        visite = []
        
        distances[debut] = 0
        visite.append((0, debut))
        
        while visite:
            # trouve le noeud non visité avec la plus petite distance
            visite.sort(key=lambda x: x[0])
            distance_courante, noeud_courant = visite.pop(0)
            
            if noeud_courant == fin:
                break
                
            # si on a déjà trouvé un meilleur chemin
            if noeud_courant in distances and distance_courante > distances[noeud_courant]:
                continue
            
            x, y = noeud_courant
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                voisin = (x + dx, y + dy)
                
                if not self._est_position_valide(voisin):
                    continue
                    
                nouvelle_distance = distance_courante + 1
                
                if voisin not in distances or nouvelle_distance < distances[voisin]:
                    distances[voisin] = nouvelle_distance
                    precedents[voisin] = noeud_courant
                    visite.append((nouvelle_distance, voisin))
        
        if fin not in precedents:
            return []
            
        chemin = []
        noeud_courant = fin
        while noeud_courant != debut:
            chemin.append(noeud_courant)
            noeud_courant = precedents[noeud_courant]
        chemin.append(debut)
        
        return list(reversed(chemin))
    
    def ajouter_obstacle(self, x: int, y: int) -> bool:
        """Ajoute un obstacle dans le projet et met à jour la grille"""
        if not self._est_position_valide((x, y)):
            return False
        
        if (x, y) in self.projet.positions_inaccessibles:
            return False
        
        self.projet.positions_inaccessibles.append((x, y))
        return True

    def supprimer_obstacle(self, x: int, y: int) -> bool:
        """Supprime un obstacle du projet et met à jour la grille"""
        if not self._est_position_valide((x, y)):
            return False
        
        # Convertir les coordonnées en liste pour la comparaison
        position = [x, y]
        
        if position not in self.projet.positions_inaccessibles:
            return False
        
        self.projet.positions_inaccessibles.remove(position)
        return True