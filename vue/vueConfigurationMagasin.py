from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QListWidget,
    QFormLayout, QSplitter, QGroupBox
)

from ProjetModele import ModeleProjet
from PyQt6.QtCore import Qt
from vuePlanMagasin import VuePlanMagasin

class VueConfigurationMagasin(QWidget):
    def __init__(self, modele: ModeleProjet):
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