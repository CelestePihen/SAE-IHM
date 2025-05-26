import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QPushButton, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QPen, QBrush, QPixmap
from PyQt6.QtCore import Qt, QRectF

CELL_SIZE = 50
GRID_WIDTH = 62
GRID_HEIGHT = 45

# Classe représentant une cellule du quadrillage
class GridCell(QGraphicsRectItem):
    def __init__(self, x, y, state=0):
        super().__init__(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.grid_x = x
        self.grid_y = y
        self.state = state
        self.setBrush(QBrush(Qt.GlobalColor.transparent))
        self.setPen(QPen(Qt.GlobalColor.gray))

    # Gestion du clic de souris pour changer l'état de la case
    def mousePressEvent(self, event):
        self.toggle_state()

    # Passage de la case en noir ou blanc
    def toggle_state(self):
        self.state = 1 if self.state == 0 else 0
        color = Qt.GlobalColor.black if self.state == 1 else Qt.GlobalColor.transparent
        self.setBrush(QBrush(color))

# Fenêtre principale de l'éditeur de quadrillage
class GridEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadrillage Magasin")

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints())

        self.plan = QPixmap("plan.jpg")
        self.scene.addPixmap(self.plan)

        self.grid_cells = []

        # Création de la grille de cellules
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                cell = GridCell(x, y)
                self.scene.addItem(cell)
                row.append(cell)
            self.grid_cells.append(row)

        self.save_button = QPushButton("Sauvegarder la grille")
        self.save_button.clicked.connect(self.save_grid)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    # Méthode pour sauvegarder l'état de la grille dans un fichier JSON
    def save_grid(self):
        data = [[cell.state for cell in row] for row in self.grid_cells]
        with open("grille_magasin.json", "w") as f:
            json.dump(data, f)
        print("Grille sauvegardée dans grille_magasin.json")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = GridEditor()
    editor.show()
    sys.exit(app.exec())
