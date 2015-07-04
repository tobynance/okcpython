from base_command import BaseCommand
from mcpi import block


########################################################################
class Mod(BaseCommand):
    ####################################################################
    def once(self):
        pos = self.player.getTilePos()
        width = 10
        self.world.setBlocks(pos.x-width,
                             pos.y-1,
                             pos.z-width,
                             pos.x+width,
                             pos.y-1,
                             pos.z+width,
                             block.DIRT.id)

########################################################################
if __name__ == "__main__":
    Mod().once()
