from server_utils import Player


#######################################################################
def get_players():
    return {"human":  Player("Human",  ["python", "human.py"], "../client/human"),
            "basic1": Player("Basic1", ["python", "really_simple_client.py"], "../client/python_sample"),
            "basic2": Player("Basic2", ["python", "simple_client.py"], "../client/python_sample")}
