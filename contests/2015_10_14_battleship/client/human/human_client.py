import sys, os
from PyQt4 import QtGui, QtCore
from grid import GridWidget
from input_communicator import InputCommunicator
from ship import Ship
from utils import Vector2
import logging

#######################################################################
### setup the basic logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)-8s: %(message)s',
                    filename='human_client.log',
                    filemode='w')

WAITING_FOR_SHIPS = 0
WAITING_FOR_SHOTS = 1


#######################################################################
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None)
        logging.debug("MainWindow constructor: starting communicator")
        self.communicator = InputCommunicator()
        self.communicator.end_game.connect(self.endGame)
        self.communicator.get_ship_locations.connect(self.getShipLocations)
        self.communicator.get_shots.connect(self.getShots)
        self.communicator.grid_size.connect(self.setGridSize)
        self.communicator.num_ships.connect(self.setNumShips)
        self.communicator.ship_sizes.connect(self.setShipSizes)
        self.communicator.received_line.connect(self.addMessage)
        self.communicator.you_hit.connect(self.youHit)
        self.communicator.you_miss.connect(self.youMiss)
        self.communicator.opponent_hit.connect(self.opponentHit)
        self.communicator.opponent_miss.connect(self.opponentMiss)

        self.communicator.start()
        self.width = 0
        self.height = 0
        self.num_ships = 0
        self.ship_sizes = []
        self.client = None
        logging.debug("end of MainWindow constructor")

    ###################################################################
    def youHit(self, x, y):
        logging.debug("MainWindow: youHit (%d, %d)", x, y)
        self.client.youHit(x, y)

    ###################################################################
    def youMiss(self, x, y):
        logging.debug("MainWindow: youMiss (%d, %d)", x, y)
        self.client.youMiss(x, y)

    ###################################################################
    def opponentHit(self, x, y):
        logging.debug("MainWindow: opponentHit (%d, %d)", x, y)
        self.client.opponentHit(x, y)

    ###################################################################
    def opponentMiss(self, x, y):
        logging.debug("MainWindow: opponentMiss (%d, %d)", x, y)
        self.client.opponentMiss(x, y)

    ###################################################################
    def endGame(self):
        logging.debug("MainWindow: endGame")
        global app
        app.exit()

    ###################################################################
    def getShipLocations(self):
        ### get the visuals to show
        logging.debug("MainWindow: getShipLocations")
        self.client = HumanClient(self.width, self.height, self.num_ships, self.ship_sizes)
        self.setCentralWidget(self.client)
        self.client.show()        
        ### now ask the client to place some ships

    ###################################################################
    def getShots(self, num_shots):
        logging.debug("MainWindow: getShots: (%d)", num_shots)
        self.client.num_shots_allowed = num_shots
        if num_shots == 1:
            self.addMessage("Place 1 shot on the grid to the left")
        else:
            self.addMessage("Place %d shots on the grid to the left" % num_shots)

    ###################################################################
    def addMessage(self, line):
        logging.debug("MainWindow: addMessage: (%s)", line)
        if self.client:
            self.client.addMessage(line)
        pass

    ###################################################################
    def setGridSize(self, x, y):
        logging.debug("MainWindow: setGridSize (%d, %d)", x, y)
        self.width = x
        self.height = y

    ###################################################################
    def setNumShips(self, num_ships):
        logging.debug("MainWindow: setNumShips: (%d)", num_ships)
        self.num_ships = num_ships
    
    ###################################################################
    def setShipSizes(self, ship_sizes):
        logging.debug("MainWindow: setShipSizes: (%s)", str(ship_sizes))
        self.ship_sizes = ship_sizes

#######################################################################
class HumanClient(QtGui.QWidget):
    def __init__(self, width, height, num_ships, ship_sizes):
        QtGui.QWidget.__init__(self, None)
        logging.debug("HumanClient: constructor")
        self.num_ships = num_ships
        self.grid_width = width
        self.grid_height = height
        self.ship_sizes = ship_sizes
        self.pixmaps = {}
        for item in ["bottom", "empty", "hit", "miss", "left", "middle", "right", "small", "top", "crosshair"]:
            self.pixmaps[item] = QtGui.QPixmap(os.path.join(".", "images", item + ".png"))

        vlayout = QtGui.QVBoxLayout()
        layout = QtGui.QHBoxLayout()
        self.opponent_grid = GridWidget(self, self.pixmaps, width, height)
        self.my_grid = GridWidget(self, self.pixmaps, width, height)

        self.opponent_grid.start_drag.connect(self.opponentStartDrag)
        self.my_grid.start_drag.connect(self.myStartDrag)

        self.opponent_grid.ship_dropped.connect(self.opponentDropShip)
        self.my_grid.ship_dropped.connect(self.myDropShip)

        self.opponent_grid.rotate_ship.connect(self.opponentRotateShip)
        self.my_grid.rotate_ship.connect(self.myRotateShip)

        spacer = QtGui.QFrame(self)
        spacer.setFrameStyle(QtGui.QFrame.VLine | QtGui.QFrame.Sunken)
        layout.addWidget(self.opponent_grid)
        layout.addWidget(spacer)
        layout.addWidget(self.my_grid)
        self.setLayout(vlayout)
        messages_and_button = QtGui.QHBoxLayout()
        self.messages = QtGui.QListWidget(self)
        messages_and_button.addWidget(self.messages)
        vlayout.addLayout(layout)
        vlayout.addLayout(messages_and_button)
        self.submit_button = QtGui.QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit)

        buttons_layout = QtGui.QVBoxLayout()
        buttons_layout.addWidget(self.submit_button)
        messages_and_button.addLayout(buttons_layout)

        self.addMessage("Num Ships: %d" % self.num_ships)
        self.addMessage("Ship Sizes: %s" % str(self.ship_sizes))
        self.addMessage("Place your ships on the grid on the right")
        self.dragItem = None

        ships = []
        y = 0
        for size in self.ship_sizes:
            ships.append(Ship(Vector2(0, y), Vector2(size-1, y)))
            y += 1
        for ship in ships:
            self.addShipToGrid(ship)

        self.ships = ships
        self.state = WAITING_FOR_SHIPS
        self.shots = []
        self.num_shots_allowed = 0
        logging.debug("HumanClient: end of constructor")

    ###################################################################
    def submit(self):
        logging.debug("HumanClient: submit")
        if self.state == WAITING_FOR_SHIPS:
            self.submitShips()

            self.opponent_grid.start_drag.disconnect(self.opponentStartDrag)
            self.my_grid.start_drag.disconnect(self.myStartDrag)
    
            self.opponent_grid.ship_dropped.disconnect(self.opponentDropShip)
            self.my_grid.ship_dropped.disconnect(self.myDropShip)
    
            self.opponent_grid.rotate_ship.disconnect(self.opponentRotateShip)
            self.my_grid.rotate_ship.disconnect(self.myRotateShip)
            
            self.opponent_grid.clicked.connect(self.addShot)
            self.state = WAITING_FOR_SHOTS
        elif self.state == WAITING_FOR_SHOTS:
            self.submitShots()

    ###################################################################
    def submitShots(self):
        logging.debug("HumanClient: submitShots")
        self.addMessage("submit shots")
        out_str = "|RESPONSE|shots|"
        for shot in self.shots:
            out_str += "%d %d|" % (shot.x, shot.y)
        out_str += "END|"
        self.addMessage(out_str)
        self.send(out_str)
        self.shots = []

    ###################################################################
    def youHit(self, x, y):
        logging.debug("HumanClient: youHit (%d, %d)", x, y)
        self.opponent_grid[x, y].setPixmap(self.pixmaps["hit"])

    ###################################################################
    def youMiss(self, x, y):
        logging.debug("HumanClient: youMiss (%d, %d)", x, y)
        self.opponent_grid[x, y].setPixmap(self.pixmaps["miss"])

    ###################################################################
    def opponentHit(self, x, y):
        logging.debug("HumanClient: opponentHit (%d, %d)", x, y)
        self.my_grid[x, y].setPixmap(self.pixmaps["hit"])

    ###################################################################
    def opponentMiss(self, x, y):
        logging.debug("HumanClient: opponentMiss (%d, %d)", x, y)
        self.my_grid[x, y].setPixmap(self.pixmaps["miss"])

    ###################################################################
    def addShot(self, x, y):
        logging.debug("HumanClient: addShot (%d, %d)", x, y)
        self.addMessage("addShot: (%d, %d)" % (x, y))
        p = Vector2(x, y)
        if p in self.shots:
            self.shots.remove(p)
            self.opponent_grid[x, y].setPixmap(self.pixmaps["empty"])
            return
        if len(self.shots) < self.num_shots_allowed:
            self.shots.append(p)            
            self.opponent_grid[x, y].setPixmap(self.pixmaps["crosshair"])
        
    ###################################################################
    def submitShips(self):
        logging.debug("HumanClient: submitShips")
        ### I need my ships to be sorted in the same order as self.ship_sizes
        ships = self.ships[:]
        new_ships = []
        for size in self.ship_sizes:
            for i in range(len(ships)):
                if ships[i].my_grid and ships[i].size == size:
                    new_ships.append(ships.pop(i))
                    break
        
        ### so new_ships should be all of them in the right order
        out_str = "|RESPONSE|ship locations|"
        for ship in new_ships:
            x = ship.points[0].x
            y = ship.points[0].y
            if ship.horizontal:
                direction = "H"
            else:
                direction = "V"
            out_str += "%d %d %s|" % (x, y, direction)
        out_str += "END|"
        self.send(out_str)

    ###################################################################
    def send(self, output):
        logging.debug("HumanClient: send (%s)", output)
        output = output.strip() + "\n"
        #print output
        sys.stdout.write(output)
        sys.stdout.flush()

    ###################################################################
    def opponentDropShip(self, ship):
        logging.debug("HumanClient: opponentDropShip (%s)", str(ship))
        ship.my_grid = False
        self.ships.append(ship)
        self.redrawShips()

    ###################################################################
    def myDropShip(self, ship):
        logging.debug("HumanClient: myDropShip (%s)", str(ship))
        ship.my_grid = True
        self.ships.append(ship)
        self.redrawShips()

    ###################################################################
    def setState(self, state):
        logging.debug("HumanClient: setState (%s)", str(state))
        self.addMessage("State Change: %d" % state)
        self.state = state

    ###################################################################
    def addMessage(self, line):
        logging.debug("HumanClient: addMessage (%s)", line)
        QtGui.QListWidgetItem(line, self.messages)
        ### highlight the line just added
        self.messages.setCurrentRow(self.messages.count() - 1)

    ###################################################################
    def addShipToGrid(self, ship):
        logging.debug("HumanClient: addShipToGrid (%s)", str(ship))
        if ship.my_grid:
            grid = self.my_grid
        else:
            grid = self.opponent_grid

        if ship.size == 1:
            x, y = ship.points[0].x, ship.points[0].y
            grid[x, y].setPixmap(self.pixmaps["small"])
            return
        if ship.horizontal:
            right = ship.right.x
            x, y = ship.left.x, ship.left.y
            grid[x, y].setPixmap(self.pixmaps["left"])
            x += 1
            while x < right:
                grid[x, y].setPixmap(self.pixmaps["middle"])
                x += 1
            grid[x, y].setPixmap(self.pixmaps["right"])
        else:
            bottom = ship.bottom.y
            x, y = ship.top.x, ship.top.y
            grid[x, y].setPixmap(self.pixmaps["top"])
            y += 1
            while y < bottom:
                grid[x, y].setPixmap(self.pixmaps["middle"])
                y += 1
            grid[x, y].setPixmap(self.pixmaps["bottom"])

    ###################################################################
    def opponentRotateShip(self, x, y):
        logging.debug("HumanClient: opponentRotateShip (%d, %d)", x, y)
        self.addMessage("opponent rotate ship: (%d, %d)" % (x, y))
        for ship in self.ships:
            if ship.my_grid == False:
                if ship.point_in_ship(x, y):
                    self.rotateShip(ship)
                    return

    ###################################################################
    def myRotateShip(self, x, y):
        logging.debug("HumanClient: myRotateShip (%d, %d)", x, y)
        self.addMessage("my rotate ship: (%d, %d)" % (x, y))
        for ship in self.ships:
            if ship.my_grid == True:
                if ship.point_in_ship(x, y):
                    self.rotateShip(ship)
                    return

    ###################################################################
    def opponentStartDrag(self, x, y):
        logging.debug("HumanClient: opponentStartDrag (%d, %d)", x, y)
        self.addMessage("opponent start drag: (%d, %d)" % (x, y))
        for ship in self.ships:
            if ship.my_grid == False:
                if ship.point_in_ship(x, y):
                    self.startDragging(ship)
                    return

    ###################################################################
    def myStartDrag(self, x, y):
        logging.debug("HumanClient: myStartDrag (%d, %d)", x, y)
        self.addMessage("my start drag: (%d, %d)" % (x, y))
        for ship in self.ships:
            if ship.my_grid == True:
                if ship.point_in_ship(x, y):
                    self.startDragging(ship)
                    return

    ###################################################################
    def rotateShip(self, ship):
        logging.debug("HumanClient: rotateShip (%s)", str(ship))
        ship.rotate()
        self.redrawShips()

    ###################################################################
    def startDragging(self, ship):
        logging.debug("HumanClient: startDragging (%s)", str(ship))
        self.dragItem = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setData("ship", str(ship))
        self.dragItem.setMimeData(mimeData)
        self.dragItem.setPixmap(self.getPixmapForShip(ship))
        dropAction = self.dragItem.exec_()

        if dropAction == QtCore.Qt.MoveAction:
            self.ships.remove(ship)
            self.redrawShips()

    ###################################################################
    def getPixmapForShip(self, ship):
        logging.debug("HumanClient: getPixmapForShip (%s)", str(ship))
        width = 24
        height = 24
        if ship.horizontal:
            width = 24 * ship.size
        else:
            height = 24 * ship.size
        
        return self.pixmaps["middle"].scaled(width, height)

    ###################################################################
    def opponentClicked(self, x, y):
        logging.debug("HumanClient: opponentClicked (%d, %d)", x, y)
        self.addMessage("opponent grid clicked: (%d, %d)" % (x, y))

    ###################################################################
    def placeShips(self):
        logging.debug("HumanClient: placeShips")
        for ship in self.ships:
            self.addShipToGrid(ship)

    ###################################################################
    def clear(self):
        "Clear the board to empty pics"
        logging.debug("HumanClient: clear")
        for grid in [self.my_grid, self.opponent_grid]:
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    grid[x, y].setPixmap(self.pixmaps["empty"])

    ###################################################################
    def redrawShips(self):
        logging.debug("HumanClient: redrawShips")
        self.clear()
        self.placeShips()

#######################################################################
if __name__ == "__main__":
    logging.debug("start")
    app = QtGui.QApplication(sys.argv)
    #widget = HumanClient(20, 20, 3, [1, 2, 3])
    widget = MainWindow()
    widget.show()
    logging.debug("MinWindows created and shown")
    sys.exit(app.exec_())
