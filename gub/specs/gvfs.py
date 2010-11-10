from gub import gnome
from gub import target

class Gvfs (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/gvfs/1.2/gvfs-1.2.3.tar.gz'
    dependencies = [
        'tools::libtool',
        'glib-devel',
        'dbus',
        ]
    def patch (self):
        target.AutoBuild.patch (self)
        self.file_sub ([('pkg-config', '$PKG_CONFIG')], '%(srcdir)s/configure')
        self.file_sub ([(r'(^\s*)PKG_CONFIG=', r'\1XPKG_CONFIG=')], '%(srcdir)s/configure')
    def configure (self):
        target.AutoBuild.configure (self)
        self.file_sub ([('(giomodulesdir.*=")/.*/usr', r'\1/usr')], '%(builddir)s/config.status', must_succeed=True)
        self.system ('cd %(builddir)s && ./config.status')
