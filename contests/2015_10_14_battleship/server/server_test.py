import unittest
from server import BattleshipServer, ClientProxy, ClientErrorException


########################################################################
class NullStream(object):
    ####################################################################
    def readline(self):
        pass

    ####################################################################
    def write(self, *args):
        pass

    ####################################################################
    def flush(self, *args):
        pass

########################################################################
class MockClient(object):
    ####################################################################
    def __init__(self):
        self.stdin = NullStream()
        self.stdout = NullStream()


########################################################################
class ServerTests(unittest.TestCase):
    ####################################################################
    def setUp(self):
        self.player1 = ClientProxy("p1", MockClient())
        self.player2 = ClientProxy("p2", MockClient())
        self.server = BattleshipServer(5, 5, [1, 1], self.player1, self.player2)

    ####################################################################
    def test_parse_line_into_value_sets(self):
        values = self.server.parse_line_into_value_sets("|RESPONSE|ship_locations|0 0 H|0 1 H|0 2 H|END|")
        self.assertEqual(values, [["0", "0", "H"], ["0", "1", "H"], ["0", "2", "H"]])

        values = self.server.parse_line_into_value_sets("|RESPONSE|shots|3 2|4 1|4 2|END|")
        self.assertEqual(values, [["3", "2"], ["4", "1"], ["4", "2"]])

    ####################################################################
    def test_overlapping_ships(self):
        self.server.get_player_info = lambda x, y: [["0", "0", "H"], ["0", "0", "H"]]
        try:
            self.server.get_ships(self.player1)
            self.fail("Overlapping ships should result in error")
        except ClientErrorException, e:
            pass
    
    ####################################################################
    def test_ships_out_of_bounds(self):
        self.server.get_player_info = lambda x, y: [["10", "0", "H"], ["0", "0", "H"]]
        try:
            self.server.get_ships(self.player1)
            self.fail("Out-of-bounds ships should result in error")
        except ClientErrorException, e:
            pass

    ####################################################################
    def test_client_gave_garbage_for_ship_placement(self):
        self.player1.client.stdout.readline = lambda : "asdfw\n"
        try:
            self.server.get_ships(self.player1)
            self.fail("Garbage for ships should result in error")
        except ClientErrorException, e:
            pass
    
    ####################################################################
    def test_client_gave_garbage_for_shots(self):
        self.player1.client.stdout.readline = lambda : "asdfw\n"
        try:
            self.server.get_player_shots(self.player1)
            self.fail("Garbage for shots should result in error")
        except ClientErrorException, e:
            pass

    ####################################################################
    def test_client_submitted_too_many_ships(self):
        self.server.get_player_info = lambda x, y: [["0", "0", "H"], ["1", "0", "H"], ["2", "0", "H"]]
        try:
            self.server.get_ships(self.player1)
            self.fail("Overlapping ships should result in error")
        except ClientErrorException, e:
            pass

    ####################################################################
    def test_client_submitted_too_few_ships(self):
        self.server.get_player_info = lambda x, y: [["0", "0", "H"]]
        try:
            self.server.get_ships(self.player1)
            self.fail("Overlapping ships should result in error")
        except ClientErrorException, e:
            pass

    ####################################################################
    def test_client_submitted_too_many_shots(self):
        self.server.get_num_surviving_ships = lambda x: 1
        self.server.get_player_info = lambda x, y: [["0", "0"], ["0", "1"], ["0", "2"], ["0", "3"], ["0", "4"], ["0", "5"]]
        try:
            self.server.get_player_shots(self.player1)
            self.fail("Too many shots should result in error")
        except ClientErrorException, e:
            pass

    ####################################################################
    def test_client_submitted_too_few_shots(self):
        self.server.get_num_surviving_ships = lambda x: 2
        self.server.get_player_info = lambda x, y: [["0", "0"]]
        try:
            self.server.get_player_shots(self.player1)
            self.fail("Too few shots should result in error")
        except ClientErrorException, e:
            pass
