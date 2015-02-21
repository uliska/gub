from gub import tools

class Texinfo__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/pub/gnu/texinfo/texinfo-4.13a.tar.gz'
    patches = ['texinfo-4.13a-fix-bashism.patch']
    def patch (self):
        tools.AutoBuild.patch (self)
        # Drop ncurses dependency
        self.file_sub ([(' info ',' ')], '%(srcdir)s/Makefile.in')
        # Avoid man rebuild
        self.system('''
touch %(srcdir)s/doc/texi2dvi.1
touch %(srcdir)s/doc/texi2pdf.1
touch %(srcdir)s/doc/pdftexi2dvi.1
''')
