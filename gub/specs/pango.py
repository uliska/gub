import re
#
from gub import misc
from gub import loggedos
from gub import target

pango_module_version_regexes = [
    (r'^1\.14', '1.5.0'),
    (r'^1\.20', '1.6.0'),
    (r'^1\.22', '1.6.0'),
    (r'^1\.24', '1.6.0'),
    (r'^1\.26', '1.6.0'),
    (r'^1\.27', '1.6.0'),
    (r'^1\.28', '1.6.0'),
    (r'^1\.29', '1.6.0'),
    (r'^1\.30', '1.6.0'),
    (r'^1\.31', '1.8.0'),
    (r'^1\.32', '1.8.0'),
    (r'^1\.33', '1.8.0'),
    (r'^1\.34', '1.8.0'),
    (r'^1\.35', '1.8.0'),
    (r'^1\.36', '1.8.0'),
    ]

class Pango (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/pango/1.36/pango-1.36.8.tar.xz'
    patches = [
        'pango-1.36.8-substitute-env.patch',
        'pango-1.36.8-test-without-cairo.patch',
    ]
    dependencies = [
            'tools::glib', 
            'freetype-devel',
            'fontconfig-devel',
            'glib-devel',
            'harfbuzz-devel',
            'libtool'
            ]
    def get_conflict_dict (self):
        return {'': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'devel': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'doc': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'runtime': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc']}
    configure_flags = (target.AutoBuild.configure_flags
                + misc.join_lines ('''
--without-cairo
'''))
    def module_version (self):
        result = None
        version = self.version()
        for regex, candidate in pango_module_version_regexes:
            if re.match(regex, version):
                result = candidate
                break
        assert result
        return result
    def install (self):
        target.AutoBuild.install (self)
        self.create_config_files ()
        self.fix_config_files ()
    def create_config_files (self, prefix='/usr'):
        pango_module_version = self.module_version ()
        etc = self.expand ('%(install_root)s/%(prefix)s/etc/pango', locals ())
        self.dump ('''[Pango]
ModuleFiles = $PANGO_PREFIX/etc/pango/pango.modules
ModulesPath = $PANGO_PREFIX/lib/pango/%(pango_module_version)s/modules
''' % locals (), etc + '/pangorc')
        self.dump ('''
setfile PANGO_RC_FILE=$INSTALLER_PREFIX/etc/pango/pangorc
setdir PANGO_PREFIX=$INSTALLER_PREFIX/
set PANGO_MODULE_VERSION=%(pango_module_version)s
''', '%(install_prefix)s/etc/relocate/pango.reloc', env=locals ())
        self.copy ('%(sourcefiledir)s/pango.modules', etc)
    def fix_config_files (self, prefix='/usr'):
        etc = self.expand ('%(install_root)s/%(prefix)s/etc/pango', locals ())
        self.system ('mkdir -p %(etc)s' , locals ())
        def fix_prefix (logger, file_name):
            loggedos.file_sub (logger, [('/' + prefix + '/', '$PANGO_PREFIX/')],
                               file_name)
        self.map_locate (fix_prefix, etc, '*')

class Pango__freebsd (Pango):
    dependencies = Pango.dependencies + ['libiconv-devel']

class Pango__darwin (Pango):
    def install (self):
        Pango.install (self)                
        # FIXME: PANGO needs .so, NOT .dylib?
        self.dump ('''
set PANGO_SO_EXTENSION=.so
''', '%(install_prefix)s/etc/relocate/pango.reloc', env=locals (), mode='a')
