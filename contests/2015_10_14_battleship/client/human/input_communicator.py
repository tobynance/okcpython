import sys
from PyQt4 import QtCore


#######################################################################
class InputCommunicator(QtCore.QThread):
    end_game = QtCore.pyqtSignal()
    get_ship_locations = QtCore.pyqtSignal()
    get_shots = QtCore.pyqtSignal(int)
    grid_size = QtCore.pyqtSignal(int, int)
    num_ships = QtCore.pyqtSignal(int)
    ship_sizes = QtCore.pyqtSignal(list)
    received_line = QtCore.pyqtSignal(str)
    you_hit = QtCore.pyqtSignal(int, int)
    you_miss = QtCore.pyqtSignal(int, int)
    opponent_hit = QtCore.pyqtSignal(int, int)
    opponent_miss = QtCore.pyqtSignal(int, int)

    ###################################################################
    def __init__(self):
        QtCore.QThread.__init__(self)

    ###################################################################
    def run(self):
        out_file = file("client.log", "w")
        while True:
            line = sys.stdin.readline()
            out_file.write(line)
            line = line.strip()
            self.received_line.emit(line)
            assert(line.endswith("|END|"))
            if line == "|INFO|end game|END|":
                self.end_game.emit()
                return
            elif line == "|QUERY|ship locations|END|":
                self.get_ship_locations.emit()
            elif line.startswith("|QUERY|shots"):
                num_shots = int(line.split("|")[3])
                self.get_shots.emit(num_shots)
            elif line.startswith("|INFO|grid size"):
                grid_size = line.split("|")[3].split()
                grid_width = int(grid_size[0])
                grid_height = int(grid_size[1])
                self.grid_size.emit(grid_width, grid_height)
            elif line.startswith("|INFO|num ships"):
                num_ships = line.split("|")[3]
                num_ships = int(num_ships)
                self.num_ships.emit(num_ships)
            elif line.startswith("|INFO|ship sizes"):
                ship_sizes = [int(x) for x in line.split("|")[3:-2]]
                self.ship_sizes.emit(ship_sizes)
            elif line.startswith("|INFO|you hit|"):
                location = [int(x) for x in line.split("|")[3].split()]
                x, y = location
                self.you_hit.emit(x, y)
            elif line.startswith("|INFO|you miss|"):
                location = [int(x) for x in line.split("|")[3].split()]
                x, y = location
                self.you_miss.emit(x, y)
            elif line.startswith("|INFO|opponent hit|"):
                location = [int(x) for x in line.split("|")[3].split()]
                x, y = location
                self.opponent_hit.emit(x, y)
            elif line.startswith("|INFO|opponent miss|"):
                location = [int(x) for x in line.split("|")[3].split()]
                x, y = location
                self.opponent_miss.emit(x, y)
            elif line.startswith("|INFO|"):
                pass
