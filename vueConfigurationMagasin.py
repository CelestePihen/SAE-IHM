from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QFileDialog, QMessageBox, QTabWidget, QListWidget, QInputDialog,
    QDialog, QFormLayout, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt

import os
from PyQt6.QtCore import Qt
from ProjetModele import ProjetModele
from vueNouveauProjet import DialogueNouveauProjet
from vuePlanMagasin import VuePlanMagasin
from CheminModele import CheminModele

class VueConfigurationMagasin(QWidget):
    def __init__(self, modele: ProjetModele):
        super().__init__()
        self.modele = modele
        self.init_widgets()
        self.modele.projet_modifie.connect(self.mettre_a_jour_affichage)
        
        self.debut = False
        self.fin = False
        self.mode_inaccessible = False
    
    def init_widgets(self):
        layout: QVBoxLayout= QVBoxLayout(self)
        
        # barre d'outils
        toolbar_layout: QHBoxLayout= QHBoxLayout()
        
        self.btn_nouveau: QPushButton = QPushButton("Nouveau projet")
        self.btn_ouvrir: QPushButton = QPushButton("Ouvrir projet")
        self.btn_sauvegarder: QPushButton = QPushButton("Sauvegarder")
        self.btn_supprimer: QPushButton = QPushButton("Supprimer projet")
        
        toolbar_layout.addWidget(self.btn_nouveau)
        toolbar_layout.addWidget(self.btn_ouvrir)
        toolbar_layout.addWidget(self.btn_sauvegarder)
        toolbar_layout.addWidget(self.btn_supprimer)
        toolbar_layout.addStretch()
        
        layout.addLayout(toolbar_layout)
        
        # zone principale avec splitter
        splitter: QSplitter = QSplitter(Qt.Orientation.Horizontal)
        
        # panneau de gauche - configuration
        config_widget: QWidget = QWidget()
        config_layout: QVBoxLayout = QVBoxLayout(config_widget)
        
        # informations projet
        info_group: QGroupBox = QGroupBox("Informations du projet")
        info_layout: QFormLayout = QFormLayout(info_group)
        
        self.label_nom: QLabel = QLabel("-")
        self.label_auteur: QLabel = QLabel("-")
        self.label_date: QLabel = QLabel("-")
        self.label_magasin: QLabel = QLabel("-")
        
        info_layout.addRow("Nom :", self.label_nom)
        info_layout.addRow("Auteur :", self.label_auteur)
        info_layout.addRow("Date :", self.label_date)
        info_layout.addRow("Magasin :", self.label_magasin)
        
        config_layout.addWidget(info_group)
        
        # configuration du plan
        plan_group: QGroupBox= QGroupBox("Configuration du plan")
        plan_layout: QVBoxLayout= QVBoxLayout(plan_group)
        
        self.btn_charger_plan: QPushButton = QPushButton("Charger plan")
        plan_layout.addWidget(self.btn_charger_plan)
        
        # quadrillage
        quad_layout: QHBoxLayout = QHBoxLayout()
        quad_layout.addWidget(QLabel("Cases X :"))
        self.spin_x: QSpinBox = QSpinBox()
        self.spin_x.setRange(10, 100)
        self.spin_x.setValue(20)
        quad_layout.addWidget(self.spin_x)
        
        quad_layout.addWidget(QLabel("Cases Y :"))
        self.spin_y: QSpinBox = QSpinBox()
        self.spin_y.setRange(10, 100)
        self.spin_y.setValue(15)
        quad_layout.addWidget(self.spin_y)
        
        quad_layout.addWidget(QLabel("Taille :"))
        self.spin_taille: QSpinBox = QSpinBox()
        self.spin_taille.setRange(20, 100)
        self.spin_taille.setValue(30)
        quad_layout.addWidget(self.spin_taille)
        
        self.btn_appliquer_quad: QPushButton = QPushButton("Appliquer quadrillage")
        
        plan_layout.addLayout(quad_layout)
        plan_layout.addWidget(self.btn_appliquer_quad)
        
        config_layout.addWidget(plan_group)
        
        # gestion des produits
        produits_group :  QGroupBox = QGroupBox("Produits du magasin")
        produits_layout : QVBoxLayout = QVBoxLayout(produits_group)
        
        self.combo_produits_dispo : QComboBox = QComboBox()
        self.btn_ajouter_produit : QPushButton = QPushButton("Ajouter produit")
        
        produits_layout.addWidget(QLabel("Produits disponibles:"))
        produits_layout.addWidget(self.combo_produits_dispo)
        produits_layout.addWidget(self.btn_ajouter_produit)
        
        produits_layout.addWidget(QLabel("Produits du magasin:"))
        self.liste_produits_magasin : QListWidget = QListWidget()
        produits_layout.addWidget(self.liste_produits_magasin)
        
        self.btn_positionner : QPushButton = QPushButton("Positionner produit sélectionné")
        produits_layout.addWidget(self.btn_positionner)
        
        config_layout.addWidget(produits_group)
        config_layout.addStretch()
        
        splitter.addWidget(config_widget)
        
        self.btn_inaccessible : QPushButton = QPushButton("Zone inaccessible")
        produits_layout.addWidget(self.btn_inaccessible)
        self.btn_debut : QPushButton = QPushButton("Entrée magasin")
        produits_layout.addWidget(self.btn_debut)
        self.btn_fin : QPushButton = QPushButton("Sortie magasin")
        produits_layout.addWidget(self.btn_fin)
        
        # vue du plan
        self.vue_plan = VuePlanMagasin()
        splitter.addWidget(self.vue_plan)
        
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)
        
         # connexions
        self.connecter_signaux()
        self.charger_produits_disponibles()
    
    def connecter_signaux(self):
        """Connecte les signaux aux slots"""
        self.btn_nouveau.clicked.connect(self.nouveau_projet)
        self.btn_ouvrir.clicked.connect(self.ouvrir_projet)
        self.btn_sauvegarder.clicked.connect(self.sauvegarder_projet)
        self.btn_supprimer.clicked.connect(self.supprimer_projet)
        self.btn_charger_plan.clicked.connect(self.charger_plan)
        self.btn_appliquer_quad.clicked.connect(self.appliquer_quadrillage)
        self.btn_ajouter_produit.clicked.connect(self.ajouter_produit)
        self.btn_positionner.clicked.connect(self.positionner_produit)
        
        self.vue_plan.produit_positionne.connect(self.produit_positionne)
        self.vue_plan.debut_position.connect(self.debut_positionne)
        self.vue_plan.fin_position.connect(self.fin_positionnee)
        
        self.btn_debut.clicked.connect(self.position_deb)
        self.btn_fin.clicked.connect(self.position_fin)
        self.btn_inaccessible.clicked.connect(self.activer_mode_inaccessible)
        self.vue_plan.zone_inaccessible_selectionnee.connect(self.zone_inaccessible_selectionnee)
        
    def activer_mode_inaccessible(self):
        """Active le mode sélection de zones inaccessibles"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        if not self.mode_inaccessible:
            self.mode_inaccessible = True
            self.vue_plan.definir_mode_inaccessible(True)
            self.btn_inaccessible.setText("Arrêter la sélection")
            self.btn_inaccessible.setStyleSheet("background-color: #ff6666; color: white;")
            QMessageBox.information(self, "Mode sélection", 
                                "Mode zones inaccessibles activé !\n\n"
                                "• Cliquez sur une case accessible pour la rendre inaccessible\n"
                                "• Cliquez sur une case inaccessible pour la rendre accessible\n"
                                "• Cliquez sur 'Arrêter sélection' pour terminer")
        else:
            self.mode_inaccessible = False
            self.vue_plan.definir_mode_inaccessible(False)
            self.btn_inaccessible.setText("Zone inaccessible")
            self.btn_inaccessible.setStyleSheet("")
            QMessageBox.information(self, "Mode terminé", 
                                "Mode sélection de zones inaccessibles désactivé.")

    def zone_inaccessible_selectionnee(self, x, y, est_inaccessible):
        """Gère la sélection/désélection d'une zone inaccessible"""
        chemin_modele = CheminModele(self.modele)
        if est_inaccessible:
            # Utiliser la méthode ajouter_obstacle de CheminModele
            if chemin_modele.ajouter_obstacle(x, y):
                self.modele.ajouter_position_inaccessible(x, y)
                print(f"Zone ({x}, {y}) rendue inaccessible")
                # Mettre à jour le modèle pour déclencher le signal
            else:
                self.modele.supprimer_position_inaccessible(x, y)
                print(f"Zone ({x}, {y}) déjà inaccessible")
        else:
            # Utiliser la méthode supprimer_obstacle de CheminModele
            if chemin_modele.supprimer_obstacle(x, y):
                print(f"Zone ({x}, {y}) rendue accessible")
                # Mettre à jour le modèle pour déclencher le signal
            else:
                print(f"Zone ({x}, {y}) déjà accessible")
                
    def position_deb(self):
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        if self.debut == False:
            self.debut = True
            self.vue_plan.definir_debut_position(True)
            # Active le mode positionnement pour le début dans la vue plan
            QMessageBox.information(self, "Mode positionnement", 
                                "Cliquez sur le plan pour positionner l'entrée du magasin")
        
    def position_fin(self):
        """Active le mode positionnement pour la sortie du magasin"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        if self.fin == False:
            self.fin = True
            self.vue_plan.definir_fin_position(True)
            # Active le mode positionnement pour la fin dans la vue plan
            QMessageBox.information(self, "Mode positionnement", 
                                "Cliquez sur le plan pour positionner la sortie du magasin")
    
    def debut_positionne(self, x, y):
        """Gère le positionnement du début"""
        success = self.modele.positionner_debut(x, y)
        if success:
            QMessageBox.information(self, "Succès", f"Entrée positionnée en ({x}, {y})")
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de positionner l'entrée.")
    
    def fin_positionnee(self, x, y):
        """Gère le positionnement de la fin"""
        success = self.modele.positionner_fin(x, y)
        if success:
            QMessageBox.information(self, "Succès", f"Sortie positionnée en ({x}, {y})")
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de positionner la sortie.")
        
    def produit_positionne(self, nom, x, y):
        """Positionne le produit dans le modèle et met à jour l'affichage"""
        success = self.modele.positionner_produit(nom, x, y)
        if not success:
            QMessageBox.warning(self, "Erreur", f"Impossible de positionner le produit '{nom}'.")     
    
    def charger_produits_disponibles(self):
        """Charge les produits disponibles dans le combo"""
        self.combo_produits_dispo.clear()
        for produit in self.modele.produits_disponibles:
            self.combo_produits_dispo.addItem(f"{produit.nom} ({produit.categorie})", produit.nom)
    
    def nouveau_projet(self):
        """Crée un nouveau projet"""
        dialog = DialogueNouveauProjet(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if all(data.values()):
                success = self.modele.nouveau_projet(
                    data['nom'], data['auteur'], data['nom_magasin'], data['adresse']
                )
                if not success:
                    QMessageBox.warning(self, "Erreur", "Un projet avec ce nom existe déjà.")
                else:
                    QMessageBox.information(self, "Success", "Projet créé avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires.")
    
    def ouvrir_projet(self):
        """Ouvre un projet existant"""
        projets = self.modele.lister_projets()
        if not projets:
            QMessageBox.information(self, "Information", "Aucun projet disponible.")
            return
        
        projet, ok = QInputDialog.getItem(self, "Ouvrir projet", "Choisir un projet:", projets, 0, False)
        if ok:
            success = self.modele.charger_projet(projet)
            if success:
                QMessageBox.information(self, "Succès", "Projet chargé avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de charger le projet.")
    
    def sauvegarder_projet(self):
        """Sauvegarde le projet courant"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        success = self.modele.sauvegarder_projet()
        if success:
            QMessageBox.information(self, "Succès", "Projet sauvegardé avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de la sauvegarde.")
    
    def supprimer_projet(self):
        """Supprime un projet"""
        projets = self.modele.lister_projets()
        if not projets:
            QMessageBox.information(self, "Information", "Aucun projet à supprimer.")
            return
        
        projet, ok = QInputDialog.getItem(self, "Supprimer projet", "Choisir un projet:", projets, 0, False)
        if ok:
            reply = QMessageBox.question(self, "Confirmation", 
                                       f"Supprimer définitivement le projet '{projet}' ?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                success = self.modele.supprimer_projet(projet)
                if success:
                    QMessageBox.information(self, "Succès", "Projet supprimé.")
                else:
                    QMessageBox.warning(self, "Erreur", "Erreur lors de la suppression.")
    
    def charger_plan(self):
        """Charge un plan d'image"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        fichier, _ = QFileDialog.getOpenFileName(
            self, "Charger plan", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if fichier:
            success = self.modele.charger_plan_image(fichier)
            if success:
                self.vue_plan.charger_plan(self.modele.projet_courant.plan_image)
                QMessageBox.information(self, "Succès", "Plan chargé avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors du chargement du plan.")
    
    def appliquer_quadrillage(self):
        """Applique les paramètres du quadrillage"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        x = self.spin_x.value()
        y = self.spin_y.value()
        taille = self.spin_taille.value()
        
        self.modele.definir_quadrillage(x, y, taille)
        self.vue_plan.definir_quadrillage(x, y, taille)
    
    def ajouter_produit(self):
        """Ajoute un produit au magasin"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        nom_produit = self.combo_produits_dispo.currentData()
        if nom_produit:
            success = self.modele.ajouter_produit_magasin(nom_produit)
            if not success:
                QMessageBox.warning(self, "Erreur", "Produit déjà ajouté au magasin.")
    
    def positionner_produit(self):
        """Active le mode positionnement pour le produit sélectionné"""
        if not self.modele.projet_courant:
            QMessageBox.warning(self, "Erreur", "Aucun projet ouvert.")
            return
        
        current_item = self.liste_produits_magasin.currentItem()
        if current_item:
            # prend le nom du produit
            texte_item = current_item.text()
            # extrait le nom entre le premier espace et la première parenthèse
            parties = texte_item.split(" ", 1)
            if len(parties) > 1:
                reste = parties[1]
                nom_produit = reste.split(" (")[0]  # Extraire le nom avant la catégorie
                self.vue_plan.definir_produit_a_positionner(nom_produit)
                QMessageBox.information(self, "Mode positionnement", 
                                      f"Cliquez sur le plan pour positionner '{nom_produit}'")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'extraire le nom du produit.")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit à positionner.")
    
    def mettre_a_jour_affichage(self):
        """Met à jour tous les éléments d'affichage"""
        if self.modele.projet_courant:
            projet = self.modele.projet_courant
        
            self.label_nom.setText(projet.nom)
            self.label_auteur.setText(projet.auteur)
            self.label_date.setText(projet.date_creation)
            self.label_magasin.setText(f"{projet.nom_magasin} - {projet.adresse_magasin}")
        
            if projet.quadrillage_x > 0:
                self.spin_x.setValue(projet.quadrillage_x)
            if projet.quadrillage_y > 0:
                self.spin_y.setValue(projet.quadrillage_y)
            if projet.taille_case > 0:
                self.spin_taille.setValue(projet.taille_case)
        
            if projet.plan_image and os.path.exists(projet.plan_image):
                self.vue_plan.charger_plan(projet.plan_image)
                if projet.quadrillage_x > 0 and projet.quadrillage_y > 0:
                    self.vue_plan.definir_quadrillage(projet.quadrillage_x, projet.quadrillage_y, projet.taille_case)
        
            self.liste_produits_magasin.clear()
            for produit in projet.produits:
                status = "✓" if produit.est_positionne() else "○"
                position = f"({produit.position_x},{produit.position_y})" if produit.est_positionne() else ""
                texte = f"{status} {produit.nom} ({produit.categorie}) {position}"
                self.liste_produits_magasin.addItem(texte)
            
                if produit.est_positionne():
                    self.vue_plan.afficher_produit(produit.nom, produit.position_x, produit.position_y)
        
            # Gestion sécurisée des points début/fin (conversion liste -> tuple)
            if projet.debut is not None:
                debut = tuple(projet.debut) if isinstance(projet.debut, list) else projet.debut
                self.vue_plan.afficher_entree(debut[0], debut[1])
            
            if projet.fin is not None:
                fin = tuple(projet.fin) if isinstance(projet.fin, list) else projet.fin
                self.vue_plan.afficher_sortie(fin[0], fin[1])
        
            # Normaliser les positions inaccessibles en tuples
            positions_inaccessibles_tuples = set()
            for pos in projet.positions_inaccessibles:
                if isinstance(pos, list):
                    positions_inaccessibles_tuples.add(tuple(pos))
                else:
                    positions_inaccessibles_tuples.add(pos)
            
            # Supprimer les zones qui ne sont plus inaccessibles
            for cle_zone, item in list(self.vue_plan.zones_inaccessibles_items.items()):
                if cle_zone not in positions_inaccessibles_tuples:
                    self.vue_plan.scene.removeItem(item)
                    del self.vue_plan.zones_inaccessibles_items[cle_zone]
        
            # Afficher les nouvelles zones inaccessibles
            for pos in projet.positions_inaccessibles:
                if isinstance(pos, list):
                    x, y = pos[0], pos[1]
                else:
                    x, y = pos
                self.vue_plan.afficher_zone_inaccessible(x, y)
        else:
            self.label_nom.setText("-")
            self.label_auteur.setText("-")
            self.label_date.setText("-")
            self.label_magasin.setText("-")
            self.liste_produits_magasin.clear()
            self.vue_plan.scene.clear()
            self.vue_plan.zones_inaccessibles_items.clear()
