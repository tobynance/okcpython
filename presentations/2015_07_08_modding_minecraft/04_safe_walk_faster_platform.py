from base_command import BaseCommand
from mcpi import block
from mcpi.vec3 import Vec3

REPLACE_BLOCKS = [block.WATER.id,
                  block.WATER_FLOWING.id,
                  block.WATER_STATIONARY.id,
                  block.AIR.id]


########################################################################
class Mod(BaseCommand):
    heart_beat_rate = 0.05

    ####################################################################
    def on_heart_beat(self):
        pos = self.player.getTilePos()
        blocks = self.get_blocks(Vec3(pos.x-1,
                                      pos.y-2,
                                      pos.z-1),
                                 Vec3(pos.x+1,
                                      pos.y-1,
                                      pos.z+1))
        for p, b in blocks:
            if b in REPLACE_BLOCKS:
                self.set_block(p, block.ICE.id)

########################################################################
if __name__ == "__main__":
    Mod().run()
