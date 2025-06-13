from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ProjetModele import ProjetModele
from vueConfigurationMagasin import VueConfigurationMagasin
from vueCheminOptimal import VueCalculChemin

class VuePrincipale(QMainWindow):
    """Fenêtre principale de l'application"""
    
    def __init__(self, modele: ProjetModele):
        super().__init__()
        self.modele = modele
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("SAÉ Graphes-IHM - Gestion de Magasin")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central avec onglets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Onglet 1 : Configuration du magasin
        self.vue_config = VueConfigurationMagasin(self.modele)
        self.tabs.addTab(self.vue_config, "Configuration Magasin")
        
        # Onglet 2 : Calcul de chemin
        self.vue_chemin = VueCalculChemin(self.modele)
        self.tabs.addTab(self.vue_chemin, "Calcul de Chemin")
        
        # Barre de statut
        self.statusBar().showMessage("Prêt - Créez ou ouvrez un projet pour commencer")
        
        # Connexion pour mettre à jour la barre de statut
        self.modele.projet_modifie.connect(self.mettre_a_jour_statut)
        self.tabs.currentChanged.connect(self.tab_change)
        
    def mettre_a_jour_statut(self):
        """Met à jour la barre de statut"""
        if self.modele.projet_courant:
            self.statusBar().showMessage(
                f"Projet actuel : {self.modele.projet_courant.nom} - "
                f"Magasin : {self.modele.projet_courant.nom_magasin}"
            )
        else:
            self.statusBar().showMessage("Aucun projet ouvert")
            
    def tab_change(self,index):
        self.vue_chemin.actualiser_liste_magasins()
            
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    modele = ProjetModele()
    vue_principale = VuePrincipale(modele)
    vue_principale.show()
    
    sys.exit(app.exec())