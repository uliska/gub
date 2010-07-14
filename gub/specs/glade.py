from gub import target

class Glade (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/glade3/3.6/glade3-3.6.7.tar.gz'
    dependencies = [
        'gtk+',
        'libxml2',
        ]

class Glade__mingw (Glade):
    def compile (self):
        self.system ('cd %(builddir)s && cp -pv %(srcdir)s/data/icons/glade-3.ico data/icons')
        Glade.compile (self)
