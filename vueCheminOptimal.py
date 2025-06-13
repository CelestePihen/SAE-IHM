import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QMessageBox, QListWidget, QSplitter
)
from PyQt6.QtCore import Qt
from ProjetModele import ProjetModele
from vuePlanMagasin import VuePlanMagasin
from CheminModele import CheminModele

class VueCalculChemin(QWidget):
    """Vue pour le calcul et l'affichage du chemin optimal"""
    
    def __init__(self, modele: ProjetModele):
        super().__init__()
        self.modele = modele
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Sélection du magasin
        magasin_layout = QHBoxLayout()
        magasin_layout.addWidget(QLabel("Magasin :"))
        self.combo_magasins = QComboBox()
        self.btn_charger_magasin = QPushButton("Charger")
        magasin_layout.addWidget(self.combo_magasins)
        magasin_layout.addWidget(self.btn_charger_magasin)
        magasin_layout.addStretch()
        
        layout.addLayout(magasin_layout)
        
        # Zone principale avec splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panneau de gauche - Liste de courses
        courses_widget = QWidget()
        courses_layout = QVBoxLayout(courses_widget)
        
        courses_layout.addWidget(QLabel("Liste de courses :"))
        
        # Produits disponibles
        self.liste_produits_dispo = QListWidget()
        self.liste_produits_dispo.setMaximumHeight(200)
        courses_layout.addWidget(QLabel("Produits disponibles :"))
        courses_layout.addWidget(self.liste_produits_dispo)
        
        self.btn_ajouter_course = QPushButton("Ajouter à la liste")
        courses_layout.addWidget(self.btn_ajouter_course)
        
        # Liste de courses
        self.liste_courses = QListWidget()
        courses_layout.addWidget(QLabel("Ma liste de courses :"))
        courses_layout.addWidget(self.liste_courses)
        
        btn_layout = QHBoxLayout()
        self.btn_retirer_course = QPushButton("Retirer")
        self.btn_vider_courses = QPushButton("Vider")
        
        self.btn_calculer_chemin = QPushButton("Calculer chemin optimal")
        self.btn_calculer_chemin.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        courses_layout.addWidget(self.btn_calculer_chemin)
        
        # Informations sur le chemin
        self.label_info_chemin = QLabel("Aucun chemin calculé")
        courses_layout.addWidget(self.label_info_chemin)
        
        courses_layout.addStretch()
        splitter.addWidget(courses_widget)
        
        # Vue du plan avec chemin
        self.vue_plan_chemin = VuePlanMagasin()
        splitter.addWidget(self.vue_plan_chemin)
        
        splitter.setSizes([350, 650])
        layout.addWidget(splitter)
        
        # Connexions
        self.actualiser_liste_magasins()
        self.connecter_signaux()

    
    def connecter_signaux(self):
        """Connecte les signaux aux slots"""
        self.btn_charger_magasin.clicked.connect(self.charger_magasin)
        self.btn_ajouter_course.clicked.connect(self.ajouter_a_liste_courses)
        self.btn_retirer_course.clicked.connect(self.retirer_de_liste_courses)
        self.btn_vider_courses.clicked.connect(self.vider_liste_courses)
        self.btn_calculer_chemin.clicked.connect(self.calculer_chemin)
    
    def actualiser_liste_magasins(self):
        """Met à jour la liste des magasins disponibles"""
        self.combo_magasins.clear()
        projets = self.modele.lister_projets()
        for projet in projets:
            self.combo_magasins.addItem(projet)
    
    def charger_magasin(self):
        """Charge le magasin sélectionné"""
        nom_projet = self.combo_magasins.currentText()
        if nom_projet:
            success = self.modele.charger_projet(nom_projet)
            if success:
                self.afficher_magasin()
                self.actualiser_produits_disponibles()
                QMessageBox.information(self, "Succès", f"Magasin '{nom_projet}' chargé.")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de charger le magasin.")
    
    def afficher_magasin(self):
        """Affiche le plan du magasin chargé"""
        if not self.modele.projet_courant:
            return
        
        projet = self.modele.projet_courant
        
        # Charger le plan
        if projet.plan_image and os.path.exists(projet.plan_image):
            self.vue_plan_chemin.charger_plan(projet.plan_image)
            
            # Appliquer le quadrillage
            if projet.quadrillage_x > 0 and projet.quadrillage_y > 0:
                self.vue_plan_chemin.definir_quadrillage(projet.quadrillage_x, projet.quadrillage_y, projet.taille_case)
            
            # Afficher les produits positionnés
            for produit in projet.produits:
                if produit.est_positionne():
                    self.vue_plan_chemin.afficher_produit(produit.nom, produit.position_x, produit.position_y)
                    
            if projet.debut is not None:
                self.vue_plan_chemin.afficher_entree(projet.debut[0], projet.debut[1])
                
            if projet.fin is not None:
                self.vue_plan_chemin.afficher_sortie(projet.fin[0], projet.fin[1])
            
            if projet.positions_inaccessibles:
                for cle_zone, item in list(self.vue_plan_chemin.zones_inaccessibles_items.items()):
                    if cle_zone not in [(x, y) for x, y in projet.positions_inaccessibles]:
                        self.vue_plan_chemin.scene.removeItem(item)
                        self.vue_plan_chemin.zones_inaccessibles_items.pop(cle_zone)
                
                # Ensuite afficher les nouvelles zones
                for x, y in projet.positions_inaccessibles:
                    self.vue_plan_chemin.afficher_zone_inaccessible(x, y)

    def actualiser_produits_disponibles(self):
        """Met à jour la liste des produits disponibles dans le magasin"""
        self.liste_produits_dispo.clear()
        if self.modele.projet_courant:
            for produit in self.modele.projet_courant.produits:
                if produit.est_positionne():
                    self.liste_produits_dispo.addItem(f"{produit.nom} ({produit.categorie})")
    
    def ajouter_a_liste_courses(self):
        """Ajoute un produit à la liste de courses"""
        current_item = self.liste_produits_dispo.currentItem()
        if current_item:
            nom_produit = current_item.text().split(" (")[0]
            
            # Vérifier si déjà dans la liste
            for i in range(self.liste_courses.count()):
                if self.liste_courses.item(i).text().startswith(nom_produit):
                    return
            
            self.liste_courses.addItem(current_item.text())
    
    def retirer_de_liste_courses(self):
        """Retire un produit de la liste de courses"""
        current_row = self.liste_courses.currentRow()
        if current_row >= 0:
            self.liste_courses.takeItem(current_row)
    
    def vider_liste_courses(self):
        """Vide la liste de courses"""
        self.liste_courses.clear()
    
    def calculer_chemin(self):
        """Calcule et affiche le chemin optimal"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun magasin chargé.")
            return
        
        if self.liste_courses.count() == 0:
            QMessageBox.warning(self, "Erreur", "Liste de courses vide.")
            return
        
        # Extraire les noms des produits
        produits_courses = []
        for i in range(self.liste_courses.count()):
            nom_produit = self.liste_courses.item(i).text().split(" (")[0]
            produits_courses.append(nom_produit)
            
        # Calculer le chemin
        modele_chemin = CheminModele(self.modele)
        chemin = modele_chemin.calculer_chemin_optimal(produits_courses)
        
        if chemin:
            # Afficher le chemin sur le plan
            self.afficher_magasin()  # Réafficher le magasin proprement
            self.vue_plan_chemin.afficher_chemin(chemin)
            
            # Mettre à jour les informations
            distance_totale = len(chemin) - 1  # Nombre de déplacements
            
            self.label_info_chemin.setText(
                f"Chemin calculé :\n"
                f"• {len(produits_courses)} produits à collecter\n"
                f"• {distance_totale} déplacements\n"
            )
            
            QMessageBox.information(self, "Succès", "Chemin optimal calculé et affiché en vert!")
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de calculer un chemin optimal.")
            self.label_info_chemin.setText("Erreur dans le calcul du chemin")