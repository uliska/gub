from gub import tools
from gub import build

class Fonts_dejavu (build.BinaryBuild):
    source = 'http://sourceforge.net/projects/dejavu/files/dejavu/2.35/dejavu-fonts-ttf-2.35.tar.bz2'
    dependencies = ['tools::bzip2']
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/truetype/dejavu')
        self.system ('cp %(srcdir)s/ttf/*.ttf %(install_prefix)s/share/fonts/truetype/dejavu/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_dejavu__tools (tools.AutoBuild, Fonts_dejavu):
    pass
