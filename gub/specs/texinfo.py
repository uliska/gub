from gub import tools

class Texinfo__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/gnu/texinfo/texinfo-5.2.tar.xz'
    dependencies = [ 'tools::xzutils' ]
    def patch (self):
        tools.AutoBuild.patch (self)
        # Drop ncurses dependency
        self.file_sub ([(' info ',' ')], '%(srcdir)s/Makefile.in')
