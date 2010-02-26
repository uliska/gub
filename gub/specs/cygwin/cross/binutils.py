from gub import misc
from gub import cygwin
from gub.specs.cross import binutils as cross_binutils

# FIXME: setting binutil's tooldir and/or gcc's gcc_tooldir may fix
# -luser32 (ie -L .../w32api/) problem without having to set LDFLAGS.
class Binutils__cygwin (cross_binutils.Binutils):
    make_flags = misc.join_lines ('''
tooldir="%(cross_prefix)s/%(target_architecture)s"
''')
    configure_flags = (cross_binutils.Binutils.configure_flags
                 + ' --disable-werror ')
    def pre_install (self):
        self.system ('mkdir -p %(install_prefix)s%(cross_dir)s/%(target_architecture)s/bin')

class use_cygwin_sources_Binutils (cross_binutils.Binutils):
    source = 'http://mirrors.kernel.org/sourceware/cygwin/release/binutils/binutils-20060817-1-src.tar.bz2'
