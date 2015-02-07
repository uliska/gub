#
from gub import misc
from gub import target
from gub import tools

class Expat (target.AutoBuild):
    source = 'http://sourceforge.net/projects/expat/files/expat/2.0.1/expat-2.0.1.tar.gz'
    patches = ['expat-2.0.1-mingw.patch']
    dependencies = ['libtool', 'tools::expat']
    make_flags = misc.join_lines ('''
CFLAGS='-O2 -DHAVE_EXPAT_CONFIG_H'
EXEEXT=
RUN_FC_CACHE_TEST=false
''')
    if 'stat' in misc.librestrict (): # 40 lines of sh code from 1993 implementing `mkdir -p', statting components of DESTDIR: /home, ...
        make_flags = make_flags + ''' 'mkinstalldirs=mkdir -p' '''
    def patch (self):
        target.AutoBuild.patch (self)
        #FIXME: should have configure.ac/in vs configure timestamp test
        self.system ('rm %(srcdir)s/configure')
        self.system ('touch %(srcdir)s/tests/xmltest.sh.in')

class Expat__mingw (Expat):
    # mingw's expat libtool build breaks with DASH
    configure_variables = (Expat.configure_variables
                .replace ('SHELL=', 'XSHELL='))

class Expat__linux__arm__vfp (Expat):
    patches = []
    source = 'http://sourceforge.net/projects/expat/files/expat/2.0.0/expat-2.0.0.tar.gz'
    def patch (self):
        self.system ('touch %(srcdir)s/tests/xmltest.sh.in')
        target.AutoBuild.patch (self)

class Expat__darwin (Expat):
    dependencies = [x for x in Expat.dependencies
                if x.replace ('-devel', '') not in [
                'libxml2', # Included in darwin-sdk, hmm?
                ]]

class Expat__tools (tools.AutoBuild, Expat):
    dependencies = [
            'automake',
            'libtool',
            ]
