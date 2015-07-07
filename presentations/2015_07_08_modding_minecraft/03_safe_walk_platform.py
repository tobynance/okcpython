from base_command import BaseCommand
from mcpi import block
from mcpi.vec3 import Vec3

REPLACE_BLOCKS = [block.WATER.id,
                  block.WATER_FLOWING.id,
                  block.WATER_STATIONARY.id,
                  block.AIR.id]


########################################################################
class Mod(BaseCommand):
    heart_beat_rate = 0.01

    ####################################################################
    def get_surrounding_blocks(self, pos, distance=1):
        """
        Get all the positions around `pos` on the XZ plane,
        including the `pos` block.
        """
        for x in range(-distance, distance+1):
            for z in range(-distance, distance+1):
                yield Vec3(pos.x+x, pos.y, pos.z+z)

    ####################################################################
    def on_heart_beat(self):
        pos = self.player.getTilePos()
        pos.y -= 1  # block BELOW the player

        for p in self.get_surrounding_blocks(pos):
            b = self.get_block(p)
            if b in REPLACE_BLOCKS:
                self.set_block(p, block.ICE.id)

########################################################################
if __name__ == "__main__":
    Mod().run()
