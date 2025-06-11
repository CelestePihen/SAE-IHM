import sys

from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem,
    QGraphicsLineItem
)
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPointF
from PyQt6.QtGui import QPixmap, QPen, QBrush, QColor, QMouseEvent
import heapq

class VuePlanMagasin(QGraphicsView):
    """Vue pour afficher et manipuler le plan du magasin"""
    
    produit_positionne: pyqtSignal = pyqtSignal(str, int, int)
    
    def __init__(self):
        super().__init__()
        self.scene: QGraphicsScene = QGraphicsScene()
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        self.plan_item: QGraphicsPixmapItem = None
        self.quadrillage_items: list[QGraphicsLineItem] = []
        self.produit_items: dict = {}
        self.produit_en_cours: str = None
        
        self.taille_case: int = 30
        self.nb_cases_x: int = 0
        self.nb_cases_y: int = 0
    
    def charger_plan(self, chemin_image: str):
        """Charge et affiche le plan du magasin"""
        self.scene.clear()
        self.quadrillage_items.clear()
        self.produit_items.clear()
        
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
    
    def mousePressEvent(self, event: QMouseEvent):
        """Gère le clic pour positionner un produit"""
        if self.produit_en_cours and event.button() == Qt.MouseButton.LeftButton:
            scene_pos: QPointF = self.mapToScene(event.pos())
            
            # convertir en coordonnées de grille
            grid_x: int = int(scene_pos.x() // self.taille_case)
            grid_y: int = int(scene_pos.y() // self.taille_case)
            
            if 0 <= grid_x < self.nb_cases_x and 0 <= grid_y < self.nb_cases_y:
                self.produit_positionne.emit(self.produit_en_cours, grid_x, grid_y)
                self.produit_en_cours = None
        
        super().mousePressEvent(event)
    
    def afficher_produit(self, nom: str, x: int, y: int):
        """Affiche un produit positionné sur le plan"""
        # Supprimer l'ancienne position si elle existe
        if nom in self.produit_items:
            self.scene.removeItem(self.produit_items[nom])
        
        # Créer le nouvel item
        rect = QGraphicsRectItem(x * self.taille_case + 2, y * self.taille_case + 2,
                               self.taille_case - 4, self.taille_case - 4)
        rect.setBrush(QBrush(QColor(255, 0, 0, 150)))
        rect.setPen(QPen(QColor(255, 0, 0)))
        rect.setToolTip(nom)
        
        self.scene.addItem(rect)
        self.produit_items[nom] = rect
    
    def afficher_chemin(self, chemin: list[tuple[int, int]]):
        """Affiche le chemin optimal sur le plan"""
        if len(chemin) < 2:
            return
        
        pen = QPen(QColor(0, 255, 0), 3)
        for i in range(len(chemin) - 1):
            x1, y1 = chemin[i]
            x2, y2 = chemin[i + 1]
            
            # Centre des cases
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