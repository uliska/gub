from gub import target

class Libglade (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/libglade/2.6/libglade-2.6.4.tar.gz'
#    patches = [
#        'libglade-cross.patch',
#        ]
#    force_autoupdate = True
#    def aclocal_path (self):
#        return (target.AutoBuild.aclocal_path (self)
#                + ['%(srcdir)s/m4', '%(srcdir)s'])
    def autoupdate (self):
        target.AutoBuild.autoupdate (self)
        # pkg-config is such a brilliant tool, why do these auto*
        # people break its cross compiling features?
        self.file_sub ([(r'(^\s*)PKG_CONFIG=', r'\1XPKG_CONFIG=')], '%(srcdir)s/configure')
    dependencies = [
        'atk',
        'gtk+',
        'libxml2',
        ]

class Libglade__mingw (Libglade):
    def compile (self):
        self.system ('cd %(builddir)s && cp -pv %(srcdir)s/glade/glade.def glade')
        Libglade.compile (self)
