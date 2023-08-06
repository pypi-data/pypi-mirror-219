import sys, os, logging, stat
from re import match
from os.path import ( isdir,
                      isfile,
                      islink,
                      join,
                      basename,
                      dirname,
                      realpath  )

log = logging.getLogger(__name__)

from .COLORS import *
from . import __version__

class DirTree:
    """
    Create a nice looking directory tree
    """
    _FORMAT = { 'tty': { 'dir'     : f"\x1b[38;2;0;0;255m_-_{C__()}",                   # blue
                         'dirname' : f"\x1b[38;2;29;84;173;1m_-_{C__()}",               # kinda blue, kinda purple BOLD
                         'text'    : f"\x1b[38;2;144;144;144m_-_{C__()}",               # gray
                         'file'    : f"\x1b[38;2;202;202;202m_-_{C__()}",               # light gray
                         'link'    : f"\x1b[38;2;19;245;234;3m_-_{C__()}",              # cyan italic
                         'filelink': f"\x1b[38;2;91;91;91;3m_-_{C__()}",                # dark gray italic
                         'dirlink' : f"\x1b[38;2;88;154;252;3m_-_{C__()}",              # light blue italic
                         'replink' : f"\x1b[38;2;184;0;0;3m_-_{C__()}",                 # red italic
                         'tree'    : f"\x1b[38;2;99;184;105m_-_{C__()}",                # light green
                         'treelink': f"\x1b[38;2;117;175;184m_-_{C__()}",               # light blue/green
                         'title'   : f"\x1b[38;2;255;255;255m{F_U()}_-_{C__()}",        # White UNDERLINE
                         'title2'  : f"\x1b[38;2;221;221;221;1m_-_{C__()}",             # offwhite BOLD
                         'pre'     : '',
                         'post'    : "",
                         'nl'      : '\n' },
                'html': { 'dir'     : "<font color=\"#0000ff\">_-_</font>",             # blue
                          'dirname' : "<font color=\"#1d54ad\"><b>_-_</b></font>",      # kinda blue, kinda purple BOLD
                          'text'    : "<font color=\"#909090\">_-_</font>",             # gray
                          'file'    : "<font color=\"#cacaca\">_-_</font>",             # light gray
                          'link'    : "<font color=\"#13f5ea\"><i>_-_</i></font>",      # cyan italic
                          'filelink': "<font color=\"#5b5b5b\"><i>_-_</i></font>",      # dark gray italic
                          'dirlink' : "<font color=\"#589afc\"><i>_-_</i></font>",      # light blue italic
                          'replink' : "<font color=\"#b80000\"><i>_-_</i></font>",      # red italic
                          'tree'    : "<font color=\"#63b869\">_-_</font>",             # light green
                          'treelink': "<font color=\"#75afb8\">_-_</font>",             # light blue/green
                          'title'   : "<font color=\"#ffffff\">  <u>_-_</u></font>",    # white UNDERLINE
                          'title2'  : "<font color=\"#dddddd\"><b>_-_</b></font>",      # offwhite BOLD
                          'pre'     : "<body style=\"background-color: #000000; color: #ffffff;\"><pre>",
                          'post'    : "</pre></body>",
                          'nl'      : "<br>" }}
    _LINK_LIST = []
    count = { 'dirs'          : 0,
              'files'         : 0,
              'followed_links': 0,
              'linkdirs'      : 0,
              'linkfiles'     : 0,
              'hidden_files'  : 0,
              'hidden_dirs'   : 0,
              'hidden_links'  : 0 }

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
                       'path'  : '',
                       'error' : False }
            return subdir

        base_dir     = self.base_dir
        dotfiles     = self.dotfiles
        scandirs     = []
        self.listing = create_subdir()
        self.listing['path'] = base_dir


        def isHidden(path):
            R = False
            try:
                if sys.platform == 'windows':
                    x = os.stat(path)
                    if x.st_file_attributes % 4 == stat.FILE_ATTRIBUTE_HIDDEN:
                        R = True
                elif match( '^\.+', basename(path) ):
                    R = True
            except Exception as E:
                log.exception(E)
            finally:
                return R

        def iterDir(directory, count):
            dirs, files, ERROR = [], [], False
            try:
                toIter = os.listdir(directory)
                _E = None
                log.debug(f"Scanning directory - '{directory}'")
                for i in toIter:
                    path = join( directory, i )
                    _islink = False
                    _isdir  = False
                    _hidden = isHidden(path)

                    if not dotfiles and _hidden:
                        continue

                    elif islink( path ):
                        _islink = True
                        if self.follow_links:
                            if ( basename( path ), realpath( path )) in self._LINK_LIST:
                                log.warning(f"Found infinite recursion loop from symlink to '{realpath(path)}'")
                                files.append((i, 'replink', f' --> {realpath( path )}'))
                            elif isdir( path ):
                                _isdir = True
                                log.info(f"Following symlink - '{path}'")
                                count['followed_links'] += 1
                                count['linkdirs'] += 1
                                self._LINK_LIST.append(( basename( path ), realpath( path )))
                                dirs.append((i, 'link', f' --> {realpath( path )}'))
                            else:
                                log.debug(f"Found file symlink - '{path}'")
                                count['linkfiles'] += 1
                                files.append((i, 'filelink', f' --> {realpath( path )}'))
                        elif isdir( join( directory, i )):
                            _isdir = True
                            log.debug(f"Found directory symlink - '{path}'")
                            count['linkdirs'] += 1
                            files.append((i, 'dirlink', f' --> {realpath( path )}'))
                        else:
                            log.debug(f"Found file symlink - '{path}'")
                            count['linkfiles'] += 1
                            files.append((i, 'filelink', f' --> {realpath( path )}'))

                    elif isdir( path ):
                        _isdir = True
                        count['dirs'] += 1
                        dirs.append((i, 'dir'))

                    else:
                        count['files'] += 1
                        files.append((i, 'file'))

                    if _hidden:
                        if _islink:
                            count['hidden_links'] += 1
                        elif _isdir:
                            count['hidden_dirs'] += 1
                        else:
                            count['hidden_files'] += 1

                dirs = sorted( dirs, key = lambda x:x[0] )
                files = sorted( files, key = lambda x:x[0] )

            except PermissionError as E:
                ERROR = True
                _E = E

            except Exception as E:
                ERROR = True
                _E = E

            finally:
                if _E:
                    if self.ignore_errors:
                        log.warning( str(_E) )
                    else:
                        log.error( str(_E) )
                        sys.exit(2)

                return files, dirs, directory, ERROR

        level = 0
        scandirs = [( self.listing, base_dir, level )]

        scan = True
        while scan:
            try:
                current, scandir, level = scandirs.pop(0)
            except:
                scan = False
                continue

            F, D, path, ERROR = iterDir(scandir, self.count)
            current['path'] = path
            current['error'] = ERROR

            for d in D:
                if self.__chk_exclude(d[0], ftype = 'dir'):
                    current['dirs'][d] = create_subdir()
                    if level < self.depth:
                        scandirs.append(( current['dirs'][d], join(scandir, d[0]), level + 1 ))
                    else:
                        log.debug(f"Level of depth '({self.depth})' has been reached")
                        if self.follow_links and d[1] == 'link':
                            log.info(f"Removing followed link count for '{join(scandir, d[0])}' - max depth reached")
                            self.count['followed_links'] -= 1

            for f in F:
                if self.__chk_exclude(f[0]):
                    current['files'].append(f)

        if self.depth < 999999:
            log.info(f"Recursion depth limited to {self.depth}")

        log.info(f"Found {self.count['files'] + self.count['linkfiles']} files and {self.count['dirs'] + self.count['linkdirs']} directories")
        log.info(f"Found {self.count['linkfiles']} symlinked files")
        log.info(f"Found {self.count['linkdirs']} symlinked directories")
        log.info(f"Followed {self.count['followed_links']} symlinked directories")

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
                                return f"Python Project: {name}"

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
                                return f"Git Project: {name}"

                        if not name:
                            return 'Git Project'

                    else:
                        cd = dirname(cd)

            def getWinTitle(D):
                for P in os.path.getvars('%PATH%').split(';'):
                    if D == P:
                        if D.startswith( os.path.expanduser('~') ):
                            return "User Path Directory"
                        else:
                            return "System Path Directory"

                if D.startswith( os.path.expanduser('~') ):
                    return f"User Directory: {basename(D)}"

                elif D.startswith( os.path.expandvars('%SystemRoot%')):
                    if D == os.path.expandvars('%SystemRoot%'):
                        return f"Windows Root Directory"
                    else:
                        return f"Windows Root: {basename(D)}"


                root_drive = os.path.abspath( os.path.sep )
                drive = os.path.abspath( D ).split( os.path.sep )[0] + os.path.sep
                if D.startswith( root_drive ):
                    return f"System: {basename(D)}"

                from .winvolumeinfo import VolumeInfo
                vi = VolumeInfo( drive )
                if vi.disk_label:
                    return f"Disk: {vi.disk_label}"
                elif vi.serial:
                    return f"Disk: {vi.serial}"
                else:
                    return 'BB-DirTree'

            def getUnixTitle(D):
                for P in os.environ['PATH'].split(':'):
                    if D == P:
                        if D.startswith( os.path.expanduser('~') ):
                            return "User Path Directory"
                        else:
                            return "System Path Directory"

                if D.startswith( os.path.expanduser('~') ):
                    return f"User Directory: {basename(D)}"

                from .unixvolumeinfo import VolumeInfo
                vi = VolumeInfo()
                part = vi.fromPath( D )

                if part['MOUNTPOINT'] == os.path.abspath( os.path.sep ):
                    if D == os.path.abspath( os.path.sep ):
                        return f"Linux Root"
                    else:
                        return f"Root: {basename(D)}"

                elif part:
                    if part['LABEL']:
                        return f"Disk: {part['LABEL']}"

                    elif part['PATH']:
                        return f"Disk: {part['PATH']}"

                return 'BB-DirTree'

            name = findPyProjectName(D)
            if name:
                return name

            name = findGitProjectName(D)
            if name:
                return name

            if D == os.path.expanduser('~'):
                name = f'Home Directory:\x1b[0;0;33m {basename(D).title()}'

            else:
                if sys.platform == 'windows':
                    name = getWinTitle(D)
                elif sys.platform == 'linux':
                    name = getUnixTitle(D)
                # elif sys.platform == "darwin":        # TODO add darwin specific titles
                #     pass
                else:
                    name = f"BB-DirTree"

            return name

        def getFancyTitle(T):
            try:
                width = os.get_terminal_size().columns
            except:
                width = 80

            if width >= 80:
                w = 68
            else:
                w = width - 12

            divider = f"    ┉╼{'':═^{w}}╾┉"
            return [ divider, f'          {T}', divider ]

        _TITLE = ''
        title = get_title(base_dir)

        if title.find(':') >= 0:
            t0, t1 = title.split(':')
            _TITLE = F['title'].replace( '_-_', t0.strip() + ':' ) + '  ' + F['title2'].replace( '_-_', t1.strip() )
        else:
            _TITLE = F['title'].replace( '_-_', title.strip() )

        bd = base_dir
        while len(bd) < 5:
            bd = ' ' + bd

        if base_dir == base_dir.split( os.path.sep )[0] + os.path.sep:
            _basedir = F['dirname'].replace( '_-_', '       ' + bd )
        elif islink( base_dir ):
            _TITLE = f"{_TITLE}  {F['replink'].replace( '_-_', '(link)' )}"
            _basedir = F['dirname'].replace( '_-_', '      ' + bd + os.path.sep ) + F['link'].replace( '_-_', " --> " + realpath(base_dir) + os.path.sep )
        else:
            _basedir = F['dirname'].replace( '_-_', '      ' + bd + os.path.sep )

        Ilist = []

        dirs, files, path = getlist(listing)
        level = 1
        if islink(path):
            link_levels.append(level)

        if len(dirs) + len(files) <= 1:
            passbar[level] = False
        else:
            passbar[level] = True

        self._output = Plist = [ F['pre'], *getFancyTitle(_TITLE), _basedir, indentText(2) ]

        Ilist.append(( dirs, files, level, path ))
        dirs, files = [], []

        while True:
            while link_levels and link_levels[-1] > level:
                link_levels.pop(-1)

            if islink(path) and level not in link_levels:
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
                 ( "-h", "--help", "This help message" ),
                 ( "-L", "--follow-links", "Follow links to directories - default is NOT to follow links" ),
                 ( "-q", "--qt-html", "Print in html format for use with QT - works with some browsers too" ),
                 ( "-r", "--regex", f"Use regex to include/exclude files in tree{C__()}\n{C_Gri()}  -see *Regex*" ),
                 ( "-v", "--verbose", "Set verbose level [1-5] <or> 'debug' = 1" ),
                 ( "", "--ignore-errors", "Ignore read errors (such as permission errors) - Default is to error and exit" ),
                 ( "", "--no-print", "Don't print any output" ),
                 ( "", "--version", "Print version info and exit" )]

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
        opts, args = getopt( sys.argv[1:], "b:d:De:hLqr:v:", [ "base-dir=",
                                                               "depth=",
                                                               "dotfiles",
                                                               "exclude=",
                                                               "ignore-errors",
                                                               "follow-links",
                                                               "help",
                                                               "no-print",
                                                               "qt-html",
                                                               "regex=",
                                                               "verbose=",
                                                               "version" ])
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
                    log.error(f"Can't find directory - '{arg}'")
                    return 1
            else:
                BASE_DIR = arg

        elif opt in ('-d', '--depth'):
            try:
                dpth = int(arg)
            except:
                log.error("Depth must be an integer")
                return 1

            DEPTH = dpth

        elif opt in ('-D', '--dotfiles'):
            DOTFILES = True

        elif opt in ('-e', '--exclude'):
            for i in arg.split(':'):
                if match( '.*/$', arg ):
                    EXCLUDE_DIRS.append(i[:-1])
                else:
                    EXCLUDE_FILES.append(i)

        elif opt in ('-h', '--help'):
            help_message()
            sys.exit(0)

        elif opt in ('-L', '--follow-links'):
            FOLLOW_LINKS = True

        elif opt in ('-q', '--qt-html'):
            HTML = True

        elif opt in ('-r', '--regex'):
            try:
                m = arg.split('=', 1)[0]
                reg = arg.split('=', 1)[1]
            except:
                log.error("Invalid format for regex option. See 'dirtree --help'")
                return 1

            if m == 'include':
                REGEX_IN.append(reg)
            elif m == 'exclude':
                REGEX_EX.append(reg)
            else:
                log.error(f"Invalid regex option '{m}'. See 'dirtree --help'")
                return 1

        elif opt in ('-v', '--verbose'):
            try:
                if arg.lower() in ( '1', 'debug' ):
                    log.set_format( 'debug' )
                else:
                    log.set_level( int(arg) )
            except TypeError:
                log.error("Verbosity must be a number 1-5 <or> 'debug'")
                return 1
            except Exception as E:
                log.exception(E)
                raise E

        elif opt == '--ignore-errors':
            IGNORE_ERRORS = True

        elif opt == "--no-print":
            NO_PRINT = True

        elif opt == '--version':
            print( '\n'.join([ '',
                               f"{C_W()}    ╭╼═════════════════════════════════════════════════════════╾╮",
                               f"{C_W()}    ╽                                                           ╽",
                               f"{C_W()}    ║     {F_U()}BB-DirTree{C__()}{C_Gri()}  - print a nice looking directory tree{C_W()}     ║",
                               f"{C_W()}    ║                                                           ║",
                               f"{C_W()}    ║{C_gri()}      version:{C_Gr()}   {__version__}{C_W()}                                     ║",
                               f"{C_W()}    ║{C_gri()}      developer:{C_Gr()} Erik Beebe{C_W()}                                ║",
                               f"{C_W()}    ║{C_gri()}      webpage:{C_C()}   https://pypi.org/project/bb-dirtree/{C_W()}      ║",
                               f"{C_W()}    ║{C_gri()}      debugging:{C_C()} beebeapps_debugging@tuta.io{C_W()}               ║",
                               f"{C_W()}    ║{C_gri()}      feedback:{C_C()}  beebeapps_feedback@tuta.io{C_W()}                ║",
                               f"{C_W()}    ╿                                                           ╿",
                               f"{C_W()}    ╰╼═════════════════════════════════════════════════════════╾╯",
                               '' ]))
            sys.exit(0)

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
