# -*- coding: utf-8 -*-
"""
Interface to drawing libraries: PDF with ReportLab.
"""
from os import path
from reportlab.pdfgen.canvas import Canvas as RLCanvas
from reportlab.lib import colors as col
from embermaker.drawinglib import canvas_base
from embermaker.drawinglib.helpers import cm, textwrapsub, defaultfont


def subsuper(scriptlevel, fontsize, string):
    """
    :param scriptlevel: "sub" or "super"
    :param fontsize:
    :param string:
    :return:
    Provides a string with the tag needed for sub/superscripts, for use in textwrapsub
    :return: the processed string for use within this module: prepares for operations within paragraph() by adding ¶
    """
    return f"¶_{string}" if scriptlevel == "sub" else f"¶^{string}"


class CanvasPdf(canvas_base.CanvasBase):

    def __init__(self, outfile, colorsys, size):
        super().__init__(outfile, colorsys, size)
        self.filename = path.splitext(outfile)[0] + '.pdf'
        self.can = RLCanvas(self.filename, enforceColorSpace=colorsys)

    def repcolor(self, acolor, default=None):
        """
        The representation of the colour for PDF files with ReportLab
        :param acolor: a colour name or tuple
        :param default:
        :return: a string that can be used as colour with ReportLab
        """
        usecolor = super().repcolor(acolor, default)
        if usecolor == "currentcolor":
            usecolor = self.colors("black")  # currentcolor is for svg's - not supported here so far.
        if not usecolor:
            return None  # Can pass none if no color is defined
        elif isinstance(usecolor, canvas_base.Color):
            return col.Color(*usecolor)
        else:
            raise ValueError(f"Color {usecolor} is not defined in EmberFactory>Drawinglib>CanvasPdf")

    def _set_fill_color(self, color):
        usecolor = color if color else self.fill.default
        if self.fill.current != usecolor:
            self.can.setFillColor(self.repcolor(usecolor))
            self.fill.current = usecolor

    def _set_stroke_color(self, color):
        usecolor = color if color else self.stroke.default
        if self.stroke.current != usecolor:
            self.can.setStrokeColor(self.repcolor(usecolor))
            self.stroke.current = usecolor

    def _set_stroke_width(self, width):
        usewidth = width if width else self.stroke_width.default
        if self.stroke_width.current != usewidth:
            self.can.setLineWidth(usewidth)
            self.stroke_width.current = usewidth

    def set_page_size(self, size):
        self.can.setPageSize(size)

    def line(self, x1, y1, x2, y2, stroke=None, stroke_width=None, dash=None, markers=None, eid=None):
        super().line(x1, y1, x2, y2, stroke, stroke_width, dash, markers, eid)
        self._set_stroke_color(stroke)
        self._set_stroke_width(stroke_width)
        if dash:
            self.can.setDash([3, 3], 1)  # 3 unit on, 2 unit off; the last parameter defines a start point with dashes.
        self.can.line(x1, y1, x2, y2)
        if dash:
            self.can.setDash([], 0)  # Stop dashes = back to solid, unbroken line (this is from Adobe PDF reference)

    def rect(self, x, y, width, height, fill=None, stroke=None, stroke_width=None, tooltip=None, eid=None):
        self._set_stroke_color(stroke)
        self._set_fill_color(fill)
        self._set_stroke_width(stroke_width)
        self.can.rect(x, y, width, height,
                      stroke=stroke is not None,
                      fill=fill is not None)

    def circle(self, x, y, rad, fill=None, stroke=None):
        self._set_stroke_color(stroke)
        self._set_fill_color(fill)
        self.can.circle(x, y, rad, fill=fill is not None, stroke=stroke is not None)

    def lin_gradient_rect(self, cliprect: tuple, gradaxis: tuple, colorlevels: list, plotlevels: list, eid=None):
        """
        Draws a rectangle filled with a linear gradient
        :param cliprect:
        :param gradaxis: a tuple defining the axis on which the gradient's stops are defined, as (x0, y0, x1, y1)
        :param colorlevels:
        :param plotlevels:
        :param eid: the element's id
        :return:
        """
        # Store the drawing context to come back to it after plotting the gradients
        c = self.can
        c.saveState()

        # Restrict the viewable area to the frame enclosing the BE
        # (colour gradients do not have x limits, hence the need to limit their visible part):
        p = c.beginPath()
        p.rect(*cliprect)
        c.clipPath(p, stroke=0)

        # Draw the color gradients
        repcolorslevels = (self.repcolor(color) for color in colorlevels)
        c.linearGradient(*gradaxis, repcolorslevels, plotlevels)
        # Had extend=False before (= show beyond ends); this was causing trouble with Adobe Illustrator 2021.

        c.restoreState()

    def string(self, xx, yy, text, align='left', font=None, scale=1.0, color="black"):
        """
        Draws text with interpretation of '^' and '_' as symbols
        to indicate that the next character is a superscript (e.g m^2) or subscript (CO_2).

        :param xx: x position
        :param yy: y position
        :param text: a string to draw on the canvas
        :param align: if set to 'right', behaves like drawRightString;
                      if set to 'center', behaves like drawCentredString; by default, aligns to the left
        :param scale: scales the text horizontally; scale < 1.0 produces condensed text.
        :param font: tuple (font name, font size)
        :param color: font color
        :return: experimental: length
        """
        font = defaultfont(font)
        smallfont = (font[0], font[1] * 0.7)  # Font for the sub/superscripts
        textobject = self.can.beginText()

        # Split the string for processing any sub/superscript, keeping the _ or ^ so as to act appropriately
        splitexp = text.replace('^', '¶^').replace('_', '¶_').split('¶')
        # Alignment: first calculate the true length of text, given smaller sub/superscripts
        ltext = self.can.stringWidth(splitexp[0], *font)  # Before any superscript (exponent, ^)
        if len(splitexp) > 1:  # If at least one superscript
            for splitpart in splitexp[1:]:  # A fraction of text starting with a sub/superscript
                ltext += self.can.stringWidth(splitpart[1], *smallfont)  # length of the superscripted character
            if len(splitexp[-1]) > 1:  # if there is some string after the sub/superscripted character
                ltext += self.can.stringWidth(splitexp[-1][2:], *font)

        xleft = xx  # Left position, adjusted if align is set
        if align == 'right':
            xleft -= ltext
        elif align == 'center':
            xleft -= ltext / 2.0

        textobject.setTextOrigin(xleft, yy)
        textobject.setTextTransform(scale, 0, 0, 1.0, xleft, yy)
        textobject.setFillColor(color)
        textobject.setFont(*font)
        textobject.textOut(splitexp[0])
        if len(splitexp) > 1:
            for splitpart in splitexp[1:]:
                textobject.setFont(*smallfont)
                if splitpart[0] == '^':
                    textobject.setRise(4)
                else:
                    textobject.setRise(-3)
                textobject.textOut(splitpart[1])
                textobject.setFont(*font)
                textobject.setRise(0)
                if len(splitpart) > 1:
                    textobject.textOut(splitpart[2:])
        self.can.drawText(textobject)
        return ltext

    def paragraph(self, xx, yy, text, width=5*cm, align='left',  valign='bottom', rotate=0,
                  font=None, scale=1.0, color="black", breakwords=True):
        """
        Draws a paragraph within a box of max width = length, with interpretation of '^' and '_' as symbols
        to indicate that the next character is a superscript (e.g m^2) or subscript (CO_2).

        :param xx: x position
        :param yy: y position
        :param text: the text of the paragraph
        :param width: a string to draw on the canvas
        :param width: the length of a box in which the paragraph will be placed
        :param align: if set to 'right', behaves like drawRightString;
                      if set to 'center', behaves like drawCentredString; by default, aligns to the left
        :param valign: vertical alignment
        :param rotate: rotation angle
        :param font: tuple (font name, font size)
        :param scale: scales the text horizontally; scale < 1.0 produces condensed text.
        :param color: font color
        :param breakwords: whether words can be broken at end of line
        """
        font = defaultfont(font)
        normsize = float(font[1])
        smallfont = (font[0], font[1] * 0.7)  # Font for the sub/superscripts
        linespacing = normsize * 1.1
        lines = textwrapsub(text, width, normsize, font[0], breakwords, subsuper)

        if valign == "bottom":
            ytrans = len(lines) * linespacing
        elif valign == "top":
            ytrans = 0
        else:  # Center
            ytrans = len(lines) * linespacing * 0.666

        self.can.saveState()
        self.can.translate(xx, yy)
        if rotate:
            self.can.rotate(rotate)

        textobject = self.can.beginText()
        textobject.setFillColor(self.repcolor(color))
        textobject.setFont(*font)

        for iline, line in enumerate(lines):
            actwidth = min(line[1], width)
            if align == "left":
                xtrans = 0
            elif align == "right":
                xtrans = -actwidth
            elif align == "center":
                xtrans = -actwidth / 2.0
            else:
                raise ValueError(f"Align = {align} is not valid.")

            if line[1] > width:
                textobject.setHorizScale(width/line[1]*100.0*scale)
            else:
                textobject.setHorizScale(100.0*scale)

            textobject.setTextOrigin(xtrans, ytrans - linespacing * (iline+1))

            if "¶" in line[0]:
                splitexp = line[0].split('¶')
                textobject.textOut(splitexp[0])
                for splitpart in splitexp[1:]:
                    textobject.setFont(*smallfont)
                    if splitpart[0] == '^':
                        textobject.setRise(4)
                    else:
                        textobject.setRise(-3)
                    wordsinpart = splitpart.split(' ', 1)  # 1 is the "max split" parameter : only first white is split
                    textobject.textOut(wordsinpart[0][1:])  # The sub or superscripted part = up to the first blank
                    textobject.setFont(*font)
                    textobject.setRise(0)
                    if len(wordsinpart) > 1:
                        print(splitpart, wordsinpart)
                        textobject.textOut(" " + wordsinpart[1]) # The rest of that piece of text
            else:
                textobject.textOut(line[0])

        self.can.drawText(textobject)
        self.can.restoreState()
        # For verification:
        # self.rect(xx - (width/2.0 if align=="center" else 0.0),
        #          yy, width, (-1.0 if valign=="top" else 1.0) * len(lines) * linespacing, stroke="green")


    def set_creator(self, creator):
        self.can.setCreator(creator)

    def set_subject(self, subject):
        self.can.setSubject(subject)

    def set_keywords(self, keywords):
        self.can.setKeywords(keywords)

    def save(self):
        self.can.showPage()
        self.can.save()
        return self.filename
