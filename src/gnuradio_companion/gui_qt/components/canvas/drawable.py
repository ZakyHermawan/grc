class Drawable(object):
    """
    GraphicalElement is the base class for all graphical elements.
    It contains an X,Y coordinate, a list of rectangular areas that the element occupies,
    and methods to detect selection of those areas.
    """

    @classmethod
    def make_cls_with_base(cls, super_cls):
        name = super_cls.__name__
        bases = (super_cls,) + cls.__bases__[1:]
        namespace = cls.__dict__.copy()
        return type(name, bases, namespace)

    def __init__(self):
        """
        Make a new list of rectangular areas and lines, and set the coordinate and the rotation.
        """
        self.coordinate = (0, 0)
        self.rotation = 0
        self.highlighted = False

        self._bounding_rects = []
        self._bounding_points = []
