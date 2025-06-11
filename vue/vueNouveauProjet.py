from PyQt6.QtWidgets import (
    QLineEdit, QTextEdit,QDialog, QFormLayout, QDialogButtonBox,
)


class DialogueNouveauProjet(QDialog):
    """Dialogue pour créer un nouveau projet"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau projet")
        self.resize(400, 300)
        
        layout : QFormLayout= QFormLayout(self)
        
        self.nom_edit : QLineEdit= QLineEdit()
        self.auteur_edit : QLineEdit= QLineEdit()
        self.nom_magasin_edit : QLineEdit= QLineEdit()
        self.adresse_edit : QTextEdit = QTextEdit()
        self.adresse_edit.setMaximumHeight(80)
        
        layout.addRow("Nom du projet :", self.nom_edit)
        layout.addRow("Auteur :", self.auteur_edit)
        layout.addRow("Nom du magasin :", self.nom_magasin_edit)
        layout.addRow("Adresse :", self.adresse_edit)
        
        buttons : QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_data(self):
        return {
            'nom': self.nom_edit.text().strip(),
            'auteur': self.auteur_edit.text().strip(),
            'nom_magasin': self.nom_magasin_edit.text().strip(),
            'adresse': self.adresse_edit.toPlainText().strip()
        }