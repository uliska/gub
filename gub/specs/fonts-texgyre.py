from gub import tools
from gub import build

class Fonts_texgyre (build.BinaryBuild):
    source = 'http://www.gust.org.pl/projects/e-foundry/tex-gyre/whole/tg-2.005bas.zip'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/texgyre')
        self.system ('cp %(srcdir)s/fonts/opentype/public/tex-gyre/*.otf %(install_prefix)s/share/fonts/opentype/texgyre/')
        self.system ('mkdir -p %(install_prefix)s/share/doc/texgyre')
        self.system ('cp %(srcdir)s/doc/fonts/tex-gyre/* %(install_prefix)s/share/doc/texgyre/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_texgyre__tools (tools.AutoBuild, Fonts_texgyre):
    pass
