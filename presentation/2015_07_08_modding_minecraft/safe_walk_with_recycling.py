import math
from base_command import BaseCommand
from mcpi import block


########################################################################
class Mod(BaseCommand):
    heart_beat_rate = 0.01
    ####################################################################
    def __init__(self):
        super(Mod, self).__init__(heart_beat_rate=0.001)
        self.old_ice_position = None
        self.old_ice_type = None

    ####################################################################
    def on_heart_beat(self):
        pos = self.player.getTilePos()
        pos.y -= 1  # block BELOW the player
        if self.old_ice_position and pos != self.old_ice_position:
            self.world.setBlock(self.old_ice_position.x,
                                self.old_ice_position.y,
                                self.old_ice_position.z,
                                self.old_ice_type)

        b = self.world.getBlock(pos.x, pos.y, pos.z)
        if b in [block.WATER.id, block.WATER_FLOWING.id, block.WATER_STATIONARY.id, block.AIR.id]:
            self.world.setBlock(pos.x,
                                pos.y,
                                pos.z,
                                block.ICE.id)
            self.old_ice_position = pos
            self.old_ice_type = b

########################################################################
if __name__ == "__main__":
    Mod().run()
