from gub import tools
from gub import build

class Fonts_texgyre (build.BinaryBuild):
    source = 'http://www.gust.org.pl/projects/e-foundry/tex-gyre/whole/tg-2.005otf.zip'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/texgyre')
        self.system ('cp %(srcdir)s/*.otf %(install_prefix)s/share/fonts/opentype/texgyre/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_texgyre__tools (tools.AutoBuild, Fonts_texgyre):
    pass
