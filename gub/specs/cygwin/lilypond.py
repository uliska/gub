from gub import cygwin
from gub import gup
from gub import misc
from gub import target
from gub.specs import lilypond

class LilyPond (lilypond.LilyPond):
    '''A program for printing sheet music
LilyPond lets you create music notation.  It produces beautiful
sheet music from a high-level description file.'''
    subpackage_names = ['doc', '']
    source = 'http://lilypond.org/download/source/v2.14/lilypond-2.14.1.tar.gz'
#    source = 'git://git.sv.gnu.org/lilypond.git'
    dependencies = gup.gub_to_distro_deps (lilypond.LilyPond.dependencies,
                                           cygwin.gub_to_distro_dict) + [
        'tools::imagemagick',
        'tools::icoutils',
        ] + [
                                               'bash',
                                               'coreutils',
                                               'findutils',
                                               'flex',
                                               'urw-fonts',
                                               ]
    configure_flags = (lilypond.LilyPond.configure_flags
                       .replace ('--enable-relocation', '--disable-relocation'))
    LDFLAGS = '-L%(system_prefix)s/lib -L%(system_prefix)s/bin -L%(system_prefix)s/lib/w32api'
    make_flags = (lilypond.LilyPond.make_flags
                  + ' LDFLAGS="%(LDFLAGS)s"')
#    branch = 'stable/2.12'
    def __init__ (self, settings, source):
        lilypond.LilyPond.__init__ (self, settings, source)
        self.dependencies += [misc.with_platform ('lilypond-doc',
                                                  self.settings.build_platform)]
    def install (self):
        ##lilypond.LilyPond.install (self)
        target.AutoBuild.install (self)
        self.install_doc ()
    def install_doc (self):
        # lilypond.make uses `python gub/versiondb.py --build-for=2.11.32'
        # which only looks at source ball build numbers, which are always `1'
        # This could be fixed, but for now just build one doc ball per release?
        installer_build = '1'
        installer_version = self.build_version ()
        docball = self.expand ('%(uploads)s/lilypond-%(installer_version)s-%(installer_build)s.documentation.tar.bz2', env=locals ())

        self.system ('''
mkdir -p %(install_prefix)s/share/doc/lilypond
cd %(install_prefix)s && LIBRESTRICT_ALLOW=/ tar -C %(install_prefix)s -jxf %(docball)s
cd %(install_prefix)s/share/doc/lilypond/html && mv offline-root/Documentation .
cd %(install_prefix)s/share/doc/lilypond/html && rm -rf offline-root
cd %(install_prefix)s && rm -rf license
''',
                  locals ())
    def category_dict (self):
        return {'': 'Interpreters'}

Lilypond = LilyPond
