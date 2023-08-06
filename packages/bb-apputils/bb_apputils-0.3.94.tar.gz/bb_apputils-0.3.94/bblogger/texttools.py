"""
# ANSI escapes for text manipulation

Import and use these to make your python scripts perdy.
All escape codes are returned in octal format.
A few cursor controls are included but you can find
many more with a few duckduckgo searches.
"""

import re
# from bb_logger import getLogger

# log = getLogger(__name__, level = 3)

def __formatting__(func):
    """
    Wrapper for formatting text colors
        bold            - bold text
        italic          - italic text
        underline       - underline text
        strikethrough   - add line through text
        blink           - make text blink
    """
    def __wrapper__( *args, **kwargs ):
        txt = func( *args, **kwargs )
        color = [ txt, 'm' ]

        if 'bold' in kwargs:
            if fmt['bold']:
                color.insert( -1, ';1' )
            else:
                color.insert( -1, ';21' )

        if 'italic' in kwargs:
            if fmt['italic']:
                color.insert( -1, ';3' )
            else:
                color.insert( -1, ';23' )

        if 'underline' in kwargs:
            if fmt['underline']:
                color.insert( -1, ';4' )
            else:
                color.insert( -1, ';24' )

        if 'blink' in kwargs:
            if fmt['blink']:
                color.insert( -1, ';5' )
            else:
                color.insert( -1, ';25' )

        if 'strikethrough' in kwargs:
            if fmt['strikethrough']:
                color.insert( -1, ';5' )
            else:
                color.insert( -1, ';25' )

        return ''.join( color )

    return __wrapper__

@__formatting__
def C_rgb(*args, R = None, G = None, B = None, **kwargs):
    @staticmethod
    def err(e, *args):
        ERR = { 'syn' : SyntaxError("Requires up to 3 integers for rgb value"),
                'type': TypeError("Requires an iterable object"),
                'run' : RuntimeError( args[0] ) }

        raise ERR[e]

    RGB = []

    if args:
        for i in args:
            if hasattr( i, '__iter__' ):
                for I in i:
                    try:
                        if not R:
                            R = int(I)

                        elif not G:
                            G = int(I)

                        elif not B:
                            B = int(I)
                    except:
                        pass
            else:
                try:
                    if not R:
                        R = int(I)

                    elif not G:
                        G = int(I)

                    elif not B:
                        B = int(I)
                except:
                    pass

    if not R and not G and not B:
        rgb = ( '178', '178', '178' )
    else:
        if not R:
            R = 0

        if not G:
            G = 0

        if not B:
            B = 0

        rgb = ( str(i) for i in ( R, G, B ))

    for num, c in zip(rgb, ( 'red', 'green', 'blue' )):
        try:
            assert int(num) <= 255 and int(num) >= 0
        except AssertionError:
            ERR( 'run', f"Expected value of 0-255 for '{c}'" )
        except:
            ERR('syn')

    return '\033[38;2;' + ';'.join(rgb) + 'm'

@__formatting__
def C_hex(HEX, **kwargs):
    """
    Returns an RGB escape code from a hexidecimal code
    """
    h = HEX.lstrip('#')
    return '\033[38;2;' + ';'.join( str(s) for s in tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))

@__formatting__
def C_Bl(*args, **kwargs):
    """ Black """
    return '\x1b[38;2;0;0;0m'

@__formatting__
def C_DB(*args, **kwargs):
    """ Dark Blue """
    return '\x1b[38;2;0;0;160m'

@__formatting__
def C_B(*args, **kwargs):
    """ Blue """
    return '\x1b[38;2;0;0;255m'

@__formatting__
def C_b(*args, **kwargs):
    """ Light Blue """
    return '\x1b[38;2;51;153;255m'

@__formatting__
def C_DC(*args, **kwargs):
    """ Dark Cyan """
    return '\x1b[38;2;0;102;102m'

@__formatting__
def C_C(*args, **kwargs):
    """ Cyan """
    return '\x1b[38;2;0;153;135m'

@__formatting__
def C_c(*args, **kwargs):
    """ Light Cyan """
    return '\x1b[38;2;0;255;255m'

@__formatting__
def C_O(*args, **kwargs):
    """ Orange """
    return '\x1b[38;2;255;128;0m'

@__formatting__
def C_Br(*args, **kwargs):
    """ Brown """
    return '\x1b[38;2;102;51;0m'

@__formatting__
def C_DP(*args, **kwargs):
    """ Dark Purple """
    return '\x1b[38;2;51;0;102m'

@__formatting__
def C_P(*args, **kwargs):
    """ Purple """
    return '\x1b[38;2;102;0;204m'

@__formatting__
def C_p(*args, **kwargs):
    """ Light Purple """
    return '\x1b[38;2;178;102;255m'

@__formatting__
def C_M(*args, **kwargs):
    """ Magenta """
    return '\x1b[38;2;204;0;204m'

@__formatting__
def C_pi(*args, **kwargs):
    """ Pink """
    return '\x1b[38;2;255;102;255m'

@__formatting__
def C_DR(*args, **kwargs):
    """ Dark Red """
    return '\x1b[38;2;153;0;0m'

@__formatting__
def C_R(*args, **kwargs):
    """ Red """
    return '\x1b[38;2;204;0;0m'

@__formatting__
def C_r(*args, **kwargs):
    """ Light Red """
    return '\x1b[38;2;255;102;102m'

@__formatting__
def C_W(*args, **kwargs):
    """ White """
    return '\x1b[38;2;255;255;255m'

@__formatting__
def C_DGr(*args, **kwargs):
    """ Dark Gray """
    return '\x1b[38;2;96;96;96m'

@__formatting__
def C_Gr(*args, **kwargs):
    """ Gray """
    return '\x1b[38;2;160;160;160m'

@__formatting__
def C_gr(*args, **kwargs):
    """ Light Gray """
    return '\x1b[38;2;224;224;224m'

@__formatting__
def C_DG(*args, **kwargs):
    """ Dark Green """
    return '\x1b[38;2;0;102;0m'

@__formatting__
def C_G(*args, **kwargs):
    """ Green """
    return '\x1b[38;2;0;153;0m'

@__formatting__
def C_g(*args, **kwargs):
    """ Light Green """
    return '\x1b[38;2;102;255;102m'

@__formatting__
def C_Y(*args, **kwargs):
    """ Yellow """
    return '\x1b[38;2;255;255;0m'

@__formatting__
def C_Go(*args, **kwargs):
    """ Gold """
    return '\x1b[38;2;204;204;0m'

def F_B():
    """ Bold """
    return '\x1b[1m'

def F__B():
    """ Remove Bold """
    return '\x1b[21m'

def F_I():
    """ Italic """
    return '\x1b[3m'

def F__I():
    """ Remove Italic """
    return '\x1b[23m'

def F_S():
    """ Strikethrough """
    return '\x1b[9m'

def F__S():
    """ Remove Strikethrough """
    return '\x1b[29m'

def F_U():
    """ Underline """
    return '\x1b[4m'

def F__U():
    """ Remove Underline """
    return '\x1b[24m'

def C__():
    """ Reset Text Formatting """
    return '\x1b[0m'

def c_UP(n=1):
    """
     Cursor Up
     n = Number of lines
    """
    return f'\x1b[{n}A'

def c_DOWN(n=1):
    """
     Cursor Down
     n = Number of lines
    """
    return f'\x1b[{n}B'

def c_RIGHT(n=1):
    """
     Cursor Right
     n = Number of columns
    """
    return f'\x1b[{n}C'

def c_LEFT(n=1):
    """
     Cursor Left
     n = Number of columns
    """
    return f'\x1b[{n}D'

def c_COL(n=1):
    """
     Cursor To Column
     n = column number
    """
    return f'\x1b[{n}G'

def c_CLEAR(n=1):
    """
     Clear
     n = 1 - current line   [default]
     n = 2 - left of cursor
     n = 3 - right of cursor
     n = 4 - screen
    """
    if n == 1:
        return '\x1b[K'
    elif n == 2:
        return '\x1b[1K'
    elif n == 3:
        return '\x1b[0K'
    elif n == 4:
        return '\x1b[2J'

def c_HIDE():
    """ Cursor Invisible """
    return '\x1b[?25l'

def c_SHOW():
    """ Cursor Visible """
    return '\x1b[?25h'

def cprint( *args,
            blink = False,
            bold = False,
            end = '\n',
            italic = False,
            finish = '\x1b[0m',
            noprint = False,
            strikethrough = False,
            underline = False ):

    color, string, rgb = [], None, []
    for arg in args:
        if hasattr( arg, '__call__' ):
            try:
                assert not color and not rgb
            except:
                raise SyntaxError("Only one color method should be defined")

            try:
                c = arg(_skip_formatting = True)
                assert isinstance( c, str )
                color += [ c.strip('m'), 'm' ]
                del c
            except:
                raise RuntimeError("Invalid method provided - expected a returned string")

        elif isinstance( arg, str ):
            if re.match( '^(#){1}[a-fA-F0-9]{6}$', arg ):
                try:
                    assert not color and not rgb
                except:
                    raise SyntaxError("Only one color method should be defined")

                color += [ C_hex(arg).strip('m'), 'm' ]

            elif byColorName( arg ) and not color:
                color += [ byColorName( arg ).strip('m'), 'm' ]

            else:
                try:
                    assert not string
                    string = arg
                except:
                    string += '\n' + arg

        elif isinstance( arg, int ):
            try:
                assert not color
            except:
                raise SyntaxError("Only one color method can be used")

            try:
                assert len( rgb ) < 3
            except:
                raise SyntaxError("Only 3 rgb values should be defined")

            rgb.append(arg)

    if not noprint:
        if not string:
            raise SyntaxError("No string to print")

        if not finish:
            fin = ''
        elif hasattr( finish, '__call__' ):
            fin = str(finish())
        else:
            fin = str(finish)

        if not end:
            END = ''
        elif hasattr( end, '__call__' ):
            END = str(end())
        else:
            END = str(end)

    if not color:
        while len(rgb) < 3:
            if len(rgb) == 0:
                rgb = [ 178, 178, 178 ]
                break

            rgb.append(0)

        color += [ C_rgb(rgb).strip('m'), 'm' ]

    if bold:
        color.insert( -1, ';1' )
    else:
        color.insert( -1, ';21' )

    if italic:
        color.insert( -1, ';3' )
    else:
        color.insert( -1, ';23' )

    if underline:
        color.insert( -1, ';4' )
    else:
        color.insert( -1, ';24' )

    if blink:
        color.insert( -1, ';5' )
    else:
        color.insert( -1, ';25' )

    if strikethrough:
        color.insert( -1, ';5' )
    else:
        color.insert( -1, ';25' )

    if noprint:
        return ''.join( color )

    print( ''.join( color ) + string + fin, end = end )

def byColorName(str_ = None):
    COLORS = { 'Black'          : C_Bl,
               'Dark Gray'      : C_DG,
               'Gray'           : C_Gr,
               'Light Gray'     : C_gr,
               'Light Red'      : C_r,
               'Red'            : C_R,
               'Dark Red'       : C_DR,
               'Brown'          : C_Br,
               'Orange'         : C_O,
               'Gold'           : C_Go,
               'Yellow'         : C_Y,
               'Light Green'    : C_g,
               'Green'          : C_G,
               'Dark Green'     : C_DGr,
               'Dark Cyan'      : C_DC,
               'Cyan'           : C_C,
               'Light Cyan'     : C_c,
               'Light Blue'     : C_b,
               'Blue'           : C_B,
               'Dark Blue'      : C_DB,
               'Dark Purple'    : C_DP,
               'Purple'         : C_P,
               'Light Purple'   : C_p,
               'Magenta'        : C_M,
               'Pink'           : C_pi,
               'White'          : C_W }

    if not str_:
        return tuple( i for i in COLORS )

    if str_.title() in COLORS:
        return COLORS[str_.title()]()

    return None

def getColor(*args, **kwargs):
    kwargs['noprint'] = True
    return cprint(*args, **kwargs)

