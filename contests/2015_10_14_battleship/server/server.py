import logging
import timeout

########################################################################
class ClientErrorException(Exception): pass

########################################################################
class NullStream(object):
    ####################################################################
    def write(*args):
        pass

    ####################################################################
    def flush(*args):
        pass

########################################################################
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s: %(message)s',
                    stream=NullStream())
fileHandler = logging.FileHandler(filename="game.log", mode='w')
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s: %(message)s')
fileHandler.setFormatter(formatter)
logging.getLogger('').addHandler(fileHandler)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s: %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


########################################################################
class SimpleObserver(object):
    ####################################################################
    def __init__(self):
        self.out_file = file("observer.log", "w")

    ####################################################################
    def send(self, line):
        self.out_file.write(line)
        self.out_file.write("\n")

    ####################################################################
    def send_ship_locations(self, player_name, ship_locations):
        s = "|ship locations|%s|" % player_name
        s += "|".join((" ".join(ship) for ship in ship_locations))
        s += "|END|"
        self.send(s)

    ####################################################################
    def send_shots(self, player_name, player_shots):
        s = "|shots|%s|" % player_name
        s += "|".join((" ".join(shot) for shot in player_shots))
        s += "|END|"
        self.send(s)

    ####################################################################
    def set_players(self, player1_name, player2_name):
        s = "|players|%s|%s|END|" % (player1_name, player2_name)
        self.send(s)


#########################################################################
class BattleshipServer(object):
    def __init__(self, width, height, ship_sizes, player1, player2):
        self.width = width
        self.height = height
        self.player1 = player1
        self.player2 = player2
        self.players = [self.player1, self.player2]
        self.ship_sizes = ship_sizes
        self.observer = SimpleObserver()
        self.observer.set_players(player1.name, player2.name)
        logging.info("*" * 80)
        logging.info("board size:%d x %d" % (self.width, self.height))
        logging.info("ship sizes: %s" % (str(self.ship_sizes)))

    ####################################################################
    def run(self):
        self.send_all_clients("|INFO|grid size|%d %d|END|" % (self.width, self.height))
        self.observer.send("|grid size|%d %d|END|" % (self.width, self.height))
        self.send_all_clients("|INFO|num ships|%d|END|" % len(self.ship_sizes))
        self.observer.send("|num ships|%d|END|" % len(self.ship_sizes))
        str_ship_sizes = "|".join([str(x) for x in self.ship_sizes])
        self.send_all_clients("|INFO|ship sizes|%s|END|" % str_ship_sizes)
        self.observer.send("|ship sizes|%s|END|" % str_ship_sizes)

        ### get ship placement
        try:
            self.get_ships(self.player1)
        except ClientErrorException, e:
            self.end_game()
            return self.player2.name
        try:
            self.get_ships(self.player2)
        except ClientErrorException, e:
            self.end_game()
            return self.player1.name

        ### start game loop
        while True:
            try:
                player_1_shots = self.get_player_shots(self.player1)
            except ClientErrorException, e:
                self.end_game()
                return self.player2.name
            try:
                player_2_shots = self.get_player_shots(self.player2)
            except ClientErrorException, e:
                self.end_game()
                return self.player1.name

            ### make shots
            try:
                self.play_shots(self.player1, self.player2, player_1_shots)
            except ClientErrorException, e:
                self.end_game()
                return self.player2.name
            try:
                self.play_shots(self.player2, self.player1, player_2_shots)
            except ClientErrorException, e:
                self.end_game()
                return self.player1.name

            ### check player status
            player_1_alive = self.check_player_alive(self.player1)
            player_2_alive = self.check_player_alive(self.player2)

            if player_1_alive and player_2_alive:
                continue
            elif player_1_alive and not player_2_alive:
                self.player1.send("|INFO|won game|END|")
                self.player2.send("|INFO|lost game|END|")
                self.observer.send("|end game|%s won|END|" % self.player1.name)
                logging.info("%s won the game" % self.player1.name)
                self.end_game()
                return self.player1.name
            elif player_2_alive and not player_1_alive:
                self.player2.send("|INFO|won game|END|")
                self.player1.send("|INFO|lost game|END|")
                logging.info("%s won the game" % self.player2.name)
                self.observer.send("|end game|%s won|END|" % self.player2.name)
                self.end_game()
                return self.player2.name
            elif player_1_alive == False and player_2_alive == False:
                self.send_all_clients("|INFO|tie game|END|")
                logging.info("The game was tied")
                self.observer.send("|end game|tie game|END|")
                self.end_game()
                return

    ####################################################################
    def get_player_info(self, player, tag):
        line = player.receive()
        logging.info("%s: %s", player.name, line)

        if not (line.startswith("|RESPONSE|" + tag + "|") and line.endswith("|END|")):
            logging.error("bad line from client: (%s)", line)
            try:
                self.end_game()
            except:
                pass
            raise ClientErrorException("bad line from client: (%s)" % line)
        return self.parse_line_into_value_sets(line)

    ####################################################################
    def parse_line_into_value_sets(self, line):
        out_values = []
        items = line.split("|")[3:-2]
        for item in items:
            out_values.append(item.split())
        return out_values

    ####################################################################
    def get_ships(self, player):
        player.send("|QUERY|ship locations|END|")
        ship_locations = self.get_player_info(player, "ship locations")
        if len(ship_locations) != len(self.ship_sizes):
            logging.error("incorrect number of ships from client %s: Expected %d but got %d (%s)", player.name, len(self.ship_sizes), len(ship_locations), ship_locations)
            self.end_game()
            raise ClientErrorException("incorrect number of ships from client %s: (%s)" % (player.name, str(ship_locations)))

        self.observer.send_ship_locations(player.name, ship_locations)
        ships = []
        used_locations = set()
        for index, (x, y, orientation) in enumerate(ship_locations):
            x = int(x)
            y = int(y)
            if orientation == "H":
                horizontal = True
            elif orientation == "V":
                horizontal = False
            ### expand each ship into an array
            size = self.ship_sizes[index]
            ship = {}
            for size_index in range(size):
                ship[x, y] = True
                if (x, y) in used_locations:
                    ### already used spot
                    logging.error("overlapping ships from client %s: (%s)", player.name, ship_locations)
                    self.end_game()
                    raise ClientErrorException("overlapping ships from client %s: (%s)" % (player.name, str(ship_locations)))
                if not (0 <= x < self.width) or not (0 <= y < self.height):
                    logging.error("ship out-of-bounds from client %s: (%s)", player.name, ship_locations)
                    self.end_game()
                    raise ClientErrorException("ship out-of-bounds from client %s: (%s)" % (player.name, str(ship_locations)))
                    
                used_locations.add((x, y))
                if horizontal:
                    x += 1
                else:
                    y += 1
            ships.append(ship)
        player.ships = ships

    ####################################################################
    def get_player_shots(self, player):
        num_shots_allowed = self.get_num_surviving_ships(player)
        player.send("|QUERY|shots|%d|END|" % num_shots_allowed)
        player_shots = self.get_player_info(player, "shots")
        self.observer.send_shots(player.name, player_shots)
        if len(player_shots) > num_shots_allowed:
            logging.error("bad number of shots from client: Expected %d but got %d (%s)", num_shots_allowed, len(player_shots), player_shots)
            self.end_game()
            raise ClientErrorException("bad number of shots from client: (%s)" % str(player_shots))
        try:
            player_shots = [(int(x), int(y)) for (x, y) in player_shots]
        except:
            logging.error("bad line from client: (%s)", player_shots)
            self.end_game()
            raise ClientErrorException("bad line from client: (%s)" % str(player_shots))
        return player_shots

    ####################################################################
    def play_shots(self, shooting_player, shot_at_player, shots):
        for location in shots:
            hit = False
            for ship in shot_at_player.ships:
                if location in ship:
                    hit = True
                    break
            if hit:
                logging.info("%s shot %s at (%d, %d)" % (shooting_player.name, shot_at_player.name, location[0], location[1]))
                shot_at_player.send("|INFO|opponent hit|%d %d|END|" % location)
                shooting_player.send("|INFO|you hit|%d %d|END|" % location)
                ship[location] = False
            else:
                logging.info("%s misses %s at (%d, %d)" % (shooting_player.name, shot_at_player.name, location[0], location[1]))
                shot_at_player.send("|INFO|opponent miss|%d %d|END|" % location)
                shooting_player.send("|INFO|you miss|%d %d|END|" % location)

    ####################################################################
    def check_player_alive(self, player):
        for ship in player.ships:
            if any(ship.values()):
                return True
        return False

    ####################################################################
    def get_num_surviving_ships(self, player):
        count = 0
        for ship in player.ships:
            if any(ship.values()):
                count += 1
        return count

    ####################################################################
    def send_all_clients(self, line):
        logging.info(line)
        for c in self.players:
            c.send(line)

    ####################################################################
    def end_game(self):
        try:
            self.send_all_clients("|INFO|end game|END|")
        except:
            pass
        logging.shutdown()

########################################################################
########################################################################
class ClientProxy(object):
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.ships = []

    ####################################################################
    def send(self, line):
        line = line.strip() + "\n"
        logging.info("From Server to %s: %s" % (self.name, line.strip()))
        try:
            self.client.stdin.write(line)
            self.client.stdin.flush()
        except Exception, e:
            logging.error("error with sending to client (%s): %s" % (self.name, str(e)))
            raise ClientErrorException("Exception sending to (%s)" % self.name)

    ####################################################################
    def receive(self):
        return self.client.stdout.readline().strip()
        # stdout_read = timeout.TimeoutFunction(self.client.stdout.readline, 10)
        # try:
        #     return stdout_read().strip()
        # except timeout.TimeoutFunctionException:
        #     logging.error("Client taking too long to respond (%s)" % self.name)
        #     raise ClientErrorException("Client taking too long to respond (%s)" % self.name)
