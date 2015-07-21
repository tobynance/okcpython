import subprocess
import server

#######################################################################
class Player(object):
    def __init__(self, name, popen_args, cwd):
        self.name = name
        self.popen_args = popen_args
        self.cwd = cwd

    ###################################################################
    def getClientProxy(self, other):
        s = subprocess.Popen(self.popen_args + [self.name, other.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.cwd)
        return server.ClientProxy(self.name, s)

#######################################################################
def getPlayers():
    all_players = {}
    all_players["human"] = Player("Human", ["python", "human_client.py"], "../client/human")
    all_players["basic1"] = Player("Basic1", ["python", "simple_client.py"], "../client/python_sample")
    all_players["basic2"] = Player("Basic2", ["python", "simple_client.py"], "../client/python_sample")

    return all_players
