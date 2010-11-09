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
#    force_autoupdate = True
    configure_flags = target.AutoBuild.configure_flags + ' --disable-Werror'
    subpackage_names = ['']
    def patch (self):
        self.system ('''cd %(srcdir)s && scripts/configure-packages guile-gnome-schikkers''')
        self.dump ('''xgconf-guile-gnome-schikkers: atk cairo defs gconf glib gtk libglade libgnomecanvas pango
guile-gnome-schikkers: atk cairo defs glib gtk libglade libgnomecanvas pango
''',
                   '%(srcdir)s/PACKAGES', mode='a')
        self.system ('cd %(srcdir)s && scripts/configure-packages guile-gnome-schikkers')
        target.AutoBuild.patch (self)
    def autoupdate (self):
        self.system ('cd %(srcdir)s && NOCONFIGURE=1 ./autogen.sh')
    configure_binary = '%(builddir)s/configure'
    def configure (self):
        self.shadow ()
        target.AutoBuild.configure (self)
        self.file_sub ([('(GUILE_CAIRO_CFLAGS.*cairo ) ', r'\1 -I%(system_prefix)s/include/guile-cairo ')], '%(builddir)s/config.status', must_succeed=True)
        self.system ('cd %(builddir)s && ./config.status')
    def install (self):
        target.AutoBuild.install (self)
        self.dump ('''
prependdir GUILE_LOAD_PATH=$INSTALLER_PREFIX/share/guile-gnome-2
''',
                   '%(install_prefix)s/etc/relocate/guile-gnome.reloc',
                   env=locals ())
        self.dump ('''
(define (get-prefix-dir) (dirname (dirname (car (command-line)))))
(define *guile-gnome-gobject-lib-path* (string-append (get-prefix-dir) "/lib/libguile-gnome-gobject-2"))
''',
                   '%(install_prefix)s/share/guile-gnome-2/gnome/gobject/config.scm',
                   mode='a')
        ## share/guile/site/gnome-2.scm
        self.file_sub ([('([(]define version "2"[)])', r'\1\n(define (get-prefix-dir) (dirname (dirname (car (command-line)))))')],
                       '%(install_prefix)s/share/guile/site/gnome-2.scm', must_succeed=True)
        self.file_sub ([('dir "/usr(/.*")', r'dir (string-append (get-prefix-dir) "\1)')],
                       '%(install_prefix)s/share/guile/site/gnome-2.scm', must_succeed=True)

class Guile_gnome__mingw (Guile_gnome):
    patches = [
        'guile-gnome-mingw.patch',
        ]

class Guile_gnome__tools (tools.AutoBuild, Guile_gnome):
    pass

