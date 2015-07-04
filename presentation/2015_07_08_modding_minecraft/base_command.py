from mcpi import minecraft, vec3
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
            if isinstance(arg, vec3.Vec3):
                output += [arg.x, arg.y, arg.z]
            else:
                output.append(arg)
        return output

    ####################################################################
    def set_block(self, *args):
        args = self._maybe_convert_arg_from_vec(args)
        self.world.setBlock(*args)

    ####################################################################
    def get_block(self, *args):
        args = self._maybe_convert_arg_from_vec(args)
        return self.world.getBlock(*args)

    ####################################################################
    def run(self):
        while True:
            self.on_heart_beat()
            time.sleep(self.heart_beat_rate)

    ####################################################################
    def on_heart_beat(self):
        raise NotImplementedError
