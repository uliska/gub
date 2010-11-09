from gub import gnome
from gub import target

class Libart (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.26/2.26.3/sources/libart_lgpl-2.3.20.tar.gz'
    dependencies = [
        'tools::libtool',
        'glib-devel',
        ]
    def compile (self):
        self.system ('cd %(builddir)s && make CC=gcc CPPFLAGS=-I. gen_art_config')
        self.system ('cd %(builddir)s && cp %(srcdir)s/libart.def .')
        target.AutoBuild.compile (self)
