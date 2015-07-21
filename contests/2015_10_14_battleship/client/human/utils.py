#######################################################################
class Vector2(object):
    def __init__(self, x = 0, y = 0):
        self.x = int(x)
        self.y = int(y)

    ###################################################################
    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False

    ###################################################################
    def __ne__(self, other):
        return not(self == other)

    ###################################################################
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    ###################################################################
    def copy(self):
        return Vector2(self.x, self.y)

    ###################################################################
    def set(self, other):
        self.x = other.x
        self.y = other.y

    ###################################################################
    @staticmethod
    def from_objs(P1, P2):
        return Vector2(P2.x - P1.x, P2.y - P1.y)

    ###################################################################
    @staticmethod
    def from_points(P1, P2):
        return Vector2(P2[0] - P1[0], P2[1] - P1[1])

    ###################################################################
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    ###################################################################
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    ###################################################################
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    ###################################################################
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    ###################################################################
    def __neg__(self):
        return Vector2(-self.x, -self.y)
