import numpy as np
import logging
from sys import gettrace
from defusedxml.common import EntitiesForbidden
from openpyxl import load_workbook
from openpyxl import DEFUSEDXML
import zipfile
from pdf2image import convert_from_path
from pdf2image.exceptions import PopplerNotInstalledError
from os import path

"""
This module contains several types of "helper functions" :
- nicelevels: devides a range of value into a set of well-chosen levels for graphics (e.g. axis)
- logging functions mostly aimed at facilitating the reporting of errors into the web interface
- opening xml files safely using defusexml and also checking the uncompressed size.
- relatively basic 'cleaning' of strings from input data prior to use
- higher level functions to facilitate the drawing of strings in Reportlab's canevas

05/2020: The logging part is adapted from an earlier version of the code, and may not be fully appropriate
and/or well structured. It works and remains needed here, but may change substantially or be removed in the future.
"""

# For protect against XML bombs, defusedxml must be installed; it will then be used automatically by openpyxl.
# https://pypi.org/project/defusedxml/
if not DEFUSEDXML:
    logging.warning("Defusedxml does not work! It is probably missing from your installation.")


def nicelevels(vmin, vmax, nalevels=5, nmticks=None, enclose=False):
    """
    Finds a nice value for the step to devide a range of values in nice levels, given constraints

    :param vmin: minimum value to be represented
    :param vmax: max value to be represented
    :param nalevels: approximative numbers of desired levels (divisions) between min and max
    :param nmticks: number of minor ticks; default is no minor ticks, 0 means auto selection
    :param enclose: whether the levels should enclose the range or be within the range (default)
    :return: levels = selected levels so that intervals are [ 5., 2.5, 2.0, 1. ]  *  1.E exponent
             labfmt = formatting string for the axis labels
             mticks = suggested number of minor tick marks between two main tick marks
    """

    #  Possible values for auto-set step between levels and corresponding prefered number of minor ticks:
    #   -first element of each tuple is the step (significand part, decreasing order),
    #   -second element is the number of minor ticks
    aticks = [(5.0, 5.0), (2.5, 5.0), (2.0, 4.0), (1.0, 5.0)]
    #
    nalevels = max(3, nalevels)

    #  First approximation of the step :
    astep = (vmax - vmin) / (float(nalevels - 1) * 0.8)
    if np.abs(astep) <= 1.E-30:
        astep = 1.E-30

    #  Exponent:
    estep = np.floor(np.log10(astep) + 99.) - 99.
    #  Significand part of the step (mantissa, see https://en.wikipedia.org/wiki/Significand):
    mastep = astep / 10 ** estep
    #  Step selection:
    mstep, mticks = [tick for tick in aticks if tick[0] <= mastep][0]
    stp = (10 ** estep) * mstep  # interval between main ticks
    if nmticks is None:
        mstp = stp
    else:
        if nmticks == 0:
            mstp = stp / mticks  # interval between minor ticks
        else:
            mstp = stp / nmticks
    #
    #  Formatting string for labels
    #  Potential strings:
    lab = ["{:.6f}", "{:.5f}", "{:.4}", "{:.3f}", "{:.2f}", "{:.1f}", "{:.0f}"]
    ilab = int(round(estep))
    if (ilab <= 5) and (ilab > 0):
        labfmt = "{:.0f}"
    elif (ilab >= -5) and (ilab <= 0):
        labfmt = lab[ilab + 6 - (mstep == 2.5)]
    else:
        labfmt = "{:.2e}"

    # Generate levels (main ticks)
    op = np.floor if enclose else np.ceil
    newmin = op(vmin / stp) * stp
    nlevels = np.ceil((vmax - newmin + stp * 0.01) / stp) + enclose
    nlevels = max(2, nlevels)
    levels = np.arange(nlevels) * stp + newmin

    # Generate minor ticks
    if nmticks is None:
        mticks = None
    else:
        mtmin = np.ceil((min(vmin, newmin))/mstp) * mstp  # first minor tick
        tmticks = np.ceil((vmax - mtmin + mstp * 0.01) / mstp)  # total number of ticks (minor+main)
        # Get minor ticks as all ticks - main ticks (remove tick if = main tick)
        mticks = [tick for tick in np.arange(tmticks) * mstp + mtmin if tick % stp != 0.0]

    return levels, labfmt, mticks


logmes = {}


def addlogmes(mes, mestype=None):
    """
    This is perhaps temporary: DIY logging for web feedback
    Studying the logging class could perhaps help designing something better & more standard?
    This was designed for the previous version, which worked with mod_python.
    """
    global logmes
    logging.debug(mes)

    mes = rembrackets(mes)
    if mestype == 'title':
        mes = '<h4>' + mes + '</h4>'
    elif mestype == 'subtitle':
        mes = '<h5>' + mes + '</h5>'
    else:
        mes = '<p class="compact indent">' + mes + '</p>'
    logmes["full"].append(mes)


def addlogwarn(mes, critical=False):
    """
    Warning message
    """
    global logmes
    if critical:
        logging.critical(mes)
        logmes["critical"].append(rembrackets(mes))
    else:
        logging.warning(mes)
        logmes["warning"].append(rembrackets(mes))
    mes = '<p class="compact">' + mes + '</p>'
    logmes["full"].append(mes)


def addlogfail(mes):
    """
    Log message as fatal error and return it to raise exception
    """
    global logmes
    mes = "FATAL ERROR: " + mes
    logging.critical(mes)
    outmes = '<span class="error">' + rembrackets(mes) + '</span>'
    logmes["full"].append(outmes)
    logmes["critical"].append(rembrackets(mes))
    return mes


def startlog():
    global logmes
    if gettrace():
        logging.basicConfig(level=logging.DEBUG)
    logmes = {"full": [], "warning": [], "critical": []}


def getlog(level):
    global logmes
    try:
        mes = logmes[level]
    except (KeyError, NameError):
        mes = ['The logging facility failed or did not start!']
    return mes


def rembrackets(instr):
    # This was mostly useful when the code run with mod_python,
    # as Flask probably does it by default. Consider removing.
    return str(instr).replace('<', '&lt;').replace('>', '&gt;')


def secure_open_workbook(file, maxsize=8E6):
    # Attempt at protecting against a real or poential (?) zip bomb:
    # (is it really needed? not sure - see here: https://bugs.python.org/issue36260`

    try:
        with zipfile.ZipFile(file) as zf:
            if sum(zi.file_size for zi in zf.infolist()) > maxsize:
                raise Exception('Excel file appears too large for reading; please contact app managers')
    except zipfile.BadZipFile:
        raise ValueError('Excel file appears invalid [Z]')

    try:
        return load_workbook(file, read_only=True, data_only=True)
    except EntitiesForbidden:
        raise ValueError('Excel file appears invalid [L]')


def isempty(value):
    """
    Finds if a variable is "empty", whatever the type and including strings containing blanks
    :param value: the data to be checked
    :return: whether the input value is judged 'empty'
    """
    if value is None or (hasattr(value, "__getitem__") and len(value) == 0):
        return True
    if isinstance(value, str):
        if not value.strip():
            return True
    return False


def hasindex(lst, index):
    """
    Returns True if lst is a list, and lst(index) exists and contains something (including 0 and '')
    :param lst:
    :param index:
    :return:
    """
    return isinstance(lst, list) and index < len(lst) and (lst[index] is not None)


def stripped(value, default=None):
    """
    Remove blanks if the value is a string, don't touch if it is not a string,
    except if it is None: in that case replace by the default value when provided.
    :param value: the string to be processed
    :param default: to be returned if value is None
    :return: the 'stripped' string
    """
    if isinstance(value, str):
        return value.strip()
    elif value is None and default is not None:
        return default
    else:
        return value


def norm(value):
    """
    Convert to a string if needed, then "normalize" to help with comparisons:
    remove the blanks at both ends and make lower case.
    Works on scalars and lists. Does not touch values which are not strings, including None

    :param value: the value or list of values to be processed
    :return: the 'normalised' string
    """
    if isinstance(value, list):
        return [str(el).strip().lower() if isinstance(el, str) else el for el in value]
    else:
        return str(value).strip().lower() if isinstance(value, str) else value


def htmlbreaks(value):
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")

def rasterize(infilepath, outfilext, fmt='png', width=800, dpi=200, jpegopt=None, cairo=True):
    """
    Converts PDF files to image formats through pdf2image.

    :param infilepath:
    :param outfilext:
    :param fmt:
    :param width:
    :param dpi:
    :param jpegopt:
    :param cairo:
    :return:
    """
    output_folder = path.dirname(infilepath)
    output_file = path.splitext(outfilext)[0]
    outpath = None
    if width:
        size = (width, None)
    else:
        size = None
    try:
        if convert_from_path(infilepath, output_folder=output_folder, single_file=True,
                             output_file=output_file, fmt=fmt, size=size, dpi=dpi, jpegopt=jpegopt,
                             use_pdftocairo=cairo):
            outpath = path.join(output_folder, outfilext)
        else:
            addlogwarn("Conversion from PDF to image failed (did not get image).")
            outpath = None  # No image was produced
    except PopplerNotInstalledError:
        addlogwarn("To convert diagrams to image formats other than PDF, you need to install Poppler.")
    except RuntimeError:
        addlogwarn("Conversion from PDF to image failed.")

    return outpath


def getpath_defaults():
    return path.join(path.dirname(__file__), "defaults/")
