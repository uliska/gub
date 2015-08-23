from gub import tools
from gub import build

class Fonts_luximono (build.BinaryBuild):
    source = 'http://mirrors.ctan.org/fonts/LuxiMono.zip'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/type1/luximono')
        self.system ('cp %(srcdir)s/LuxiMono/*.afm %(install_prefix)s/share/fonts/type1/luximono/')
        self.system ('cp %(srcdir)s/LuxiMono/*.pf? %(install_prefix)s/share/fonts/type1/luximono/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_luximono__tools (tools.AutoBuild, Fonts_luximono):
    pass
