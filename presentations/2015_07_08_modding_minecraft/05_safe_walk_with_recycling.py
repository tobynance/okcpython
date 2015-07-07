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
    def __init__(self):
        super(Mod, self).__init__()
        self.old_ice_blocks = set()

    ####################################################################
    def on_heart_beat(self):
        pos = self.player.getTilePos()
        # print "*" * 20
        # print "pos:", pos
        for p, b in self.old_ice_blocks.copy():
            if p.y >= pos.y or (pos - p).length() > 4:
                self.set_block(p, b)
                # print "reset back to old:", p, b
                self.old_ice_blocks.remove((p, b))

        blocks = self.get_blocks(Vec3(pos.x-2,
                                      pos.y-2,
                                      pos.z-2),
                                 Vec3(pos.x+2,
                                      pos.y-1,
                                      pos.z+2))
        for p, b in blocks:
            # print "p, b:", p, b
            if b in REPLACE_BLOCKS:
                self.old_ice_blocks.add((p, b))
                self.set_block(p, block.ICE.id)
                # print "set ice:", p, b


########################################################################
if __name__ == "__main__":
    Mod().run()
