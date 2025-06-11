from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QFileDialog, QMessageBox, QTabWidget, QListWidget, QInputDialog,
    QDialog, QFormLayout, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt


from PyQt6.QtCore import Qt
from modele.ProjetModele import ProjetModele
from vueNouveauProjet import DialogueNouveauProjet
from vue.vuePlanMagasin import VuePlanMagasin

class VueConfigurationMagasin(QWidget):
    def __init__(self, modele: ProjetModele):
        super().__init__()
        self.modele = modele
        self.init_widgets()
        self.modele.projet_modifie.connect(self.mettre_a_jour_affichage)
    
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
                    self.vue_plan.definir_quadrillage(projet.quadrillage_x, 
                                                    projet.quadrillage_y, 
                                                    projet.taille_case)
            
            self.liste_produits_magasin.clear()
            for produit in projet.produits:
                status = "✓" if produit.est_positionne() else "○"
                position = f"({produit.position_x},{produit.position_y})" if produit.est_positionne() else ""
                texte = f"{status} {produit.nom} ({produit.categorie}) {position}"
                self.liste_produits_magasin.addItem(texte)
                
                if produit.est_positionne():
                    self.vue_plan.afficher_produit(produit.nom, produit.position_x, produit.position_y)
        else:
            self.label_nom.setText("-")
            self.label_auteur.setText("-")
            self.label_date.setText("-")
            self.label_magasin.setText("-")
            self.liste_produits_magasin.clear()
            self.vue_plan.scene.clear()