from gub import target
from gub import tools

class Guile_gnome (target.AutoBuild):
    source = 'git://git.sv.gnu.org/guile-gnome.git'
    dependencies = [
        'guile-cairo',
        'gtk+',
        'g-wrap',
        'gnomecanvas',
        ]
    subpackage_names = ['']
    def patch (self):
        target.AutoBuild.patch (self)
        self.dump ('''guile-gnome-schikkers: atk cairo defs gconf glib gtk libglade libgnomecanvas pango
guile-gnome-xschikkers: atk cairo defs glib gtk libglade libgnomecanvas pango
''',
                   '%(srcdir)s/PACKAGES', mode='a')
    def autoupdate (self):
#        self.system ('''cd %(srcdir)s && scripts/configure-packages guile-gnome-platform''')
#        self.system ('''cd %(srcdir)s && scripts/configure-packages libgnomecanvas''')
#        for i in ('atk', 'cairo' 'glib', 'gtk', 'libglade', 'libgnomecanvas', 'pango',):
#            self.system ('''cd %(srcdir)s && scripts/configure-packages ''' + i)
        self.system ('''cd %(srcdir)s && scripts/configure-packages guile-gnome-schikkers''')
        self.system ('cd %(srcdir)s && NOCONFIGURE=1 ./autogen.sh')

    configure_binary = '%(builddir)s/configure'
    def configure (self):
        self.shadow ()
        target.AutoBuild.configure (self)
        self.file_sub ([('(GUILE_CAIRO_CFLAGS.*cairo ) ', r'\1 -I%(system_prefix)s/include/guile-cairo ')], '%(builddir)s/config.status', must_succeed=True)
        self.system ('cd %(builddir)s && ./config.status')

class Guile_gnome__mingw (Guile_gnome):
    patches = [
        'guile-gnome-mingw.patch',
        ]

class Guile_gnome__tools (tools.AutoBuild, Guile_gnome):
    pass

