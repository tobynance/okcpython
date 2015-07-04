from mcpi import block
from mcpi import minecraft

########################################################################
def run():
    world = minecraft.Minecraft.create()
    player = world.player

    pos = player.getTilePos()
    width = 10
    world.setBlocks(pos.x-width, pos.y-1, pos.z-width, pos.x+width, pos.y-1, pos.z+width, block.DIRT.id)
