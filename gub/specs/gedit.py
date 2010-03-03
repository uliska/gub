'''
TODO:
  * figure out solution pango/pangocairo, lilypond/lilypondcairo mess
'''

from gub import misc
from gub import repository
from gub import target

class Gedit (target.AutoBuild):
    source = 'git://git.savannah.gnu.org/gedit.git'
    source = 'http://ftp.gnome.org/pub/GNOME/sources/gedit/2.29/gedit-2.29.2.tar.gz'
    subpackage_names = ['']
    dependencies = [
        'tools::automake',
        'tools::gettext',
        'tools::libtool',
        'tools::pkg-config',
        'gtk+-devel',
        'libgtksourceview-devel',
        'libxml2-devel',
        'python',
        ]
    configure_flags = (target.AutoBuild.configure_flags
                       + ' --enable-binreloc'
                       + ' --program-prefix='
                       )
    # FIXME: --enable-binreloc has been neutralized.
    make_flags = 'BINRELOC_CFLAGS=-DENABLE_BINRELOC=1'

    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        if isinstance (source, repository.Git):
            source.version = misc.bind_method (repository.Repository.version_from_configure_in, source)

class Gedit__mingw__windows (Gedit):
    dependencies = [x for x in Gedit.dependencies
                    if x.replace ('-devel', '') not in [
            ]]
    make_flags = ''

class Gedit__mingw__console (Gedit__mingw__windows):
    configure_flags = (Gedit__mingw__windows.configure_flags
                       + ' --enable-debugging')
    def __init__ (self, settings, source):
        Gedit__mingw__windows.__init__ (self, settings, source)
        # Configure (link) without -mwindows for gedit-console.exe
        self.target_gcc_flags = '-mms-bitfields'
    def compile (self):
        Gedit__mingw__windows.compile (self)
        self.system ('''
cd %(builddir)s/src && mv .libs/gedit.exe gedit-console.exe && rm -f gedit.exe
cd %(builddir)s/src && make AM_LDFLAGS="-mwindows" && cp -p .libs/gedit.exe gedit-windows.exe
''')
    def install (self):
        Gedit__mingw__windows.install (self)
        self.system ('''
install -m755 %(builddir)s/src/gedit-windows.exe %(install_prefix)s/bin/gedit.exe
install -m755 %(builddir)s/src/gedit-console.exe %(install_prefix)s/bin/gedit-console.exe
''')

# Use debugging for Windows for now.
# Gedit__mingw = Gedit__mingw__windows
Gedit__mingw = Gedit__mingw__console

class Gedit__darwin (Gedit):
    dependencies = [x for x in Gedit.dependencies
                    if x.replace ('-devel', '') not in [
            'libxml2', # Included in darwin-sdk, hmm?
            ]]
