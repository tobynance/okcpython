from mcpi import minecraft
from mcpi.vec3 import Vec3
import time


########################################################################
class BaseCommand(object):
    heart_beat_rate = 0.1

    ####################################################################
    def __init__(self):
        self.world = minecraft.Minecraft.create()
        self.player = self.world.player

    ####################################################################
    def _maybe_convert_arg_from_vec(self, args):
        output = []
        for arg in args:
            if isinstance(arg, Vec3):
                output += [arg.x, arg.y, arg.z]
            else:
                output.append(arg)
        return output

    ####################################################################
    def set_block(self, *args):
        # print "setting block:", args
        args = self._maybe_convert_arg_from_vec(args)
        self.world.setBlock(*args)

    ####################################################################
    def get_block(self, *args):
        args = self._maybe_convert_arg_from_vec(args)
        return self.world.getBlock(*args)

    ####################################################################
    def get_blocks(self, start_pos, end_pos):
        args = list(start_pos) + list(end_pos)
        # print "get_blocks:", args
        blocks = self.world.getBlocks(*args)
        block_index = 0
        for x in range(start_pos.x, end_pos.x+1):
            for y in range(start_pos.y, end_pos.y+1):
                for z in range(start_pos.z, end_pos.z+1):
                    yield (Vec3(x, y, z), blocks[block_index])
                    block_index += 1

    ####################################################################
    def get_surrounding_blocks(self, pos, distance=1):
        """
        Get all the positions around `pos` on the XZ plane,
        including the `pos` block.
        """
        return self.get_blocks(Vec3(pos.x-distance,
                                    pos.y,
                                    pos.z-distance),
                               Vec3(pos.x+distance,
                                    pos.y,
                                    pos.z+distance))

    ####################################################################
    def set_blocks(self, *args):
        args = self._maybe_convert_arg_from_vec(args)
        self.world.setBlocks(*args)

    ####################################################################
    def run(self):
        while True:
            self.on_heart_beat()
            time.sleep(self.heart_beat_rate)

    ####################################################################
    def on_heart_beat(self):
        raise NotImplementedError
