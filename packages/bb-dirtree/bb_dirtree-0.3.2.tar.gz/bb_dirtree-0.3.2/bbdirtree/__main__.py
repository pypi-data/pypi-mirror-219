import sys, os, ctypes, logging
from configparser import ConfigParser
from re import match
from os.path import ( isdir,
                      isfile,
                      islink,
                      join,
                      basename,
                      dirname,
                      realpath  )
from glob import glob
from .COLORS import *

log = logging.getLogger(__name__)

class DirTree:
    """
    Create a nice looking directory tree
    """
    _FORMAT = { 'tty': { 'dir'     : f"{C_b()}_-_{C__()}",               # blue
                         'dirname' : f"{C_c()}_-_{C__()}",               # light cyan
                         'text'    : f"{C_Gr()}_-_{C__()}",              # dark gray
                         'file'    : f"{C_gri()}_-_{C__()}",             # italic gray
                         'link'    : f"{C_Ci()}_-_{C__()}",              # cyan italic
                         'filelink': f"{C_Gri()}_-_{C__()}",             # dark gray italic
                         'dirlink' : f"{C_bi()}_-_{C__()}",              # light blue italic
                         'replink' : f"{C_ri()}_-_{C__()}",              # light red italic
                         'tree'    : f"{C_g()}_-_{C__()}",               # green
                         'treelink': f"{C_C()}_-_{C__()}",               # cyan
                         'pre'     : f"\n{C_W()}    {F_U()}_-_{C__()}",  # White
                         'title'   : f"{C_O()} {F_U()}_-_{C__()}",       # orange
                         'post'    : "",
                         'nl'      : '\n' },
                'html': { 'dir'     : "<font color=\"Blue\">_-_</font>",              # cyan
                          'dirname' : "<font color=\"DarkCyan\">_-_</font>",          # light cyan
                          'text'    : "<font color=\"Gray\">_-_</font>",              # gray
                          'file'    : "<font color=\"Gray\">_-_</font>",              # light gray
                          'link'    : "<font color=\"Cyan\"><i>_-_</i></font>",       # cyan italic
                          'filelink': "<font color=\"DarkGray\"><i>_-_</i></font>",   # dark gray italic
                          'dirlink' : "<font color=\"Blue\"><i>_-_</i></font>",       # light blue italic
                          'replink' : "<font color=\"Red\"><i>_-_</i></font>",        # red italic
                          'tree'    : "<font color=\"LightGreen\">_-_</font>",        # green
                          'treelink': "<font color=\"Cyan\">_-_</font>",              # light cyan
                          'pre'     : "<body style=\"background-color: Black;\"><pre><font color=\"White\">  <u>_-_</u></font>",
                          'title'   : "<font color=\"Orange\">  <u>_-_</u></font>",
                          'post'    : "</pre></body>",
                          'nl'      : "<br>" }}
    _LINK_LIST = []

    def __init__( self,
                  directory     = None,
                  depth         = 999999, *,
                  dotfiles      = False,
                  exclude_dirs  = [],
                  exclude_files = [],
                  follow_links  = False,
                  ignore_errors = False,
                  regex_ex      = [],
                  regex_in      = []    ):
        """
        Create and print a directory tree from the given directory
            directory     = directory to create tree of [default current dir]
            depth         = depth of directory to recurse into [default 999999]
            dotfiles      = show/not show hidden files [default False]
            exclude_dirs  = directories to ignore
            exclude files = files to ignore
            follow_links  = follows symlinks for directories
            ignore_errors = continue to parse directories, regardless of errors
            regex_ex      = regex format of files to exclude
            regex_in      = regex format to only include files
        """

        if not directory:
            directory = os.getcwd()

        elif not isdir( directory ):
            try:
                assert isdir( join( os.getcwd(), directory ))
                directory = join( os.getcwd(), directory )
            except:
                directory = os.getcwd()

        self.base_dir      = directory
        self.depth         = depth
        self.dotfiles      = dotfiles
        self.ignore_errors = ignore_errors
        self.follow_links  = follow_links
        self.regex_ex      = regex_ex
        self.regex_in      = regex_in
        self.exclude_dirs  = exclude_dirs
        self.exclude_files = exclude_files
        self._output       = []
        self._output_data  = []
        self._output_type  = ''

        self.__getBase()

    def __getBase(self):
        """
        Recursive scan of base directory
            Returns layered dictionary { 'dirs': {}, 'files': [] }
        """
        @staticmethod
        def create_subdir():
            subdir = { 'dirs'  : {},
                       'files' : [],
                       'path'  : '' }
            return subdir

        base_dir     = self.base_dir
        dotfiles     = self.dotfiles
        scandirs     = []
        self.listing = create_subdir()
        self.listing['path'] = base_dir

        def iterDir(directory):
            def has_hidden_attr(filepath):
                try:
                    attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
                    assert attrs != -1
                    result = bool(attrs & 2)
                except (AttributeError, AssertionError):
                    result = False
                return result

            dirs, files = [], []
            try:
                _E = None
                log.debug(f"Scanning directory - '{directory}'")
                for i in os.listdir(directory):
                    path = join( directory, i )

                    if ( match( '^\.+', i ) or has_hidden_attr( path )) and not dotfiles:
                        continue

                    elif islink( path ):
                        if self.follow_links:
                            if ( basename( path ), realpath( path )) in self._LINK_LIST:
                                log.warning(f"Avoiding continuous recursion from symlink - '{path}'")
                                files.append((i, 'replink', f' --> {realpath( path )}'))
                            elif isdir( path ):
                                self._LINK_LIST.append(( basename( path ), realpath( path )))
                                dirs.append((i, 'link', f' --> {realpath( path )}'))
                            else:
                                files.append((i, 'filelink', f' --> {realpath( path )}'))
                        elif isdir( join( directory, i )):
                            files.append((i, 'dirlink', f' --> {realpath( path )}'))
                        else:
                            files.append((i, 'filelink', f' --> {realpath( path )}'))

                    elif isdir( path ):
                        dirs.append((i, 'dir'))

                    else:
                        files.append((i, 'file'))

                dirs = sorted( dirs, key = lambda x:x[0] )
                files = sorted( files, key = lambda x:x[0] )

            except PermissionError as E:
                log.warning( str(E) )
                _E = E

            except Exception as E:
                log.exception(E)
                _E = E

            finally:
                if _E and not self.ignore_errors:
                    raise _E

                return files, dirs, directory

        level = 0
        scandirs = [( self.listing, base_dir, level )]

        scan = True
        while scan:
            try:
                current, scandir, level = scandirs.pop(0)
            except:
                scan = False
                continue

            F, D, path = iterDir(scandir)
            current['path'] = path

            for d in D:
                if self.__chk_exclude(d[0], ftype = 'dir'):
                    current['dirs'][d] = create_subdir()
                    if level < self.depth:
                        scandirs.append(( current['dirs'][d], join(scandir, d[0]), level + 1 ))
                    else:
                        log.info(f"Level of depth '({self.depth})' has been reached")

            for f in F:
                if self.__chk_exclude(f[0]):
                    current['files'].append(f)

    def __chk_reg(func):
        def __wrapper(self, item, ftype = 'file'):
            if ( not self.regex_ex and not self.regex_in ) or ftype == 'dir':
                R = func(self, item, ftype)
                return R

            exclude = False

            if self.regex_in:
                exclude = True
                for inc in self.regex_in:
                    if match( inc, item ):
                        exclude = False
                        break

            if exclude:
                log.debug(f"Excluding '{item}' from listing")
                return False

            for ex in self.regex_ex:
                if match( ex, item ):
                    log.debug(f"Excluding '{item}' from listing")
                    return False

            R = func(self, item, ftype)
            return R

        return __wrapper

    @__chk_reg
    def __chk_exclude(self, item, ftype = 'file'):
        if ftype == 'dir':
            if item in self.exclude_dirs:
                return False

            return True

        else:
            if item in self.exclude_files:
                return False

            return True

    def list_tty(self):
        """
        Return directory tree formatted for terminal view
        """
        self._output_type = 'TTY'
        list_tree = self.get_tree( self._FORMAT['tty'] )

        return list_tree

    def list_gui(self):
        """
        Return directory tree in html formatting
        """
        self._output_type = 'HTML'
        list_tree = self.get_tree( self._FORMAT['html'] )

        return list_tree

    def get_tree(self, F):
        link_levels = []
        level = 0
        listing = dict( self.listing.items() )
        base_dir = self.base_dir
        passbar = {0: False}

        def tree(f):
            T, B, L = '     ├', '──', '     └'
            R = ''

            if f == 'T':
                R = T + B

            elif f == 'L':
                R = L + B

            else:
                raise RuntimeError(f"Invalid key for 'f' - '{f}'")

            if level in link_levels:
                return F['treelink'].replace('_-_', R)
            else:
                return F['tree'].replace('_-_', R)

        def indentText(num):
            pbT = '     │'
            pbF = '      '
            R = ''

            if num == 0:
                return ''

            for i in range(0, num):
                if passbar[i]:
                    if i in link_levels:
                        R = R + F['treelink'].replace('_-_', pbT)
                    else:
                        R = R + F['tree'].replace('_-_', pbT)
                else:
                    R = R + pbF

            return R

        def getlist(obj):
            log.debug( f"Getting file list" )
            if not obj['dirs'] and not obj['files']:
                log.debug("Nothing to add")
                return [], [], obj['path']

            d = []
            for i in obj['dirs']:
                if len(i) == 3:
                    d.append(( obj['dirs'][i], i[0], i[1], i[2] ))
                else:
                    d.append(( obj['dirs'][i], i[0], i[1] ))
                log.debug( f"Appended '{d[-1]}' to file list" )


            log.debug( f"Files in list = '{obj['files']}'" )
            f = obj['files']

            return d, f, obj['path']

        def get_title(D):
            def findPyProjectName(D):           # Search for python project name
                cd = D
                name = None
                file, file_lines = None, []
                while True:
                    if cd == os.path.expanduser('~') or cd == os.path.sep:
                        return ''

                    files = os.listdir(cd)
                    if 'pyproject.toml' in files:
                        file = join( cd, 'pyproject.toml' )
                    elif 'setup.py' in files:
                        file = join( cd, 'setup.py' )

                    if file:
                        with open( file, 'r' ) as f:
                            file_lines = [ i.strip() for i in f.read().strip().split('\n') ]

                        for line in file_lines:
                            if line.startswith('name'):
                                name = line.split('=')[1].replace('"', '').replace("'", '').strip()
                                return name

                        if not name:
                            return 'Python Project'

                    else:
                        cd = dirname(cd)

            def findGitProjectName(D):           # Search for git project name
                cd = D
                name = None
                while True:
                    if cd == os.path.expanduser('~') or cd == os.path.sep:
                        return ''

                    files = os.listdir(cd)
                    if '.SRCINFO' in files:
                        file = join( cd, '.SRCINFO' )
                        with open( file, 'r' ) as f:
                            file_lines = [ i.strip() for i in f.read().strip().split('\n') ]

                        for line in file_lines:
                            if line.startswith('pkgbase'):
                                name = line.split('=')[1].replace('"', '').replace("'", '').strip()
                                return name

                        if not name:
                            return 'Git Project'

                    else:
                        cd = dirname(cd)

            name = findPyProjectName(D)
            if name:
                return f"Python Project: {name}"

            name = findGitProjectName(D)
            if name:
                return f"Git Project: {name}"

            return ''

        title = get_title(base_dir)
        if not title:
            if os.getcwd() == os.path.expanduser('~'):
                title = f'Home Directory:\x1b[0;0;33m {basename(os.getcwd()).title()}'
            else:
                title = 'BB-DirTree'

        Ilist = []

        if title.find(':') >= 0:
            t0, t1 = title.split(':')
            self._output = Plist = [ F['pre'].replace( '_-_', t0 + ':' ) + F['title'].replace( '_-_', t1.strip() ), F['dirname'].replace('_-_', '      ' + base_dir + os.path.sep ) ]
        else:
            self._output = Plist = [ F['pre'].replace( '_-_', title ), F['dirname'].replace('_-_', '      ' + base_dir + os.path.sep ) ]

        dirs, files, path = getlist(listing)
        level = 1
        Plist.append( f"{F['tree'].replace('_-_', indentText(level))}" )

        if len(dirs) + len(files) <= 1:
            passbar[level] = False
        else:
            passbar[level] = True

        Ilist.append(( dirs, files, level, path ))
        dirs, files = [], []

        while True:
            while link_levels and link_levels[-1] > level:
                link_levels.pop(-1)

            if islink(path):
                link_levels = sorted( link_levels + [level] )

            try:
                nextdir = dirs[0][0]
                log.debug(f"nextdir = '{nextdir}'")

                if len(dirs) + len(files) == 1:
                    _tree = indentText(level) + tree('L')
                    passbar[level] = False
                else:
                    _tree = indentText(level) + tree('T')
                    passbar[level] = True

                if dirs[0][2] == 'link':
                    _txt = f" {F['dirlink'].replace('_-_', dirs[0][1] + '/')} {F['link'].replace('_-_', dirs[0][3] + '/')}"
                else:
                    _txt = f" {F['dir'].replace('_-_', dirs[0][1] + '/')}"

                Plist.append( _tree + _txt )
                dirs.pop(0)
                Ilist.append(( dirs, files, level, path ))
                level += 1
                dirs, files, path = getlist(nextdir)

            except IndexError:
                for i in range(0, len(files)):
                    if i == len(files) - 1:
                        t = 'L'
                    else:
                        t = 'T'

                    preT = F['tree'].replace('_-_', indentText(level) + tree(t))
                    if files[i][1] == 'filelink':
                        Plist.append( f"{preT} {F[ 'filelink' ].replace('_-_', files[i][0])} {F['link'].replace('_-_', files[i][2])}" )
                    elif files[i][1] in ( 'replink', 'dirlink' ):
                        Plist.append( f"{preT} {F[ files[i][1] ].replace('_-_', files[i][0] + '/')} {F['link'].replace('_-_', files[i][2] + '/')}" )
                    else:
                        Plist.append( f"{preT} {F['file'].replace('_-_', files[i][0])}" )

                try:
                    dirs, files, level, path = Ilist.pop(-1)
                    self._output_data.append({'path': path, 'dirs': dirs, 'files': files, 'level': level})
                except IndexError:
                    Plist.append( F['post'] )
                    break

        return F['nl'].join(Plist)

def err(s):
    print(f"\x1b[1;31m  [ERROR]\x1b[0;1;30;3m {s}\x1b[0m")

def main():
    from getopt import getopt
    from tabulate import tabulate
    from time import sleep

    def help_message():
        headers = [ f"{C_W()}Short{C__()}", f"{C_W()}Long{C__()}", f"{C_W()}Description{C__()}" ]

        body = []

        opts = [ ( "-b", "--base-dir", f"Set base directory{C__()}\n{C_Gri()}  -uses current directory if not specified" ),
                 ( "-d", "--depth", f"Integer to set the depth of directory tree{C__()}\n{C_Gri()}  -ex: '0' will only print the base directory list" ),
                 ( "-D", "--dotfiles", f"Include hidden files in tree" ),
                 ( "-e", "--exclude", f"Filenames/directories to exclude from the tree{C__()}\n{C_Gri()}  -see *Exclusions*" ),
                 ( "-I", "--ignore-errors", "Ignore read errors (such as permission errors) - Default is to error and exit" ),
                 ( "-h", "--help", "This help message" ),
                 ( "-l", "--follow-symlinks", "Follow links to directories - default is NOT to follow" ),
                 ( "-q", "--qt-html", "Print in html format for use with QT - works with some browsers too" ),
                 ( "-r", "--regex", f"Use regex to include/exclude files in tree{C__()}\n{C_Gri()}  -see *Regex*" ),
                 ( "-v", "--verbose", "Set verbose level [1-5] <or> 'debug' = 1" ),
                 ( "", "--no-print", "Don't print any output" )]

        table = []
        for i in opts:
            table.append([ C_Y() + i[0] + C__(),
                           C_Y() + i[1] + C__(),
                           C_Gr() + i[2] + C__() ])

        tab  = tabulate(table, headers, tablefmt="fancy_grid").split('\n')

        _ = f"{C_Gr()}|{C_Y()}"
        print( '\n'.join([ f"\n{C_W()}    {F_U()}DirTree{C__()}",
                           f"{C_P()}         dirtree{C_gri()} [OPTIONS]{C_Gri()} [ARGS]{C__()}",
                           '',
                           f"{C_gr()}    {F_U()}Options:{C__()}",
                           "      " + "\n      ".join(tab),
                           '',
                           f"{C_W()}  *{F_U()}Exclusions{F__U()}*{C__()}",
                           f"{C_gri()}      Provide names of files or directories to exclude. To exclude",
                           "    multiple files/directories, quote entire list and seperate",
                           f"    with a colon '{C__()}{C_W()}:{C_gri()}'. Add a '{C__()}{C_W()}/{C_gri()}' to specify a directory name to",
                           "    exclude.\n",
                           "      Example:",
                           f"{C_P()}        bbdirtree{C_Y()} --exclude{C_Gri()} \"excluded dir/:excluded file\"\n",
                           f"{C_W()}  *{F_U()}Regex{F__U()}*{C__()}",
                           f"{C_gri()}      Prefix regex with {C__()}{C_Y()}include={C_Gr()} or{C_Y()} exclude={C_gri()}.",
                           "    Seperate each regex with a space, quoting each individual argument.\n",
                           "      Example:",
                           f"{C_P()}        bbdirtree{C_Y()} --regex{C_Gri()} \"exclude=.*\\.ini$\"{C_gri()}",
                           "          exclude any files that have an 'ini' extension.",
                           f"{C_P()}        bbdirtree{C_Y()} --regex{C_Gri()} \"include=.*\\.mp3$\"{C_gri()}",
                           "          include only files with an 'mp3' extension.\n",
                           "      This has no effect on directories. Multiple regex can be",
                           f"    used by specifying{C__()}{C_Y()} --regex{C_gri()} multiple times.\n\n" ]))

    try:
        opts, args = getopt( sys.argv[1:], "b:d:De:hIlqr:v:", [ "base-dir=",
                                                                "depth=",
                                                                "dotfiles",
                                                                "exclude=",
                                                                "ignore-errors",
                                                                "follow-symlinks",
                                                                "help",
                                                                "no-print",
                                                                "qt-html",
                                                                "regex=",
                                                                "verbose=" ])
    except:
        opts = []

    BASE_DIR      = os.getcwd()
    DEPTH         = 999999
    DOTFILES      = False
    EXCLUDE_FILES = []
    EXCLUDE_DIRS  = []
    HTML          = False
    IGNORE_ERRORS = False
    FOLLOW_LINKS  = False
    NO_PRINT      = False
    REGEX_IN      = []
    REGEX_EX      = []

    for opt, arg in opts:
        if opt in ('-b', '--base-dir'):
            bdir = arg
            if not isdir(bdir):
                bdir = join( os.getcwd(), bdir )
                if isdir(bdir):
                    BASE_DIR = bdir
                else:
                    err(f"Can't find directory - '{arg}'")
                    return 1
            else:
                BASE_DIR = arg

        elif opt in ('-d', '--depth'):
            try:
                dpth = int(arg)
            except:
                err("Depth must be an integer")
                return 1

            DEPTH = dpth

        elif opt in ('-D', '--dotfiles'):
            DOTFILES = True

        elif opt in ('-I', '--ignore-errors'):
            IGNORE_ERRORS = True

        elif opt in ('-e', '--exclude'):
            for i in arg.split(':'):
                if match( '.*/$', arg ):
                    EXCLUDE_DIRS.append(i[:-1])
                else:
                    EXCLUDE_FILES.append(i)

        elif opt in ('-h', '--help'):
            help_message()
            sys.exit(0)

        elif opt in ('-l', '--follow-symlinks'):
            FOLLOW_LINKS = True

        elif opt == "--no-print":
            NO_PRINT = True

        elif opt in ('-q', '--qt-html'):
            HTML = True

        elif opt in ('-r', '--regex'):
            try:
                m = arg.split('=', 1)[0]
                reg = arg.split('=', 1)[1]
            except:
                err("Invalid format for regex option. See 'dirtree --help'")
                return 1

            if m == 'include':
                REGEX_IN.append(reg)
            elif m == 'exclude':
                REGEX_EX.append(reg)
            else:
                err(f"Invalid regex option '{m}'. See 'dirtree --help'")
                return 1

        elif opt in ('-v', '--verbose'):
            try:
                if arg.lower() in ( '1', 'debug' ):
                    log.set_format( 'debug' )
                else:
                    log.set_level( int(arg) )
            except TypeError:
                err("Verbosity must be a number 1-5 <or> 'debug'")
                return 1
            except Exception as E:
                log.exception(E)
                raise E

    x = DirTree( BASE_DIR,
                 DEPTH,
                 dotfiles = DOTFILES,
                 exclude_dirs = EXCLUDE_DIRS,
                 exclude_files = EXCLUDE_FILES,
                 regex_ex = REGEX_EX,
                 regex_in = REGEX_IN,
                 follow_links = FOLLOW_LINKS,
                 ignore_errors = IGNORE_ERRORS  )

    if HTML:
        to_print = x.list_gui()
    else:
        to_print = x.list_tty()

    if NO_PRINT:
        return 0

    print(to_print)
    return 0

if __name__ == "__main__":
    sys.exit( main() )
