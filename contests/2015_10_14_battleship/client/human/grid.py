from PyQt4 import QtGui, QtCore
from ship import Ship


#######################################################################
class GridLabel(QtGui.QLabel):
    start_drag = QtCore.pyqtSignal(int, int)
    click = QtCore.pyqtSignal(int, int)
    rotate_ship = QtCore.pyqtSignal(int, int)
    
    ###################################################################
    def __init__(self, parent, pixmap, x, y):
        QtGui.QLabel.__init__(self, parent)
        self.setPixmap(pixmap)
        self.x = x
        self.y = y
        self.setAcceptDrops(True)

    ###################################################################
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.start_drag.emit(self.x, self.y)

    ###################################################################
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.click.emit(self.x, self.y)
        if event.button() == QtCore.Qt.RightButton:
            self.rotate_ship.emit(self.x, self.y)

    ###################################################################
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("ship"):
            event.acceptProposedAction()

    ###################################################################
    def dropEvent(self, event):
        ship = event.mimeData().data("ship")
        accept = self.parent().dropAttempt(ship, self.x, self.y)
        if accept:
            event.setDropAction(QtCore.Qt.MoveAction)
            event.acceptProposedAction()
        else:
            event.setDropAction(QtCore.Qt.IgnoreAction)
            event.acceptProposedAction()

#######################################################################
class GridWidget(QtGui.QWidget):
    start_drag = QtCore.pyqtSignal(int, int)
    clicked = QtCore.pyqtSignal(int, int)
    rotate_ship = QtCore.pyqtSignal(int, int)
    ship_dropped = QtCore.pyqtSignal(Ship)

    ###################################################################
    def __init__(self, parent, pixmaps, width, height):
        QtGui.QWidget.__init__(self, parent)
        self.pixmaps = pixmaps
        self.grid = {}
        layout = QtGui.QGridLayout(self)
        layout.setSpacing(2)
        self.setLayout(layout)
        for i in range(width):
            for j in range(height):
                label = GridLabel(self, self.pixmaps["empty"], i, j)
                label.click.connect(self.clickedItem)
                label.start_drag.connect(self.startDrag)
                label.rotate_ship.connect(self.rotateShip)
                layout.addWidget(label, j, i)
                self.grid[i, j] = label

    ###################################################################
    def __getitem__(self, key):
        return self.grid[key]

    ###################################################################
    def __setitem__(self, key, value):
        self.grid[key] = value

    ###################################################################
    def clickedItem(self, x, y):
        self.clicked.emit(x, y)

    ###################################################################
    def startDrag(self, x, y):
        self.start_drag.emit(x, y)

    ###################################################################
    def rotateShip(self, x, y):
        self.rotate_ship.emit(x, y)

    ###################################################################
    def dropAttempt(self, ship, x, y):
        ### TODO: make sure that there is room for a ship here
        ship = Ship.from_string(ship)
        ship.move_to(x, y)
        if ship:
            self.ship_dropped.emit(ship)
            return True
        else:
            return False