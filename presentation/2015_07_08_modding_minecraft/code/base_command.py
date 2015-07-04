from mcpi import minecraft
import time


########################################################################
class BaseCommand(object):
    ####################################################################
    def __init__(self):
        self.world = minecraft.Minecraft.create()
        self.player = self.world.player

    ####################################################################
    def run(self):
        while True:
            self.on_heart_beat()
            time.sleep(0.01)

    ####################################################################
    def on_heart_beat(self):
        pass
