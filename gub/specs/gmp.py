import re
import os
#
from gub import build
from gub import misc
from gub import target
from gub import tools

class Gmp (target.AutoBuild):
    source = 'http://ftp.gnu.org/pub/gnu/gmp/gmp-6.0.0a.tar.xz'
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        if not self.settings.platform.startswith ('darwin'):
            self.target_architecture = re.sub ('i[0-9]86-', 'i386-', settings.target_architecture)
        if 'stat' in misc.librestrict ():
            build.add_dict (self, {'LIBRESTRICT_IGNORE': '%(tools_prefix)s/bin/bash'})
    dependencies = ['libtool', 'tools::autoconf', 'tools::automake', 'tools::bison', 'tools::flex', 'tools::libtool', 'tools::xzutils']
    configure_flags = (target.AutoBuild.configure_flags
                       + ' --disable-cxx ')
    def configure (self):
        target.AutoBuild.configure (self)
        # automake's Makefile.in's too old for new libtool,
        # but autoupdating breaks even more.  This nice
        # hack seems to work.
        self.file_sub ([('(#! .*/bin/.*sh)', r'#! \1\ntagname=CXX')],
                       '%(builddir)s/libtool')
        
class Gmp__darwin (Gmp):
    def patch (self):
        ## powerpc/darwin cross barfs on all C++ includes from
        ## a C linkage file.
        ## don't know why. Let's patch C++ completely from GMP.
        self.file_sub ([('__GMP_DECLSPEC_XX std::[oi]stream& operator[<>][^;]+;$', ''),
                ('#include <iosfwd>', ''),
                ('<cstddef>','<stddef.h>')
                ],
               '%(srcdir)s/gmp-h.in')
        Gmp.patch (self)
    def install (self):
        Gmp.install (self)
        self.file_sub ([('using std::FILE;','')],
                       '%(install_prefix)s/include/gmp.h')

class Gmp__mingw (Gmp):
    patches = []
    def __init__ (self, settings, source):
        Gmp.__init__ (self, settings, source)
        # Configure (compile) without -mwindows for console
        self.target_gcc_flags = '-mms-bitfields'
    def install (self):
        Gmp.install (self)
        self.system ('''
mv %(install_prefix)s/lib/*dll %(install_prefix)s/bin || true
''')

class Gmp__tools (tools.AutoBuild, Gmp):
    dependencies = ['bison', 'flex', 'libtool', 'xzutils']
    configure_variables = (tools.AutoBuild.configure_variables
                           # avoid __isoc99_fscanf@@GLIBC_2.7 etc
                           + ' CPPFLAGS=-D_GNU_SOURCE')
    def __init__ (self, settings, source):
        tools.AutoBuild.__init__ (self, settings, source)
        if 'ABI' not in os.environ:
            if settings.target_bits == "32":
                self.configure_variables += ' ABI=32'
            elif settings.target_bits == "64":
                self.configure_variables += ' ABI=64'
