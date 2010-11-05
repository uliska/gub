from gub import gnome
from gub import target

class Libart (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.26/2.26.3/sources/libart_lgpl-2.3.20.tar.gz'
    dependencies = [
        'tools::libtool',
#        'tools::intltool',
        'glib-devel',
#        'gtk+-devel',
#        'pangocairo-devel',
#        'libart-devel',
        ]
