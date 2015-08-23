from gub import tools
from gub import build

class Fonts_ipafont (build.BinaryBuild):
    source = 'http://download.forest.impress.co.jp/pub/library/i/ipafont/10483/IPAfont00303.zip'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/ipafont')
        self.system ('cp %(srcdir)s/IPAfont00303/*.ttf %(install_prefix)s/share/fonts/opentype/ipafont/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_ipafont__tools (tools.AutoBuild, Fonts_ipafont):
    pass
