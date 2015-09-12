from gub import tools
from gub import build

class Fonts_gnufreefont (build.BinaryBuild):
    source = 'http://ftp.gnu.org/gnu/freefont/freefont-otf-20120503.tar.gz'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/gnufreefont')
        self.system ('cp %(srcdir)s/*.otf %(install_prefix)s/share/fonts/opentype/gnufreefont/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_gnufreefont__tools (tools.AutoBuild, Fonts_gnufreefont):
    pass
