from utils import Vector2


#######################################################################
class Ship(object):
    def __init__(self, point1, point2, my_grid = False):
        self.my_grid = my_grid
        self.set(point1, point2)

    ###################################################################
    def set(self, point1, point2):
        assert(isinstance(point1, Vector2))
        assert(isinstance(point2, Vector2))
        point1 = point1.copy()
        point2 = point2.copy()
        self.points = []
        if point1 == point2:
            self.points.append(point1)
            self.point = point1.copy()
            self.size = 1
            self.horizontal = True
            self.left = point1.copy()
            self.right = point1.copy()
        elif point1.x == point2.x:
            ### vertical ship
            self.horizontal = False
            if point1.y < point2.y:
                self.top = point1.copy()
                self.bottom = point2.copy()
            else:
                self.top = point2.copy()
                self.bottom = point1.copy()
        else:
            assert(point1.y == point2.y)
            ### horizontal ship
            self.horizontal = True
            if point1.x < point2.x:
                self.left = point1.copy()
                self.right = point2.copy()
            else:
                self.left = point2.copy()
                self.right = point1.copy()
        
        if self.horizontal:
            self.size = 1 + self.right.x - self.left.x
            x, y = self.left.x, self.left.y
            while x <= self.right.x:
                self.points.append(Vector2(x, y))
                x += 1
        else:
            self.size = 1 + self.bottom.y - self.top.y
            x, y = self.top.x, self.top.y
            while y <= self.bottom.y:
                self.points.append(Vector2(x, y))
                y += 1
    ###################################################################
    def point_in_ship(self, x, y):
        p = Vector2(x, y)
        if p in self.points:
            return True
        return False

    ###################################################################
    def move_to(self, x, y):
        diff_x = self.points[0].x - x
        diff_y = self.points[0].y - y
        for pt in self.points:
            pt.x -= diff_x
            pt.y -= diff_y
        if self.horizontal:
            for pt in [self.left, self.right]:
                pt.x -= diff_x
                pt.y -= diff_y
        else:
            for pt in [self.top, self.bottom]:
                pt.x -= diff_x
                pt.y -= diff_y
    
    ###################################################################
    def rotate(self):
        if self.size == 1:
            return
        if self.horizontal:
            first_point = self.left
            last_point = first_point.copy()
            last_point.y += (self.size - 1)
            self.set(first_point, last_point)
        else:
            first_point = self.top
            last_point = first_point.copy()
            last_point.x += (self.size - 1)
            self.set(first_point, last_point)

    ###################################################################
    def __str__(self):
        if self.horizontal:
            return "<SHIP HORIZONTAL (%d) |%d %d|%d %d|>" % (self.size, self.left.x, self.left.y, self.right.x, self.right.y)
        else:
            return "<SHIP VERTICAL (%d) |%d %d|%d %d|>" % (self.size, self.top.x, self.top.y, self.bottom.x, self.bottom.y)

    ###################################################################
    @staticmethod
    def from_string(text):
        text = str(text)
        if text.startswith("<SHIP"):
            pts = text.split("|")[1:3]
            p1, p2 = [[int(n) for n in p.split()] for p in pts]
            ship = Ship(Vector2(*p1), Vector2(*p2))
            return ship
        return None
