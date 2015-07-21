import sys


#######################################################################
class SimpleClient(object):
    def __init__(self):
        self.name = "SimpleClient"
        self.num_ships = 0
        self.grid_width = 0
        self.grid_height = 0
        self.ship_sizes = None

        ### location of next shot to make
        self.shooting_x = 0
        self.shooting_y = 0

    ###################################################################
    def run(self):
        while True:
            line = sys.stdin.readline()
            line = line.strip()
            #sys.stderr.write("$$$" + line + "\n")
            assert(line.endswith("|END|"))
            if line == "|INFO|end game|END|":
                #sys.stderr.write("$$$LEAVING")
                return
            elif line == "|QUERY|ship locations|END|":
                self.get_ship_locations()
            elif line.startswith("|QUERY|shots"):
                num_shots = int(line.split("|")[3])
                self.get_shots(num_shots)
            elif line.startswith("|INFO|grid size"):
                grid_size = line.split("|")[3].split()
                self.grid_width = int(grid_size[0])
                self.grid_height = int(grid_size[1])
            elif line.startswith("|INFO|num ships"):
                num_ships = line.split("|")[3]
                self.num_ships = int(num_ships)
            elif line.startswith("|INFO|ship sizes"):
                self.ship_sizes = [int(x) for x in line.split("|")[3:-2]]
            elif line.startswith("|INFO|"):
                pass
            else:
                sys.stderr.write("%s: Unknown incoming line: %s\n" % (self.name, line))
                return

    ###################################################################
    def get_ship_locations(self):
        locations = []
        for y in range(self.num_ships):
            locations.append("0 %d H" % y)
        str_locations = "|".join(locations)
        self.send("ship locations", str_locations)

    ###################################################################
    def get_shots(self, num_shots):
        shots = []
        for i in range(num_shots):
            shots.append("%d %d" % (self.shooting_x, self.shooting_y))
            self.shooting_x += 1
            if self.shooting_x == self.grid_width:
                self.shooting_x = 0
                self.shooting_y += 1
        str_shots = "|".join(shots)
        self.send("shots", str_shots)

    ###################################################################
    def send(self, tag, data):
        line = "|RESPONSE|%s|%s|END|\n" % (tag, data)
        sys.stdout.write(line)
        sys.stdout.flush()

#######################################################################
if __name__ == "__main__":
    SimpleClient().run()
