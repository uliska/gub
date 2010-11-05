from gub import gnome
from gub import target

class Gnomecanvas (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.26/2.26.3/sources/libgnomecanvas-2.26.0.tar.gz'
    dependencies = [
        'tools::libtool',
        'tools::intltool',
        'glib-devel',
        'gtk+-devel',
        'libart-devel',
        'libglade-devel',
        'pangocairo-devel',
        ]
