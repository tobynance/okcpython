### Assume the player is likely to move in the direction they are facing, or in the same direction they have been moving

from base_command import BaseCommand
from mcpi import block

REPLACE_BLOCKS = [block.WATER.id,
                  block.WATER_FLOWING.id,
                  block.WATER_STATIONARY.id,
                  block.AIR.id]


########################################################################
class Mod(BaseCommand):
    heart_beat_rate = 0.001

    ####################################################################
    def on_heart_beat(self):
        pos = self.player.getTilePos()
        pos.y -= 1  # block BELOW the player

        b = self.get_block(pos)
        if b in REPLACE_BLOCKS:
            self.set_block(pos, block.ICE.id)

########################################################################
if __name__ == "__main__":
    Mod().run()
