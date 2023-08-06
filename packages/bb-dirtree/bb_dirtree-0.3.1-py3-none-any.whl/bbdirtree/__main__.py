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
    Create and print a directory tree from the given directory
        directory     = directory to create tree of [default current dir]
        depth         = depth of directory to recurse into [default 999999]
        dotfiles      = show/not show hidden files [default False]
        exclude_dirs  = directories to ignore
        exclude files = files to ignore
        regex_ex      = regex format of files to exclude
        regex_in      = regex format to only include files
        title         = title for top of directory tree [default 'BB-DirTree']
                          - detects 'git' and 'python project' directories to title automatically
                          - can be 'None'
    """

    def __init__( self,
                  directory     = None,
                  depth         = 999999, *,
                  dotfiles      = False,
                  exclude_dirs  = [],
                  exclude_files = [],
                  follow_links  = False,                # NEW
                  ignore_errors = False,                # NEW
                  regex_ex      = [],
                  regex_in      = [],
                  title         = 'BB-DirTree' ):

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
        self.ignore_errors = ignore_errors              # NEW
        self.follow_links  = follow_links               # NEW
        self.regex_ex      = regex_ex
        self.regex_in      = regex_in
        self.exclude_dirs  = exclude_dirs
        self.exclude_files = exclude_files
        self.title         = title

        self.__getBase()

    def __getBase(self):
        """
        Recursive scan of base directory
            Returns layered dictionary { 'dirs': {}, 'files': [] }
        """
        @staticmethod
        def create_subdir():
            subdir = { 'dirs' : {},
                       'files': [],
                       'path' : '' }
            return subdir

        base_dir     = self.base_dir
        dotfiles     = self.dotfiles
        scandirs     = []
        self.listing = create_subdir()

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
                    if ( match( '^\.+', i ) or has_hidden_attr( join( directory, i )) ) and not dotfiles:
                        continue

                    elif islink( join( directory, i )):                         # NEW -----------------
                        if self.follow_links:
                            if isdir( join( directory, i )):
                                dirs.append((i, 'link', f' --> {realpath(join(directory, i))}'))
                                # log.debug(f"Added directory link '{dirs[-1]}'")
                            else:
                                files.append((i, 'link', f' --> {realpath(join(directory, i))}'))
                                # log.debug(f"Added file link '{files[-1]}'")
                        elif isdir( join( directory, i )):
                            files.append((i, 'dirlink', f' --> {realpath(join(directory, i))}'))
                            # log.debug(f"Added directory link as file '{files[-1]}'")
                        else:
                            files.append((i, 'link', f' --> {realpath(join(directory, i))}'))
                            # log.debug(f"Added file link '{files[-1]}'")
                                                                                # ---------------------
                    elif isdir( join( directory, i )):
                        dirs.append((i, 'dir'))
                        # log.debug(f"Added directory '{dirs[-1]}'")

                    else:
                        files.append((i, 'file'))
                        # log.debug(f"Added file '{files[-1]}'")

                dirs = sorted( dirs, key = lambda x:x[0] )              # NEW
                files = sorted( files, key = lambda x:x[0] )            # NEW

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
                current, scandir, level = scandirs.pop(0)           # NEW
            except:
                scan = False
                continue

            F, D, path = iterDir(scandir)
            current['path'] = path
            for d in D:
                if self.__chk_exclude(d[0], ftype = 'dir'):         # NEW
                    current['dirs'][d] = create_subdir()
                    if level < self.depth:
                        scandirs.append(( current['dirs'][d], join(scandir, d[0]), level + 1 ))     # NEW
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
        _FORMAT = { 'dir'     : f"{C_b()}_-_{C__()}",     # blue
                    'dirname' : f"{C_c()}_-_{C__()}",     # light cyan
                    'text'    : f"{C_Gr()}_-_{C__()}",    # dark gray
                    'file'    : f"{C_gri()}_-_{C__()}",   # italic gray
                    'link'    : f"{C_Ci()}_-_{C__()}",    # cyan italic              # NEW
                    'filelink': f"{C_Gri()}_-_{C__()}",   # dark gray italic         # NEW
                    'dirlink' : f"{C_bi()}_-_{C__()}",    # light blue italic        # NEW
                    'tree'    : f"{C_g()}_-_{C__()}",     # green
                    'pre'     : f"\n{C_W()}    {F_U()}_-_{C__()}",  # White
                    'title'   : f"{C_O()} {F_U()}_-_{C__()}",    # orange
                    'post'    : "",
                    'nl'      : '\n' }

        self.__getBase()
        list_tree = self.get_tree( self.listing, _FORMAT, self.base_dir, self.title )

        return list_tree

    def list_gui(self):
        """
        Return directory tree in html formatting
        """
        _FORMAT = { 'dir'     : "<font color=\"Blue\">_-_</font>",               # cyan
                    'dirname' : "<font color=\"DarkCyan\">_-_</font>",           # light cyan
                    'text'    : "<font color=\"Gray\">_-_</font>",               # gray
                    'file'    : "<font color=\"Gray\">_-_</font>",               # light gray
                    'link'    : "<font color=\"Cyan\"><i>_-_</i></font>",        # cyan italic          # NEW
                    'filelink': "<font color=\"DarkGray\"><i>_-_</i></font>",       # dark gray italic     # NEW
                    'dirlink' : "<font color=\"Blue\"><i>_-_</i></font>",    # light blue italic    # NEW
                    'tree'    : "<font color=\"LightGreen\">_-_</font>",        # green
                    'pre'     : "<body style=\"background-color: Black;\"><pre><font color=\"White\">  <u>_-_</u></font>",
                    'title'   : "<font color=\"Orange\">  <u>_-_</u></font>",
                    'post'    : "</pre></body>",
                    'nl'      : "<br>" }

        self.__getBase()
        list_tree = self.get_tree( self.listing, _FORMAT, self.base_dir, self.title )

        return list_tree

    @staticmethod
    def get_tree( listing, F, skel, TITLE ):
        def tree(f):
            T, B, L = '     ├', '──', '     └'

            if f == 'T':
                return T + B

            elif f == 'L':
                return L + B

            else:
                raise RuntimeError(f"Invalid key for 'f' - '{f}'")

        def indentText(num):
            pbT = '     │'
            pbF = '      '
            R = ''

            if num == 0:
                return ''

            for i in range(0, num):
                if passbar[i]:
                    R = R + pbT
                else:
                    R = R + pbF

            return R

        def getlist(obj):
            log.debug( f"Getting file list" )
            if not obj['dirs'] and not obj['files']:
                log.debug("Nothing to add")
                return [], []

            d = []
            for i in obj['dirs']:
                if len(i) == 3:
                    d.append(( obj['dirs'][i], i[0], i[1], i[2] ))
                else:
                    d.append(( obj['dirs'][i], i[0], i[1] ))
                log.debug( f"Appended '{d[-1]}' to file list" )


            log.debug( f"Files in list = '{obj['files']}'" )
            f = obj['files']

            return d, f

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

        title = get_title(skel)
        if not title:
            if os.getcwd() == os.path.expanduser('~'):
                title = f'Home Directory:\x1b[0;0;33m {basename(os.getcwd()).title()}'
            elif TITLE:
                title = TITLE
            else:
                title = 'BB-DirTree'
        if title.find(':') >= 0:                # NEW ---------------------------------------------------------------------------------------------------------------
            t0, t1 = title.split(':')
            Ilist, Plist = [], [ F['pre'].replace( '_-_', t0 + ':' ) + F['title'].replace( '_-_', t1.strip() ), F['dirname'].replace('_-_', '      ' + skel + os.path.sep ) ]
        else:
            Ilist, Plist = [], [ F['pre'].replace( '_-_', title ), F['dirname'].replace('_-_', '      ' + skel + os.path.sep ) ]
                                                # -------------------------------------------------------------------------------------------------------------------
        form = F

        dirs, files = getlist(listing)
        passbar = {0: False}
        level = 1
        passbar[level] = True
        Plist.append( f"{F['tree'].replace('_-_', indentText(level))}" )
        if len(dirs) + len(files) <= 1:
            passbar[level] = False

        Ilist.append(( dirs, files, level ))
        dirs, files = [], []

        while True:
            try:
                nextdir = dirs[0][0]

                if len(dirs) + len(files) == 1:
                    if dirs[0][2] == 'link':                 # NEW
                        Plist.append( f"{F['tree'].replace('_-_', indentText(level) + tree('L'))} {F['dirlink'].replace('_-_', dirs[0][1] + '/')} {F['link'].replace('_-_', dirs[0][3] + '/')}" )    # NEW
                    else:
                        Plist.append( f"{F['tree'].replace('_-_', indentText(level) + tree('L'))} {F['dir'].replace('_-_', dirs[0][1] + '/')}" )
                    passbar[level] = False
                else:
                    if dirs[0][2] == 'link':                 # NEW
                        Plist.append( f"{F['tree'].replace('_-_', indentText(level) + tree('T'))} {F['dirlink'].replace('_-_', dirs[0][1] + '/')} {F['link'].replace('_-_', dirs[0][3] + '/')}" )    # NEW
                    else:
                        Plist.append( f"{F['tree'].replace('_-_', indentText(level) + tree('T'))} {F['dir'].replace('_-_', dirs[0][1] + '/')}" )
                    passbar[level] = True

                dirs.pop(0)
                Ilist.append(( dirs, files, level ))
                level += 1
                dirs, files = getlist(nextdir)

            except IndexError:
                for i in range(0, len(files)):
                    if i == len(files) - 1:
                        t = 'L'
                    else:
                        t = 'T'

                    preT = F['tree'].replace('_-_', indentText(level) + tree(t))
                    if files[i][1] == 'link':                                                       # NEW -----------------------
                        Plist.append( f"{preT} {F['filelink'].replace('_-_', files[i][0])} {F['link'].replace('_-_', files[i][2])}" )
                    elif files[i][1] == 'dirlink':
                        Plist.append( f"{preT} {F['dirlink'].replace('_-_', files[i][0])} {F['link'].replace('_-_', files[i][2] + '/')}" )
                    else:
                        Plist.append( f"{preT} {F['file'].replace('_-_', files[i][0])}" )
                                                                                                    # ---------------------------
                try:
                    dirs, files, level = Ilist.pop(-1)

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
                 ( "-I", "--ignore-errors", "Ignore read errors (such as permission errors) - Default is to error and exit" ),        # NEW
                 ( "-h", "--help", "This help message" ),
                 ( "-l", "--follow-symlinks", "Follow links to directories - default is NOT to follow" ),               # NEW
                 ( "-q", "--qt-html", "Print in html format for use with QT - works with some browsers too" ),
                 ( "-r", "--regex", f"Use regex to include/exclude files in tree{C__()}\n{C_Gri()}  -see *Regex*" ),
                 ( "-v", "--verbose", "Set verbose level [1-5] <or> 'debug' = 1" ),             # NEW
                 ( "", "--no-print", "Don't print any output" )]         # NEW

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
    IGNORE_ERRORS = False       # NEW
    FOLLOW_LINKS  = False       # NEW
    NO_PRINT      = False       # NEW
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

        elif opt in ('-I', '--ignore-errors'):         # NEW
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

        elif opt in ('-l', '--follow-symlinks'):         # NEW
            FOLLOW_LINKS = True

        elif opt == "--no-print":         # NEW
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

        elif opt in ('-v', '--verbose'):         # NEW
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
                 follow_links = FOLLOW_LINKS,         # NEW
                 ignore_errors = IGNORE_ERRORS  )         # NEW

    if HTML:
        to_print = x.list_gui()
    else:
        to_print = x.list_tty()

    if NO_PRINT:            # NEW
        return 0

    print(to_print)
    return 0

if __name__ == "__main__":
    sys.exit( main() )
