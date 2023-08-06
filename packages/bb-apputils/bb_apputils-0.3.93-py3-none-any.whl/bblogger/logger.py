import sys, logging, os, re
from datetime import ( datetime as dt,
                       timedelta as td )
from os.path import ( isabs,
                      isdir,
                      isfile,
                      join as JN,
                      basename as BN,
                      dirname as DN,
                      expanduser as HOME,
                      splitext  )
from os import ( getcwd as pwd,
                 listdir as ls )

from .texttools import getColor

# logger options
APPNAME    = 'BB-Logger'
LEVEL      = logging.WARNING
ROOTLEVEL  = logging.DEBUG
# stream handler options
CONSOLE       = True
CONSOLEFORMAT = 'basic'
COLOR         = True
# file handler options
FILEFORMAT = 'html'
FILEPATH   = None
WRITEMODE  = 'a'
FILELEVEL  = logging.DEBUG

class BBFormatter(logging.Formatter):
    """
    BBFormatter - Color logging output with ansi or html

        mode = 'basic' (console)
                Basic logging for end user messages

               'debug' (console)
                More output information for debugging

               'html' (file)
                Uses html format to color logs to send to an html file or gui
                program that supports html formatting

               'plaintext' (file)
                No escapes inserted for logging plaintext to a file

        A lot of information on colored logging here:
     - https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

        One of my sources for the original credited to the site below:
     - adapted from https://stackoverflow.com/a/56944256/3638629

    """

    def __init__(self, mode='basic', *, colored = True):
        super().__init__()

        _time   = getColor( '#cbe2ce' )   # time
        _num    = getColor( '#FFFFFF' )   # lineno
        _debug  = getColor( '#959cab' )   # debug    ##
        _infoo  = getColor( '#719bcf' )   # info     ##
        _warnn  = getColor( '#d1c92a' )   # warning  ##
        _error  = getColor( '#d46060' )   # error    ##
        _errm   = getColor( '#ddb564' )   # error message text
        _critt  = getColor( '#fc0202',    # critical ##
                            underline = True )
        _msg    = getColor( '#cbe2ce',    # msg
                            italic = True )
        _res    = '\x1b[0m'                 # reset                                        # message  = #5c675e
        __      = f"{_num}.{_res}"          # white dot                                    # debug    = #3b4442
        _time_  = '%(asctime)s'             # TIMESTAMP                                    # info     = #2b3b4f
        _class_ = __name__                  # CLASS                                        # warning  = #8d891c
        _mod_   = '%(module)s'              # MODULE                                       # error    = #4f1b1b
        _name_  = '%(filename)s'                # NAME                                         #    txt   = #cf6d6d
        _func_  = '%(funcName)s'            # FUNCTION                                     # critical = #fc0202
        _num_   = '-%(lineno)s-'            # LINE NO                                      #    txt   = #a33e3e
        _lvl_   = '[%(levelname)s]'
        _msg_   = '%(message)s'

        if mode == 'basic':
            if colored:
                __debug    = f"{_debug}  {_lvl_}{_msg} {_msg_}{_res}"
                __info     = f"{_infoo}  {_lvl_}{_msg} {_msg_}{_res}"
                __warning  = f"{_warnn}  {_lvl_}{_msg} {_msg_}{_res}"
                __error    = f"{_error}  {_lvl_}{_msg} {_msg_}{_res}"
                __critical = f"{_critt}  {_lvl_}{_msg} {_msg_}{_res}"
            else:
                __debug = __info = __warning = __error = __critical = f"  {_lvl_} {_msg_}"

        elif mode == 'debug':
            if colored:
                __debug    = f"{_time} {_time_}{_num} {_num_ : ^14}{_debug}{_name_}{__}{_debug}{_func_}{_debug} {_lvl_}:{_msg} {_msg_}{_res}"
                __info     = f"{_time} {_time_}{_num} {_num_ : ^14}{_infoo}{_name_}{__}{_infoo}{_func_}{_infoo} {_lvl_}:{_msg} {_msg_}{_res}"
                __warning  = f"{_time} {_time_}{_num} {_num_ : ^14}{_warnn}{_name_}{__}{_warnn}{_func_}{_warnn} {_lvl_}:{_msg} {_msg_}{_res}"
                __error    = f"{_time} {_time_}{_num} {_num_ : ^14}{_error}{_name_}{__}{_error}{_func_}{_error} {_lvl_}:{_errm} {_msg_}{_res}"
                __critical = f"{_time} {_time_}{_num} {_num_ : ^14}{_critt}{_name_}{__}{_critt}{_func_}{_critt} {_lvl_}:{_errm} {_msg_}{_res}"

            else:
                __debug = __info = __warning = __error = __critical = f" {_time_} {_num_:^14}{_name_}.{_func_} {_lvl_} {_msg_}"

        elif mode == 'plaintext':
            __debug = __info = __warning = __error = __critical = f"  {_time_} {_num_:^14}{_name_}.{_mod_}.{_func_} {_lvl_}: {_msg_}"

        elif mode == 'html':
            __debug    = ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                   "<span style=\"color: #474f48;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                   "<b>[ %(lineno)d ]</b>", "<span style=\"color: #474f48;\"> %(levelname)s: </span>",
                                   "<span style=\"color: #5c675e; font-style: italic;\">%(message)s</span></p>" ])
            __info     = ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                   "<span style=\"color: #2b3b4f;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                   "<b>[ %(lineno)d ]</b>", "<span style=\"color: #2b3b4f;\"> %(levelname)s: </span>",
                                   "<span style=\"color: #5c675e; font-style: italic;\">%(message)s</span></p>" ])
            __warning  = ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                   "<span style=\"color: #8d891c;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                   "<b>[ %(lineno)d ]</b>", "<span style=\"color: #8d891c;\"> %(levelname)s: </span>",
                                   "<span style=\"color: #5c675e; font-style: italic;\">%(message)s</span></p>" ])
            __error    = ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                   "<span style=\"color: #4f1b1b;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                   "<b>[ %(lineno)d ]</b>", "<span style=\"color: #4f1b1b;\"> %(levelname)s: </span>",
                                   "<span style=\"color: #cf6d6d; font-style: italic;\">%(message)s</span></p>" ])
            __critical = ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                                   "<span style=\"color: #fc0202;\"> %(name)s>%(module)s.%(funcName)s </span>",
                                   "<b>[ %(lineno)d ]</b>", "<span style=\"color: #fc0202;\"> %(levelname)s: </span>",
                                   "<span style=\"color: #a33e3e; font-style: italic;\">%(message)s</span></p>" ])

        else:
            raise SyntaxError(f"Invalid format mode - '{mode}'")

        self.mode    = mode
        self.colored = colored
        self.__crit  = __critical
        self.FORMAT  = { logging.DEBUG    : __debug,
                         logging.INFO     : __info,
                         logging.WARNING  : __warning,
                         logging.ERROR    : __error,
                         logging.CRITICAL : __critical }

    def formatException(self, exc_info):
        if self.mode == 'console':
            return self.__crit + f'\n        {C_R()}> {C__()}' + traceback.print_exception().replace('\n', f'\n        {C_R()}> {C__()}')
        elif self.mode == 'html':
            return ''.join([ "  <p><span style=\"color: #717e73;\">%(asctime)s </span>",
                             "<span style=\"color: #fc0202;\"> %(name)s>%(module)s.%(funcName)s </span>",
                             "<b>[ %(lineno)d ]</b>", "<span style=\"color: #fc0202;\"> %(levelname)s: </span>",
                             "<code>%(message)s</code></p>" ])

    def format(self, record):
        log_fmt = self.FORMAT.get(record.levelno)
        if self.mode == 'basic':
            try:
                width = os.get_terminal_size().columns
            except:
                width = 200
            msg = record.getMessage()
            if len(msg) + len(record.levelname) + 21 > width:
                length = len(record.levelname) + 5
                words, msg_lines, indent = msg.split(), [''], f"{'    ':.<{length - 4}}"
                while words:
                    if len(words[0]) + length + 2 > width:
                        if len(msg_lines[-1]) < int(width*.7):
                            left = width - len(msg_lines[-1]) - 2
                            split_word = words.pop(0)
                            word = split_word[:left]
                            msg_lines[-1] += f" {word}"
                            msg_lines.append( f"{indent}" )
                            words.insert( 0, split_word[left:] )
                        else:
                            msg_lines.append( f"{indent}"

                        length = len(msg_lines[-1])

                    else:
                        word = f" {words.pop(0)}"
                        length += len(word)
                        msg_lines[-1] += word

                    if not words and length + 15 > width:
                        msg_lines.append( f"{indent}" )
                        length = len(msg_lines[-1])

                space = width - length - 14
                if space > 0:
                    msg_lines[-1] += f"{'':.<{space}}"

                record.msg = '\n'.join(msg_lines)

            else:
                space = width - 21 - len(record.levelname) - ( len(msg) - ( int(len(msg) / width) * width ))

            log_fmt = f"{log_fmt}  {' ':.>{space}}"+"-\x1b[1;37m"+" %(asctime)s"+"\x1b[0m"
            formatter = logging.Formatter(log_fmt, '[%R:%S]')

        elif self.mode == 'debug':
            formatter = logging.Formatter(log_fmt, '[%R:%S]')

        elif self.mode == 'html' or self.mode == 'plaintext':
            formatter = logging.Formatter(log_fmt, '%a, %m/%d/%y [%R:%S]:')

        return formatter.format(record)

class BBLogger(logging.getLoggerClass()):
    """
    Console and file logging, formatted with BBFormatter
        - options are set through logger.getLogger() with initial call
        - subsequent loggers should be called with python's logging
          module: logging.getLogger()
    """

    def __init__(self, name):
        global APPNAME
        global LEVEL
        global CONSOLE
        global CONSOLEFORMAT
        global COLOR
        global FILEPATH
        global FILELEVEL
        global FILEFORMAT
        global WRITEMODE
        global ROOTLEVEL
        self.root.setLevel( logging.DEBUG )

        super().__init__( APPNAME, level = 1 )
        self.propagate = False
        self.setLevel( ROOTLEVEL )

        if CONSOLE:
            hdlr = logging.StreamHandler( sys.stdout )
            hdlr.setFormatter( BBFormatter( mode = CONSOLEFORMAT,
                                            colored = COLOR ))
            hdlr.setLevel( LEVEL )
            self.addHandler( hdlr )

        if FILEPATH:
            errors = []
            if FILEFORMAT == 'html':
                lm = "<span style=\"color: darkcyan\"><br># BBLogger logging module</span><br>"
            else:
                lm = "\n# BBLogger logging module\n\n"

            try:
                if not isfile(FILEPATH):
                    with open( FILEPATH, 'w' ) as f:
                        f.write(lm)
                else:
                    assert os.access( FILEPATH, os.W_OK ) and os.access( FILEPATH, os.R_OK )

            except:
                raise PermissionError( f"User doesn't have read/write access to '{FILEPATH}'" )

            if FILEFORMAT == 'html' and ( len(splitext( FILEPATH )) < 2 or splitext( FILEPATH )[1] != '.html' ):
                FILEPATH = f"{splitext(FILEPATH)[0]}.html"

            fhdlr = logging.FileHandler( FILEPATH, mode = WRITEMODE, encoding = 'utf-8' )
            fhdlr.setFormatter( BBFormatter( mode = FILEFORMAT ))
            fhdlr.setLevel( FILELEVEL )

            self.addHandler( fhdlr )

        self.set_level

    def set_level(self, level = None):
        """
        Sets level for current and all other console loggers
            - files will always be debugging mode
            - acceptable modes:
                'debug'    | logging.DEBUG    | 10 | 1 <or> 0
                'info'     | logging.INFO     | 20 | 2
                'warning'  | logging.WARNING  | 30 | 3
                'error'    | logging.ERROR    | 40 | 4
                'critical' | logging.CRITICAL | 50 | 5
        """
        if level:
            global LEVEL
            lvl = getLoggingLevel(level)
            LEVEL = lvl

        for i in self.handlers:
            if isinstance( i, logging.FileHandler):
                i.setLevel( FILELEVEL )
            elif isinstance( i, logging.StreamHandler):
                i.setLevel( LEVEL )

    def set_format(self, formatting):
        """
        Change formatting for console logging
            'basic' - simple, nicely formatted messaging
            'debug' - more info pertaining to each message
                      * defaults to log level 1
        """
        if formatting not in ( 'basic', 'debug' ):
            raise SyntaxError(f"Invalid formatting option - '{formatting}'")

        if logging.StreamHandler not in [ type(i) for i in self.handlers ]:
            self.warning( "Missing StreamHandler - skipping set formatting" )
            return
        for i in self.handlers:
            if not isinstance( i, logging.FileHandler ):
                i.setFormatter( BBFormatter( mode = formatting ))
                if formatting == 'debug':
                    i.setLevel( logging.DEBUG )

def getLogger( name, level = 1, **opts ):
    """
    Set custom logger class and return logger
      - only use this for initial call to logger. Use logging.getLogger() for
        further logging modules

        'name'    = Name of returned logger
        'level'   = Log level for the returned logger. Defaults to 1.

        **opts:
              More options for logger. To print the log to a file, 'filepath'
            must be present in the opts.

            'appname'      : [ DEFAULT 'BB-Logger' ] Application name
            'console'      : [ DEFAULT = True ] Print logging to console
            'consoleformat': [ DEFAULT = 'basic' ] Console formatting. Options are
                                'basic' or 'debug'.
            'color'        : [ DEFAULT = True ] colorized console logging
            'filepath'     : [ DEFAULT None ] The path for the file to be written to.
                                The directory for the file must exist. If the file
                                exists and write_mode 'w' is used, log file will be
                                overwritten.
            'write_mode'   : [ DEFAULT = 'a'] Write mode - ('a', 'append', 'w', 'write')
            'filelevel'    : [ DEFAULT = 1 ] Set log level for file. Default is 1, DEBUGGING
                                - must be set with initial call to logger.getLogger()
            'rootlevel'    : [ DEFAULT = 1 ] Set the root logger level
                                - usually best to keep this default
            'fileformat'   : [ DEFAULT = 'html' ] Text formatting for file - 'plaintext'
                                or 'html'

              A new file will be created if not existing as long as the directory
            already exists. If only a filename is given for 'path', the file will
            be written in the user's HOME folder. Extra options should only need
            applied for the first time initiating a logger in your app/script unless
            logfile changes are wanted for a particular logger. The 'color' option
            only applies to console output.
    """
    global APPNAME
    global LEVEL
    global CONSOLE
    global CONSOLEFORMAT
    global COLOR
    global FILEPATH
    global FILELEVEL
    global FILEFORMAT
    global WRITEMODE
    global ROOTLEVEL

    LEVEL   = getLoggingLevel( level )

    try:
        if 'rootlevel' in opts:
            ROOTLEVEL = getLoggingLevel( opts['rootlogger'] )

        if 'appname' in opts:
            APPNAME = opts['appname']

        if 'console' in opts:
            if not isinstance( opts['console'], bool ):
                raise TypeError("Expected boolean for 'console' option")
            CONSOLE = opts['console']

        if 'consoleformat' in opts:
            if opts['consoleformat'] not in ( 'basic', 'debug' ):
                raise TypeError(f"Invalid console format - '{opts['consoleformat']}'")
            CONSOLEFORMAT = opts['consoleformat']

        if 'color' in opts:
            if not isinstance( opts['color'], bool ):
                raise TypeError("Expected boolean for 'color' option")
            COLOR = opts['color']

        if 'filepath' in opts:
            if not isdir( DN( opts['filepath'] )):
                raise FileNotFoundError(f"Directory doesn't exist - '{DN(opts['filepath'])}'")
            FILEPATH = opts['filepath']

        if 'filelevel' in opts:
            FILELEVEL = getLoggingLevel( opts['filelevel'] )

        if 'fileformat' in opts:
            if opts['fileformat'] not in ( 'plaintext', 'html' ):
                raise ValueError(f"Invalid file format - '{opt['fileformat']}'")
            FILEFORMAT = opts['fileformat']

        if 'write_mode' in opts:
            if opts['write_mode'] in ( 'a', 'append' ):
                WRITEMODE = 'a'
            elif opts['write_mode'] in ( 'w', 'write' ):
                WRITEMODE = 'w'
            else:
                raise ValueError("Invalid file write mode - expected one of ('a', 'append', 'w', 'write')")

    except Exception as E:
        sys.stderr.write(str(E))
        raise SyntaxError("Invalid arguments")

    logging.setLoggerClass( BBLogger )
    logger = BBLogger(APPNAME)

    return logger

def getLoggingLevel(L):
    """
    Translate verbosity from level argument
    """
    verbosity = { 0: logging.DEBUG,
                  1: logging.DEBUG,
                  2: logging.INFO,
                  3: logging.WARNING,
                  4: logging.ERROR,
                  5: logging.CRITICAL }

    if L in [ v for k, v in verbosity.items() ]:
        return L

    elif isinstance( L, int ) or ( isinstance( L, str ) and L.isnumeric() ):
        L = int(L)
        if L in ( 10, 20, 30, 40, 50 ):
            L = int( str(L)[0] )
            return verbosity[L]
        elif L > 5:
            log.warning(f"Invalid verbosity level '{L}' - setting to 5")
            return verbosity[5]
        elif L < 1:
            log.warning(f"Invalid verbosity level '{L}' - setting to 1")
            return verbosity[1]
        else:
            return verbosity[L]

    else:
        l = L.lower()
        if l == 'critical':
            return verbosity[5]
        elif l == 'error':
            return verbosity[4]
        elif l == 'warning':
            return verbosity[3]
        elif l == 'info':
            return verbosity[2]
        elif l == 'debug':
            return verbosity[1]
        else:
            raise ValueError(f"Log level must be an integer (1-5)")
