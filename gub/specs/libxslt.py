from gub import context
from gub import loggedos
from gub import misc
from gub import target
from gub import tools

class Libxslt (target.AutoBuild):
    source = 'http://xmlsoft.org/sources/libxslt-1.1.24.tar.gz'
    def patch (self):
        self.system ('rm -f %(srcdir)s/libxslt/xsltconfig.h')
    dependencies = ['libxml2-devel', 'zlib-devel']
    configure_flags = (target.AutoBuild.configure_flags
                + misc.join_lines ('''
--without-python
--without-crypto
'''))
    @context.subst_method
    def config_script (self):
        return 'xslt-config'

class Libxslt__mingw (Libxslt):
    configure_flags = (Libxslt.configure_flags
                + misc.join_lines ('''
--without-plugins
'''))
    def configure (self):
        Libxslt.configure (self)
        def undo_libtool_disable_install_not_into_dot_libs_test (logger, file):
            loggedos.file_sub (logger, [
            (r'if false && test "\$inst_prefix_dir" = "\$destdir"; then',
             'if test "$inst_prefix_dir" = "$destdir"; then'),
            (r'  false && test "\$inst_prefix_dir" = "\$destdir" &&',
             '  test "$inst_prefix_dir" = "$destdir" &&')],
                       file)
        def undo_libtool_disable_relink (logger, file):
            loggedos.file_sub (logger, [('need_relink=no', 'need_relink=yes')], file)
        self.map_locate (undo_libtool_disable_install_not_into_dot_libs_test, '%(builddir)s', 'libtool')
        self.map_locate (undo_libtool_disable_relink, '%(builddir)s', 'libtool')

class Libxslt__darwin (Libxslt):
    dependencies = [x for x in Libxslt.dependencies
                if x.replace ('-devel', '') not in [
                'libxml2', # Included in darwin-sdk, hmm?
                ]]

class Libxslt__tools (tools.AutoBuild, Libxslt):
    dependencies = Libxslt.dependencies + ['libtool']
