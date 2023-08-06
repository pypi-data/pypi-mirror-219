# -*- coding: utf-8 -*-
"""
Interface to drawing libraries: starting point
"""
import embermaker.drawinglib.canvas_svg as can_svg
import embermaker.drawinglib.canvas_pdf as can_pdf

def get_canvas(outfile, colorsys="RGB", size=(1,1), grformat="PDF"):
    if grformat == "PDF":
        return can_pdf.CanvasPdf(outfile, colorsys, size)
    elif grformat == "SVG":
        return can_svg.CanvasSvg(outfile, colorsys, size)
    else:
        raise ValueError (f"Unknown file/canvas format: {grformat}")