from gub import gnome
from gub import target

class Gconf (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.26/2.26.3/sources/GConf-2.26.2.tar.gz'
    dependencies = [
        'tools::libtool',
        'orbit',
        'dbus-glib',
        ]
    configure_flags = target.AutoBuild.configure_flags + ' --disable-defaults-service '
