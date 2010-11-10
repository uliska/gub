from gub import build
from gub import gnome
from gub import target

class Gnome_vfs (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.26/2.26.3/sources/gnome-vfs-2.24.1.tar.gz'
    dependencies = [
        'tools::libtool',
        'glib-devel',
        'gconf-devel',
        'bzip2',
        'gnome-mime-data',
        ]
    compile_flags = target.AutoBuild.compile_flags + ' modulesdir=%(system_prefix)s/lib/gnome-vfs-2.0/modules'
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        build.append_dict (self, {'PKG_CONFIG_PATH': ':%(system_prefix)s/share/pkgconfig'})

