class Circle:

    def __init__(self, a, b):
        self.centre, self.radius = a, b

    def __contains__(self, other):
        x, y, r = self.centre[0], self.centre[1], self.radius
        if (other[0] - x)**2 + (other[1] - y)**2 <= r**2:
            return True
        return False
