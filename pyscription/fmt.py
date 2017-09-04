from __future__ import (
    absolute_import, division, print_function, with_statement,
)

import sys

from . import util

none = util.identity

def surround(prefix, suffix, *fmts):
    fmt = util.compose(*fmts)
    prefix = fmt(prefix)
    suffix = fmt(suffix)
    return lambda text: prefix + text + suffix

def prefix(prefix, *fmts):
    prefix = util.compose(*fmts)(prefix)
    return lambda text: prefix + text

def suffix(suffix, *fmts):
    suffix = util.compose(*fmts)(suffix)
    return lambda text: text + suffix

# From PEP 257
# https://www.python.org/dev/peps/pep-0257/
def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

class ANSIEscape(util.Namespace):
    reset = end = '\033[0m'

    bright = '\033[1m'
    underline = '\033[4m'
    stop_underline = '\033[24m'
    reverse_video = '\033[7m'
    stop_reverse_video = '\033[27m'
    strikethrough = '\033[9m'

    black = dark = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    purple = pink = '\033[35m'
    cyan = '\033[36m'
    white = light = '\033[37m'

    intense_black = intense_dark = '\033[90m'
    intense_red = '\033[91m'
    intense_green = '\033[92m'
    intense_yellow = '\033[93m'
    intense_blue = '\033[94m'
    intense_purple = intense_pink = '\033[95m'
    intense_cyan = '\033[96m'
    intense_white = intense_light = '\033[97m'

    black_background = dark_background = '\033[40m'
    red_background = '\033[41m'
    green_background = '\033[42m'
    yellow_background = '\033[43m'
    blue_background = '\033[44m'
    purple_background = pink_background = '\033[45m'
    cyan_background = '\033[46m'
    white_background = light_background = '\033[47m'

bright = bold = surround(ANSIEscape.bright, ANSIEscape.reset)
underline = surround(ANSIEscape.underline, ANSIEscape.reset)
fill = surround(ANSIEscape.reverse_video, ANSIEscape.reset)
strikethrough = surround(ANSIEscape.strikethrough, ANSIEscape.reset)

# These opinionated default choices are the high-intensity escapes
# except for green, because high-intensity green is sometimes too similar
# to high-intensity yellow.
red = surround(ANSIEscape.intense_red, ANSIEscape.reset)
green = surround(ANSIEscape.green, ANSIEscape.reset)
yellow = surround(ANSIEscape.intense_yellow, ANSIEscape.reset)
blue = surround(ANSIEscape.intense_blue, ANSIEscape.reset)
purple = surround(ANSIEscape.intense_purple, ANSIEscape.reset)
cyan = surround(ANSIEscape.intense_cyan, ANSIEscape.reset)

black = surround(ANSIEscape.black, ANSIEscape.reset)
off_black = surround(ANSIEscape.intense_black, ANSIEscape.reset)
white  = surround(ANSIEscape.white, ANSIEscape.reset)
off_white = surround(ANSIEscape.intense_white, ANSIEscape.reset)
