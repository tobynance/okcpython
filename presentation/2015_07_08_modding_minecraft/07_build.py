from base_command import BaseCommand
from mcpi import block
from mcpi.vec3 import Vec3


########################################################################
class Mod(BaseCommand):
    HOUSE_WIDTH = 12
    HOUSE_HEIGHT = 4

    ####################################################################
    def buildHouse(self, x, y, z):
        self.clearHouse(x, y, z)
        #draw floor
        self.world.setBlocks(x,y-1,z,x+self.HOUSE_WIDTH,y-1,z+self.HOUSE_WIDTH,block.GRASS.id)
    
        #draw walls
        self.world.setBlocks(x, y, z, x+self.HOUSE_WIDTH, y+self.HOUSE_HEIGHT, z, block.STONE.id)
        self.world.setBlocks(x+self.HOUSE_WIDTH, y, z, x+self.HOUSE_WIDTH, y+self.HOUSE_HEIGHT, z+self.HOUSE_WIDTH, block.STONE.id)
        self.world.setBlocks(x+self.HOUSE_WIDTH, y, z+self.HOUSE_WIDTH, x, y+self.HOUSE_HEIGHT, z+self.HOUSE_WIDTH, block.STONE.id)
        self.world.setBlocks(x, y, z+self.HOUSE_WIDTH, x, y+self.HOUSE_HEIGHT, z, block.STONE.id)
    
        #draw windows
        self.world.setBlocks(x+(self.HOUSE_WIDTH/2)-2,y+1,z,x+(self.HOUSE_WIDTH/2)-2,y+2,z,block.GLASS.id)
        self.world.setBlocks(x+(self.HOUSE_WIDTH/2)+2,y+1,z,x+(self.HOUSE_WIDTH/2)+2,y+2,z,block.GLASS.id)

        self.world.setBlocks(x+(self.HOUSE_WIDTH/2)-2,y+1,z+self.HOUSE_WIDTH,x+(self.HOUSE_WIDTH/2)+2,y+2,z+self.HOUSE_WIDTH,block.GLASS.id)
        self.world.setBlocks(x,y+1,z+(self.HOUSE_WIDTH/2)-2,x,y+2,z+(self.HOUSE_WIDTH/2)+2,block.GLASS.id)
        self.world.setBlocks(x+self.HOUSE_WIDTH,y+1,z+(self.HOUSE_WIDTH/2)-2,x+self.HOUSE_WIDTH,y+2,z+(self.HOUSE_WIDTH/2)+2,block.GLASS.id)

         #cobble arch
        self.world.setBlocks(x+(self.HOUSE_WIDTH/2)-1,y,z,x+(self.HOUSE_WIDTH/2)+1,y+2,z,block.COBBLESTONE.id)
        # clear space for door
        self.world.setBlocks(x+(self.HOUSE_WIDTH/2),y,z,x+(self.HOUSE_WIDTH/2),y+1,z,block.AIR.id)

        # small porch
        self.world.setBlocks(x+(self.HOUSE_WIDTH/2)-2,y-1,z,x+(self.HOUSE_WIDTH/2)+2,y-1,z-2,block.WOOD_PLANKS.id)
        self.world.setBlocks(x+(self.HOUSE_WIDTH/2)-2,y,z-1,x+(self.HOUSE_WIDTH/2)+2,y+3,z-2,block.AIR.id)

        # torches aren't working, so add some glow stones for light
        # self.world.setBlock(x+(self.HOUSE_WIDTH/2)-1,y+2,z-1,block.TORCH.id,1)
        # self.world.setBlock(x+(self.HOUSE_WIDTH/2)+1,y+2,z-1,block.TORCH.id,1)
        self.world.setBlock(x+(self.HOUSE_WIDTH/2)-1,y+3,z,block.GLOWSTONE_BLOCK.id)
        self.world.setBlock(x+(self.HOUSE_WIDTH/2)+1,y+3,z,block.GLOWSTONE_BLOCK.id)

        self.world.setBlock(x+(self.HOUSE_WIDTH/2)-1,y+3,z+self.HOUSE_WIDTH,block.GLOWSTONE_BLOCK.id)
        self.world.setBlock(x+(self.HOUSE_WIDTH/2)+1,y+3,z+self.HOUSE_WIDTH,block.GLOWSTONE_BLOCK.id)

        self.world.setBlock(x,y+3,z+(self.HOUSE_WIDTH/2)-1,block.GLOWSTONE_BLOCK.id)
        self.world.setBlock(x,y+3,z+(self.HOUSE_WIDTH/2)+1,block.GLOWSTONE_BLOCK.id)

        self.world.setBlock(x+self.HOUSE_WIDTH,y+3,z+(self.HOUSE_WIDTH/2)-1,block.GLOWSTONE_BLOCK.id)
        self.world.setBlock(x+self.HOUSE_WIDTH,y+3,z+(self.HOUSE_WIDTH/2)+1,block.GLOWSTONE_BLOCK.id)

        # draw roof
        self.world.setBlocks(x,y+self.HOUSE_HEIGHT+1,z,x+self.HOUSE_WIDTH,y+self.HOUSE_HEIGHT+1,z+self.HOUSE_WIDTH,block.WOOD_PLANKS.id)

        # Add a woolen carpet, the colour is 14, which is red.
        self.world.setBlocks(x+1, y-1, z+1, x+self.HOUSE_WIDTH-1, y-1, z+self.HOUSE_WIDTH-1, block.WOOL.id, 14)

        # # draw door
        # self.world.setBlock(x+(self.HOUSE_WIDTH/2),y,z,block.DOOR_WOOD.id, 3)
        # self.world.setBlock(x+(self.HOUSE_WIDTH/2),y+1,z,block.DOOR_WOOD.id, 8)
        # # draw torches
        # self.world.setBlock(x+(self.HOUSE_WIDTH/2)-1,y+2,z-1,block.TORCH.id,4)
        # self.world.setBlock(x+(self.HOUSE_WIDTH/2)+1,y+2,z-1,block.TORCH.id,4)

    ####################################################################
    def clearHouse(self, x, y, z):
        self.world.setBlocks(x-2,y-1,z-2,x+self.HOUSE_WIDTH+2,y+self.HOUSE_HEIGHT+1,z+self.HOUSE_WIDTH+2,block.AIR.id)

    ####################################################################
    def once(self):
        pos = self.player.getTilePos()
        print "pos:", pos
        b = self.get_block(pos.x, pos.y, pos.z+1)
        print b
        b = self.get_block(pos.x, pos.y+1, pos.z+1)
        print b
        b = self.world.getBlockWithData(pos.x, pos.y, pos.z+1)
        print b
        b = self.world.getBlockWithData(pos.x, pos.y+1, pos.z+1)
        print b

        # self.world.setBlock(481, 2, -263, block.DOOR_WOOD.id, 1)
        # self.world.setBlock(481, 3, -263, block.DOOR_WOOD.id, 8)
        self.buildHouse(pos.x+2, pos.y, pos.z)
        self.world.setBlock(489, 2, -263, block.DOOR_WOOD.id, 1)
        self.world.setBlock(489, 3, -263, block.DOOR_WOOD.id, 8)
        # self.house(Vec3(pos.x+2, pos.y, pos.z))

        # self.set_block(pos.x+3, pos.y, pos.z, block.TORCH.id)
        # self.set_block(pos.x+3, pos.y+1, pos.z, block.TORCH.id, 4)




########################################################################
if __name__ == "__main__":
    Mod().once()
