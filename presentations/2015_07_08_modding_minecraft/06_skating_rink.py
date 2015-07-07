from base_command import BaseCommand
from mcpi import block
from mcpi.vec3 import Vec3

REPLACE_BLOCKS = [block.WATER.id,
                  block.WATER_FLOWING.id,
                  block.WATER_STATIONARY.id,
                  block.ICE.id]

RANGE = 5

########################################################################
class Mod(BaseCommand):
    ####################################################################
    def once(self):
        self.replaced = set()
        self.to_replace = set()
        pos = self.player.getTilePos()

        blocks = self.get_blocks(Vec3(pos.x-RANGE,
                                      pos.y-1,
                                      pos.z-RANGE),
                                 Vec3(pos.x+RANGE,
                                      pos.y-1,
                                      pos.z+RANGE))
        for p, b in blocks:
            if b in REPLACE_BLOCKS:
                self.to_replace.add(p)
        self.make_rink()

    ####################################################################
    def make_rink(self):
        while len(self.to_replace) > 0:
            pos = self.to_replace.pop()
            print "replacing block at", pos
            self.set_block(pos, block.ICE.id)
            self.replaced.add(pos)

            # check all neighbors
            for x in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if x == z == 0:
                        continue
                    new_pos = Vec3(pos.x+x,
                                   pos.y,
                                   pos.z+z)
                    if new_pos in self.replaced or new_pos in self.to_replace:
                        continue
                    b = self.get_block(new_pos)
                    if b in REPLACE_BLOCKS:
                        self.to_replace.add(new_pos)

########################################################################
if __name__ == "__main__":
    Mod().once()
