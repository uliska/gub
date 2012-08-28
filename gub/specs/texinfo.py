from gub import tools

class Texinfo__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/pub/gnu/texinfo/texinfo-4.13a.tar.gz'
    patches = [
        'texinfo-texi2dvi-4.13a.patch',
        ]
    def patch (self):
        tools.AutoBuild.patch (self)
        # Drop ncurses dependency
        self.file_sub ([(' info ',' ')], '%(srcdir)s/Makefile.in')
    def autoupdate (self):
        # We don't want to rebuild Texinfo man pages
        # 
        tools.AutoBuild.autoupdate (self)
        self.system ('''
cd %(srcdir)s && touch doc/*.1
''')
