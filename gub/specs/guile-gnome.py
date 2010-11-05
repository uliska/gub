from gub import target
from gub import tools

class Guile_gnome (target.AutoBuild):
    dependencies = [
        'guile-cairo',
        'gtk+',
        'g-wrap',
        ]
    source = 'git://git.sv.gnu.org/guile-gnome.git'
    def autoupdate (self):
        self.system ('''cd %(srcdir)s && scripts/configure-packages guile-gnome-platform''')
        self.system ('''cd %(srcdir)s && scripts/configure-packages libgnomecanvas''')
        self.system ('cd %(srcdir)s && NOCONFIGURE=1 sh ./autogen.sh')

    configure_binary = '%(builddir)s/configure'
    def configure (self):
        self.shadow ()
        target.AutoBuild.configure (self)

class Guile_gnome__mingw (Guile_gnome):
    patches = [
        'guile-gnome-mingw.patch',
        ]

class Guile_gnome__tools (tools.AutoBuild, Guile_gnome):
    pass

