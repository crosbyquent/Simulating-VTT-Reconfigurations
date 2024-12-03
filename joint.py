from vpython import *

class Joint:
    def __init__(self, x, y, z, radius=0.1, color=color.black):
        if not all(isinstance(coord, (int, float)) for coord in [x, y, z]):
            raise TypeError("Coordinates for a joint must be numbers.")
        self.sphere = sphere(pos=vector(x, y, z), radius=radius, color=color)

    @property
    def position(self):
        return self.sphere.pos