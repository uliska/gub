from gub import target
from gub import tools

class Libffi (target.AutoBuild):
    source = 'ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz'
    patches = [ 'libffi-3.2.1-includedir.patch', ]
    dependencies = [
        'tools::automake',
        'tools::libtool',
        'tools::pkg-config',
        ]

class Libffi__linux__64 (Libffi):
    # For using /usr/lib instead of /usr/lib64
    patches = Libffi.patches + [
        'libffi-3.2.1-linux-64-libdir.patch',
    ]

class Libffi__darwin__x86 (Libffi):
    # darwin-x86 can not compile libffi 3.1, 3.2.1.
    source = 'ftp://sourceware.org/pub/libffi/libffi-3.0.13.tar.gz'
    patches = [ 'libffi-3.0.13-includedir.patch', ]

class Libffi__tools (tools.AutoBuild, Libffi):
    pass
