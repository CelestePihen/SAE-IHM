import sys

from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem,
    QGraphicsLineItem
)
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPointF
from PyQt6.QtGui import QPixmap, QPen, QBrush, QColor, QMouseEvent

class VuePlanMagasin(QGraphicsView):
    """Vue pour afficher et manipuler le plan du magasin"""
    
    produit_positionne: pyqtSignal = pyqtSignal(str, int, int)
    debut_position: pyqtSignal = pyqtSignal(int, int)
    fin_position: pyqtSignal = pyqtSignal(int, int)
    zone_inaccessible_selectionnee: pyqtSignal = pyqtSignal(int, int, bool)
    
    def __init__(self):
        super().__init__()
        self.scene: QGraphicsScene = QGraphicsScene()
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        self.plan_item: QGraphicsPixmapItem = None
        self.quadrillage_items: list[QGraphicsLineItem] = []
        self.produit_items: dict[QGraphicsRectItem] = {}
        self.debut_item: QGraphicsRectItem = None
        self.fin_item: QGraphicsRectItem = None
        self.produit_en_cours: str = None
        
        self.taille_case: int = 30
        self.nb_cases_x: int = 0
        self.nb_cases_y: int = 0
        
        self.debut = False
        self.fin = False
        self.mode_inaccessible = False
        self.zones_inaccessibles_items: dict = {}  # dictionnaire des zones inaccessibles
        
    def definir_mode_inaccessible(self, mode: bool):
        """Définit si on est en mode sélection de zones inaccessibles"""
        self.mode_inaccessible = mode
    
    def charger_plan(self, chemin_image: str):
        """Charge et affiche le plan du magasin"""
        self.scene.clear()
        self.quadrillage_items.clear()
        self.produit_items.clear()
        self.zones_inaccessibles_items.clear()  # Ajouter cette ligne
        self.debut_item = None
        self.fin_item = None
        
        pixmap: QPixmap = QPixmap(chemin_image)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(1920, 1080, 
                                 Qt.AspectRatioMode.KeepAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)
            
            self.plan_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.plan_item)
            self.scene.setSceneRect(QRectF(pixmap.rect()))
    
    def definir_quadrillage(self, nb_x: int, nb_y: int, taille: int):
        """Définit et affiche le quadrillage"""
        self.nb_cases_x = nb_x
        self.nb_cases_y = nb_y
        self.taille_case = taille
        
        # supprime l'ancien quadrillage
        for item in self.quadrillage_items:
            self.scene.removeItem(item)
        self.quadrillage_items.clear()
        
        # crée le nouveau quadrillage
        pen: QPen = QPen(QColor(0, 0, 255, 128))
        for x in range(nb_x + 1):
            line: QGraphicsLineItem = self.scene.addLine(x * taille, 0, x * taille, nb_y * taille, pen)
            self.quadrillage_items.append(line)
        
        for y in range(nb_y + 1):
            line = self.scene.addLine(0, y * taille, nb_x * taille, y * taille, pen)
            self.quadrillage_items.append(line)
    
    def definir_produit_a_positionner(self, nom_produit: str):
        """Définit le produit à positionner au prochain clic"""
        self.produit_en_cours = nom_produit
        
    def definir_debut_position(self, debut: bool):
        """Définit si on doit placer le début"""
        self.debut = debut
        
    def definir_fin_position(self, fin: bool):
        """Définit si on doit placer le début"""
        self.fin = fin
    
    def mousePressEvent(self, event: QMouseEvent):
        """Gère le clic pour positionner un produit ou sélectionner une zone inaccessible"""
        if event.button() == Qt.MouseButton.LeftButton:
            scene_pos: QPointF = self.mapToScene(event.pos())
            
            # convertir en coordonnées de grille
            grid_x: int = int(scene_pos.x() // self.taille_case)
            grid_y: int = int(scene_pos.y() // self.taille_case)
            
            if 0 <= grid_x < self.nb_cases_x and 0 <= grid_y < self.nb_cases_y:
                if self.mode_inaccessible:
                    zone = (grid_x, grid_y)
                    if zone in self.zones_inaccessibles_items:
                        # zone inaccessible, la rendre accessible
                        self.scene.removeItem(self.zones_inaccessibles_items[zone])
                        self.zones_inaccessibles_items.pop(zone)
                        self.zone_inaccessible_selectionnee.emit(grid_x, grid_y, False)
                    else:
                        # zone accessible, la rendre inaccessible
                        self.afficher_zone_inaccessible(grid_x, grid_y)
                        self.zone_inaccessible_selectionnee.emit(grid_x, grid_y, True)
                elif self.produit_en_cours:
                    self.produit_positionne.emit(self.produit_en_cours, grid_x, grid_y)
                    self.produit_en_cours = None
                elif self.debut == True:
                    self.debut_position.emit(grid_x, grid_y)
                    self.debut = False
                elif self.fin == True:
                    self.fin_position.emit(grid_x, grid_y)
                    self.fin = False
        
        super().mousePressEvent(event)
        
    def afficher_zone_inaccessible(self, x: int, y: int):
        """Affiche une zone inaccessible sur le plan"""
        zone = (x, y)
        
        if zone in self.zones_inaccessibles_items:
            return
        
        # créer le rectangle pour la zone inaccessible
        rect = QGraphicsRectItem(x * self.taille_case, y * self.taille_case,
                            self.taille_case, self.taille_case)
        rect.setBrush(QBrush(QColor(128, 128, 128, 180)))
        rect.setPen(QPen(QColor(64, 64, 64), 2)) 
        rect.setToolTip(f"Zone inaccessible ({x}, {y})")
        
        self.scene.addItem(rect)
        self.zones_inaccessibles_items[zone] = rect
    
    def afficher_produit(self, nom: str, x: int, y: int):
        """Affiche un produit positionné sur le plan"""
        # supprimer l'ancienne position si elle existe
        if nom in self.produit_items:
            self.scene.removeItem(self.produit_items[nom])
        
        # créer le nouvel item
        rect = QGraphicsRectItem(x * self.taille_case + 2, y * self.taille_case + 2,
                               self.taille_case - 4, self.taille_case - 4)
        rect.setBrush(QBrush(QColor(255, 0, 0, 150)))
        rect.setPen(QPen(QColor(255, 0, 0)))
        rect.setToolTip(nom)
        
        self.scene.addItem(rect)
        self.produit_items[nom] = rect
        
    def afficher_entree(self, x: int, y: int):
        """Affiche l'entrée sur le plan"""
        # supprimer l'ancienne position si elle existe
        if self.debut_item is not None:
            if self.debut_item.scene() is not None:
                self.scene.removeItem(self.debut_item)
            self.debut_item = None
        
        # créer le nouvel item
        rect = QGraphicsRectItem(x * self.taille_case + 2, y * self.taille_case + 2,
                               self.taille_case - 4, self.taille_case - 4)
        rect.setBrush(QBrush(QColor(0, 0, 255, 150)))
        rect.setPen(QPen(QColor(0, 0, 255)))
        rect.setToolTip("Entrée")
        
        self.scene.addItem(rect)
        self.debut_item = rect
        
    def afficher_sortie(self, x: int, y: int):
        """Affiche la sortie sur le plan"""
        # supprimer l'ancienne position si elle existe
        if self.fin_item is not None:
            if self.fin_item.scene() is not None:
                self.scene.removeItem(self.fin_item)
            self.fin_item = None
        
        # créer le nouvel item
        rect = QGraphicsRectItem(x * self.taille_case + 2, y * self.taille_case + 2,
                               self.taille_case - 4, self.taille_case - 4)
        rect.setBrush(QBrush(QColor(0, 255, 255, 150)))
        rect.setPen(QPen(QColor(0, 255, 255)))
        rect.setToolTip("Sortie")
        
        self.scene.addItem(rect)
        self.fin_item = rect
    
    def afficher_chemin(self, chemin: list[tuple[int, int]]):
        """Affiche le chemin optimal sur le plan"""
        if len(chemin) < 2:
            return
        
        pen = QPen(QColor(0, 255, 0), 3)
        for i in range(len(chemin) - 1):
            x1, y1 = chemin[i]
            x2, y2 = chemin[i + 1]
            
            # centre des cases
            scene_x1 = x1 * self.taille_case + self.taille_case // 2
            scene_y1 = y1 * self.taille_case + self.taille_case // 2
            scene_x2 = x2 * self.taille_case + self.taille_case // 2
            scene_y2 = y2 * self.taille_case + self.taille_case // 2
            
            self.scene.addLine(scene_x1, scene_y1, scene_x2, scene_y2, pen)
            
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    vue = VuePlanMagasin()
    vue.charger_plan("plan.jpg")
    vue.definir_quadrillage(70, 50, 20)
    
    vue.show()
    sys.exit(app.exec())