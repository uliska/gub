from gub import target
from gub import tools

class Libunistring (target.AutoBuild):
    source = 'http://ftp.gnu.org/gnu/libunistring/libunistring-0.9.3.tar.gz'

class Libunistring__mingw (Libunistring):
    patches = [
        'libunistring-mingw.patch',
        ]

class Libunistring__tools (tools.AutoBuild, Libunistring):
    pass
