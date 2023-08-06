# -*- coding: utf-8 -*-
"""
Interface to drawing libraries: base for all formats
"""


class Color(tuple):
    """
    A color is defined by the name of the color system (RGB or CMYK) + a tuple of values;
    The value returned by colors is only the tuple.
    """
    def __new__(cls, csys, *values):  # Creates the tuple
        return super().__new__(cls, values)

    def __init__(self, csys, *values):  # Initialises csys and checks the values
        super().__init__()
        self._csys = csys
        if csys == "CMYK":
            if not (3 < len(values) < 6):
                raise TypeError("CMYK colors need 4 or 5 arguments (with alpha).")
        elif csys == "RGB":
            if not (2 < len(values) < 5):
                raise TypeError("RBG colors need 3 or 4 arguments (with alpha).")
        else:
            raise ValueError(f"Unknown color system: {csys}.")

    def colorsystem(self):
        return self._csys

    def luminance(self):
        """Luminance might be a bit hyped since this is a little rough, but that's the idea (against white back)"""
        colamount = sum(self.__getitem__(slice(0, -1))) / (len(self)-1)
        opacity = self.__getitem__(-1)
        if self._csys == "RGB":
            return (1 - opacity) + colamount * opacity
        else:
            return 1 - colamount * opacity


class Prop:
    """Some property"""
    def __init__(self, current, default):
        self.current = current
        self.default = default


class CanvasBase:
    def __init__(self, outfile, colorsys, *args):
        self.filename = outfile
        self.id = 0
        self.clipRect = None
        self.style = None
        if colorsys == "CMYK":
            # As CMYK + alpha (opacity)
            self.colors = {
                'black': Color("CMYK", 0, 0, 0, 1.0, 1.0),  # Standard black, for texts and lines
                'blue': Color("CMYK", 1.0, 0.4, 0, 0, 1.0),
                'dpurple': Color("CMYK", 0.51, 1.0, 0.31, 0.14, 1.0),  # dark purple
                'dyellow': Color("CMYK", 0, 0.2, 0.99, 0, 1.0),  # dark yellow
                'red': Color("CMYK", 0, 0.88, 0.85, 0, 1.0),
                'green': Color("CMYK", 0.95, 0.0, 0.95, 0, 1.0),
                'vdgrey': Color("CMYK", 0, 0, 0, 0.7, 1.0),
                'dgrey': Color("CMYK", 0, 0, 0, 0.55, 1.0),
                'grey': Color("CMYK", 0, 0, 0, 0.37, 1.0),
                'lgrey': Color("CMYK", 0, 0, 0, 0.18, 1.0),
                'vlgrey': Color("CMYK", 0, 0, 0, 0.09, 1.0),  # Very light grey
                'tgrey': Color("CMYK", 0, 0, 0, 1.0, 0.5),  # Transparent grey
                'tdgrey': Color("CMYK", 0, 0, 0, 1.0, 0.7),  # Transparent dark grey
                'white': Color("CMYK", 0, 0, 0, 0, 1.0),
                'transparent': Color("CMYK", 0, 0, 0, 0, 0),
                'transluscent': Color("CMYK", 0, 0, 0, 0, 0.4),  # Transluscent = transparent white
                'ltransluscent': Color("CMYK",  0, 0, 0, 0, 0.15)  # Slightly ransluscent = almost white
            }
        else:
            # As RGBA (default)
            self.colors = {
                'black': Color("RGB", 0, 0, 0, 1.0),
                'blue': Color("RGB", 0, 0, 0.9, 1.0),
                'dpurple': Color("RGB", 0.51, 0.13, 0.39, 1.0),  # dark purple
                'dyellow': Color("RGB", 0.9, 0.8, 0, 1.0),  # dark yellow
                'red': Color("RGB", 0.9, 0, 0, 1.0),
                'green': Color("RGB", 0, 0.9, 0, 1.0),
                'vdgrey': Color("RGB", 0.3, 0.3, 0.3, 1.0),
                'dgrey': Color("RGB", 0.45, 0.45, 0.45, 1.0),
                'grey': Color("RGB", 0.63, 0.63, 0.63, 1.0),
                'lgrey': Color("RGB", 0.82, 0.82, 0.82, 1.0),
                'vlgrey': Color("RGB", 0.91, 0.91, 0.91, 1.0),  # Very light grey
                'tgrey': Color("RGB", 0, 0, 0, 0.5),
                'tdgrey': Color("RGB", 0, 0, 0, 0.3),  # Transparent dark grey
                'white': Color("RGB", 1.0, 1.0, 1.0, 1.0),
                'transparent': Color("RGB", 0, 0, 0, 0),
                'transluscent': Color("RGB", 1.0, 1.0, 1.0, 0.60),  # Transluscent = transparent white
                'ltransluscent': Color("RGB", 1.0, 1.0, 1.0, 0.85)  # Slightly ransluscent = almost white
            }
        self.fill = Prop(None, self.colors['black'])
        self.stroke = Prop(None, self.colors['black'])
        self.stroke_width = Prop(None, 1.0)

    def repcolor(self, color, default=None):
        """
        Transforms a color to the appropriate object for the graphic format
        Color can be
            - None: the feature of the receiving object should be ignored (e.g. no stroke line at all).
            - "currentcolor": use the color of a parent element
            - the name of a colour defined in Canvas.colors
            - a tuple defining the color as RGB+A or CMYK+A (all numbers between 0 and 1)
        :param color: a color
        :param default: if defined, would replace acolor=None
        :return:
        """
        if not (color or default):
            return None  # Can pass none if no color is defined
        if not color:
            color = default
        if color == "currentcolor":
            return color
        elif type(color) is str:
            try:
                return self.colors[color]
            except KeyError:
                raise ValueError(f"Color name '{color}' is not defined in EmberFactory>Drawinglib>Canvas")
        elif isinstance(color, Color):
            return color
        else:
            raise TypeError(f"Argument cannot be used as color: {color}")

    def set_stroke_width(self, width):
        self.stroke_width.default = width

    def group(self, eid):
        # Group => groups drawable items and has an ID (eid => element ID, to distinguish from Python object id)
        return

    def line(self, x1, y1, x2, y2, stroke, stroke_width, dash, markers, eid):
        if markers:
            markrad = 2.5
            markps = ((x1, y1), (x2, y2))
            for markp in markps:
                self.circle(*markp, markrad, fill=None, stroke=stroke or "black", )

    def circle(self, *args, **kwargs):
        pass
