import re
import math
import datetime
from jinja2 import filters as flt


import re
import math
import datetime

from blended.sets import intersection, union,\
     symmetric_difference, complement, cartisan_product
from blended.colormap import color_map
from blended._compat import string_types
from blended.trimfloat import trimfloat, trimint
HEX_COLOR_RE = re.compile(r'^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$')
HEX_COLOR_RE_WITHOUT_HASH = re.compile(r'^([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$')

def float_range(start, end=None, increment=None):
    """Take float and integer value as input argument and return range.
    work same as python range.
    """
    if end is None and increment is None:
        return range(int(start))
    elif increment is None:
        return range(int(start), int(end))
    else:
        return range(int(start), int(end), int(increment))

def cycle(array, index):
    """
    """
    length = len(array)
    return array[int(index) % length]

def first(list_obj):
    """returns the first element in the list passed in"""
    if len(list_obj) > 0:
        return list_obj[0]
    return None

def last(list_obj):
    """returns the last element in the list passed in"""
    length = len(list_obj)
    if length > 0:
        return list_obj[-1]
    return None

def join(list1, separator=''):
    """
    Concatenates all the string elements in the list.
    If arg2 is passed in, the elements are separated by that string.
    """
    separator = str(separator)
    try:
        str_var = separator.join(str(val) for val in list1)
    except TypeError:
        return "list content non string object"
    return str_var

def concat(list1, list2):
    """
    takes 2 lists and joins them together.
    returns the result
    """
    return list1 + list2

def length(value):
    """returns length of string or number of items in list"""
    if isinstance(value, (list, str)):
        length = len(value)
    elif isinstance(value, (int, float)):
        val = str(value)
        length = len(val)
    if length:
        return length
    return None

def lower(arg):
    """converts string passed in to all lower case and returns result"""
    try:
        arg = str(arg)
    except TypeError:
        return "argument in lower function must be string, int or float"
    if isinstance(arg, str):
        return arg.lower()
    return None

def upper(arg):
    """converts string passed in to all upper case and returns result"""
    try:
        arg = str(arg)
    except TypeError:
        return "argument in upper function must be string, int or float"
    if isinstance(arg, str):
        return arg.upper()
    return None

def title(arg):
    """Converts string passed in to title case and returns result"""
    try:
        arg = str(arg)
    except TypeError:
        return "argument in title function must be string, int or float"
    if isinstance(arg, str):
        return arg.title()
    return None

def blendedround(number, precision=0):
    """rounds a number to the nearest whole number"""
    if isinstance(number, str):
        return trimfloat(round(float(number), precision))
    if isinstance(number, int):
        return trimint(round(number, precision))     # include trimint
    else:
        return trimfloat(round(number, precision))   # include trimfloat 
    

def ceil(value):
    """Rounds the value up to the nearest int."""
    if not isinstance(value, float):
        value = float(value)
    if isinstance(value, float):
        return math.ceil(value)
    return None

def floor(value):
    """Rounds down to the next lowest integer."""
    if not isinstance(value, float):
        value = float(value)
    if isinstance(value, float):
        return math.floor(value)
    return None

def mean(values):
    """Return mean of the given values.
    """
    return float(sum(values) / len(values) if len(values) > 0 else None)

def rgbcolor(colorvalue):
    """
    This function takes a hex color and
    returns a list with 3 ints representing the rgb numbers
    """
    if isinstance(colorvalue, (list, tuple)) and len(colorvalue) > 3:
        return [0, 0, 0]
    if isinstance(colorvalue, (list, tuple)) and len(colorvalue) == 3:
        col_r = int(colorvalue[0])
        col_g = int(colorvalue[1])
        col_b = int(colorvalue[2])
        if ((col_r <= 255 and col_r >= 0)
                and (col_g <= 255 and col_g >= 0)
                and (col_b <= 255 and col_b >= 0)):
            return [col_r, col_g, col_b]
        else:
            return [0, 0, 0]
    elif isinstance(colorvalue, string_types):
        if colorvalue.startswith('#'):
            normalisevalue = normalize_hex(colorvalue)
            value = normalisevalue.lstrip('#')
        else:
            hexvalue = name_to_hex(colorvalue)
            value = hexvalue.lstrip('#')
        length_value = len(value)
        try:
            if length_value == 1:
                return_value = int(value, 16)*17
                col = return_value, return_value, return_value
                return list(col)
            if length_value == 3:
                return list(int(value[i:i+1], 16)*17 for i in range(0, 3))
            length_value2 = int(length_value/3)
            return list(int(value[i:i+length_value2], 16) for i in range(0, length_value, length_value2))
        except ValueError:
            return [0, 0, 0]

def hexcolor(colorvalue):
    """
    takes a list of 3 ints and returns string representing Hex value
    """
    if isinstance(colorvalue, (list, tuple)) and len(colorvalue) > 3:
        return "#000000"
    if isinstance(colorvalue, (list, tuple)) and len(colorvalue) == 3:
        col_r = int(colorvalue[0])
        col_g = int(colorvalue[1])
        col_b = int(colorvalue[2])
        if ((col_r <= 255 and col_r >= 0)
                and (col_g <= 255 and col_g >= 0)
                and (col_b <= 255 and col_b >= 0)):
            return '#%02X%02X%02X' % (col_r, col_g, col_b)
        else:
            return "#000000"
    elif isinstance(colorvalue, string_types) and colorvalue.startswith('#'):
        hexvalue = normalize_hex(colorvalue)
        return hexvalue
    elif isinstance(colorvalue, string_types):
        hexvalue = name_to_hex(colorvalue)
        return hexvalue

def normalize_hex(hex_value):
    """
    Normalize a hexadecimal color value to 6 digits, lowercase.
    """
    if hex_value.startswith('#'):
        match = HEX_COLOR_RE.match(hex_value)
    else:
        match = HEX_COLOR_RE_WITHOUT_HASH.match(hex_value)
    if match is None:
        return "#000000"
    hex_digits = match.group(1)
    if len(hex_digits) == 3:
        hex_digits = ''.join(2 * s for s in hex_digits)
    return '#%s' % hex_digits.upper()

def name_to_hex(name):
    """
    Convert a color name to a normalized hexadecimal color value.
    When no color of that name exists in the color_map,
    ``ValueError`` is raised.
    """
    normalized = name.lower()
    hex_value = color_map.get(normalized)
    if hex_value is None:
        return normalize_hex(name)
    hexvalue = hex_value.upper()
    return hexvalue

def series(start, length, increment=None):
    """returns a range from a given start value upto the given length,
    with an optional argument 'increment'.
    """
    arr = []
    if not increment:
        increment = 1
    i = start
    while length > 0:
        arr.append(i)
        i += increment
        length -= 1
    return arr

def now():
    """
    Return a datetime object for the current time of the day
    """
    return datetime.datetime.now()


def builtins(request=None):
    """
    return builtin fucitons
    """
    return {
        'range':float_range,
        'cycle':cycle,
        'first':first,
        'last':last,
        'join':join,
        'concat':concat,
        'length':length,
        'lower':lower,
        'upper':upper,
        'title':title,
        'round':blendedround,
        'ceil':ceil,
        'floor':floor,
        'mean':mean,
        'hexcolor':hexcolor,
        'rgbcolor':rgbcolor,
        'product':cartisan_product,
        'union':union,
        'complement':complement,
        'difference':symmetric_difference,
        'intersection':intersection,
        'series':series,
        'now':now,
    }
