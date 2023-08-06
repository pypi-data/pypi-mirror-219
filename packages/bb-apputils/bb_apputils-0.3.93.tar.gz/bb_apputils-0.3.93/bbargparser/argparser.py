import re, os
from functools import partial

class ArgParser(dict):
    """
    ArgParser
      - multiple ways to parse options

        opts = list of tuples

        Each option can have as many keywords as wanted. Options are set up in
      a Unix style. No hyphens are necessary when initiating accepted options. In
      fact, they will be stripped from the beginning of each option and reassigned
      appropriately if existing.

        Options are given in a list/tuple. Each accepted option, both short and long
      arguments, are given in the same tuple. Single letter options, short opts, will
      be prepended with a single hyphen '-'. Long options with two hyphens '--'.

        You can specify acceptable options or types as well for each keyword/group of
      keywords. To do this, include '_+_' in the same tuple. Anything following this
      value will symbolize an accepted user argument or argument type. You can specify
      a path, file, or directory with '__path__', '__file__', or '__directory__'. The
      directory or file options will check to make sure that the file or directory exists
      as a file or directory. The path option only checks to make sure that the argument
      is in the proper form of a file path, ignoring whether it exists or not. The file
      path must be an absolute path.

        Another accepted option type is '__count__n', while n is the number of arguments
      required for that option. This is the only "accepted option" that you can combine
      with another type. Anything other than types will not be accepted in combination.
        For example:
            ArgParser( [('i', 'items', '_+_', '__count__3', int)] ) requires 3 arguments
          that are integers for the options '-i', '--items'.

        You can also use regex to define an accepted argument with '__regex__:' with the
      regex string following the colon (':'). Remember to use proper escapes. This option
      uses the built-in re module.

        The last "acceptable option" option is providing a function that returns True or
      False and accepts a single string argument. This option can only be used by itself.

        When specifying the type using the '_+_' value, any other arguments following it
      will be ignored, unless it's '__count__n', in which case anything after that's not
      a type will be ignored. If the user argument given doesn't match the type, a SyntaxError
      exception will be raised, unless the type is '__file__' or '__directory__', in which
      case a FileNotFoundError will be raised. An invalid option passed by the user will
      cause SyntaxError to be raised.

        Example:
            opts = ArgParser( [('i', 'input-file', '_+_', '__file__'),
                               ('o', 'output-file', '_+_', '__path__')] )

            for opt, arg in opts( sys.argv[1:],
                                  ignore_delimiters = True,
                                  set_delimiter = None,
                                  clear = True )

        Options would be set as '-i', '--input-file' and '-o', '--output-file'. The '-i'
      option will only accept an existing file as an argument and the '-o' option will
      accept an argument that matches a path format, regardless of whether it exists. opts(...)
      will return a key, item list from the provided user arguments. The '.items()' function
      should not be used when calling the class with user arguments. If no arguments are given,
      self (dict) is returned. The default is to clear self every time it is called inless 'clear'
      is set to False.

    """
    _optargs = {}
    _names   = {}

    @staticmethod
    def reMatch(_match, opt, *args):
        try:
            for arg in args:
                assert re.match( _match, arg )
        except:
            raise SyntaxError(f"Invalid argument for option '{opt}'")

        return opt, *args

    @staticmethod
    def isIn(_list, opt, *args):
        try:
            for arg in args:
                assert arg in _list
        except:
            raise SyntaxError(f"Invalid argument for option '{opt}'")

        return opt, *args

    @staticmethod
    def isFile(opt, *args):
        try:
            for arg in args:
                assert os.path.isfile(arg)
        except:
            raise FileNotFoundError(f"File '{arg}' doesn't exist")

        return opt, *args

    @staticmethod
    def isDir(opt, *args):
        try:
            for arg in args:
                assert os.path.isdir(arg)
        except:
            raise FileNotFoundError(f"Directory '{arg}' doesn't exist")

        return opt, *args

    @staticmethod
    def isPath(opt, *args):
        try:
            for arg in args:
                assert re.match( f"^({os.path.sep}.+)+", arg )
        except:
            raise SyntaxError(f"Option '{opt}' requires an absolute file path")

    @staticmethod
    def hasCount(count, opt, *args):
        try:
            assert len(args) == count
            return opt, *args
        except:
            raise SyntaxError(f"Option '{opt}' requires {count} arguments")

    @staticmethod
    def isType(_type, opt, *args):
        try:
            for arg in args:
                if _type == int:
                    assert int(arg)
                else:
                    assert isinstance( arg, _type )
        except:
            raise SyntaxError(f"Wrong argument type for option '{opt}'")

    @staticmethod
    def _returnVal(opt, *args):
        return opt, *args

    def __init__(self, *opts):
        _types = { '__path__'     : self.isPath,
                   '__directory__': self.isDir,
                   '__file__'     : self.isFile }
        OPTS = {}
        O = []
        for opt in opts:
            allopt = []
            isSubOpt = False
            _type  = False
            _count = None
            _call = None
            _regex = None
            _accepts = []
            for o in opt:
                if isSubOpt:
                    if not allopt:
                        raise ValueError("Option arguments must come before accepted arguments")

                    if hasattr( o, '__call__' ):
                        if o in ( int, bool, list, dict, tuple ):
                            if _type or _accepts or _call or _regex:
                                raise ValueError("Too many option types")
                            _type = o
                        else:
                            if _type or _accepts or _call or _regex or _count:
                                raise ValueError("Too many option types")
                            _call = o
                            break
                    elif o in ( '__path__', '__file__', '__directory__' ):
                        if _type or _accepts or _call or _regex:
                            raise ValueError("Too many option types")
                        _type = o
                    elif o.startswith('__regex__:'):
                        if _type or _accepts or _call or _regex:
                            raise ValueError("Too many option types")
                        _regex = o.split(':', 1)[1]
                    elif re.match( '^__count__[0-9]+$', o ):
                        _count = int( o[9:] )
                    elif not _type:
                        _accepts.append(o)

                else:
                    while o.startswith('-'):
                        o = o[1:]

                    if not o:
                        raise ValueError("Option can't be blank")
                    elif o == '_+_':
                        isSubOpt = True
                    elif len(o) == 1:
                        allopt.append(f"-{o}")
                    else:
                        allopt.append(f"--{o}")

            O += [':'.join(allopt)]
            OPTS[O[-1]] = []

            if _count:
                OPTS[ O[-1] ] += [ partial( self.hasCount, _count )]
            if _regex:
                OPTS[ O[-1] ] += [ partial( self.reMatch, _regex )]
            elif _call:
                OPTS[ O[-1] ] += [ partial( _call )]
            elif _type:
                if hasattr( _type, '__call__' ):
                    OPTS[ O[-1] ] += [ partial( self.isType, _type )]
                else:
                    OPTS[ O[-1] ] += [ partial( _types[_type] )]
            elif _accepts:
                OPTS[ O[-1] ] += [ partial( self.isIn, _accepts )]

        self._optargs = {}

        _o = []
        for k, v in OPTS.items():
            for opt in k.split(':'):
                if opt in _o:
                    raise KeyError("Same parameter provided more than once")
                _o += [opt]
                self._optargs[ _o[-1] ] = v

        dict.__init__(self)

    def __call__(self, *args, ignore_delimiter = False, set_delimiter = None, clear = True):
        """
        Call to recieve the list of user options and arguments
            ignore_delimiter: By default '=' is used as a delimiter. This prevents
                a single '=' from being used as an argument. Set this to True to
                use '=' as any other character

            set_delimiter: Set the delimiter to a specific value. This overrides
                'ignore_delimiter'

            - these only apply to long options

        """
        if not args:
            return self
        elif clear:
            self.clear()

        if set_delimiter:
            SD = str(set_delimiter)
        elif ignore_delimiter:
            SD = None
        else:
            SD = '='

        A = list(args)
        _a, _o = [], []
        while A:
            if A[0].startswith('-'):
                if _a:
                    if _a[-1] not in self._optargs:
                        raise SyntaxError(f"Invalid option '{_a[-1]}'")

                    for chk in self._optargs[ _a[-1] ]:
                        chk( _a[-1], *_o[-1] )

                    self[ _a[-1] ] = tuple( _o[-1] )

                    _a, _o = [], []

                _a.append( A.pop(0) )
                if _a[-1].startswith('--'):
                    if SD and SD in _a[-1]:
                        _a[-1], o = _a[-1].split(SD, 1)
                        A.insert(0, o)

                _o.append([])

            else:
                if not _a:
                    raise SyntaxError("Must specify an option before a value")

                while A and not A[0].startswith('-'):
                    _o[-1].append( A.pop(0) )

                if not A:
                    assert _a[-1] in self._optargs
                    for chk in self._optargs[ _a[-1] ]:
                        chk( _a[-1], *_o[-1] )

                    self[ _a[-1] ] = tuple( _o[-1] )

        return self.items()

    def setName(self, arg, name):
        """
        Assign an option name
         - provide one option to add the name to every option in the group
         - returns tuple of options that were named
        """
        R = []
        for i in self._optargs:
            opts = i.split(':')
            if arg in opts:
                for o in opts:
                    R += [o]
                self._names[name] = R
                return R

        raise KeyError(f"Option '{arg}' doesn't exist")

    def fromName(self, name):
        """
        Must call class with sys.argv[1:] before using this method
         - returns an items() list using names instead of options
        """
        try:
            return self._optargs[ list(set(list( self._optargs )) & set( self._names[name] ))[0] ]
        except KeyError:
            raise KeyError(f"Option name '{name}' doesn't exist")
