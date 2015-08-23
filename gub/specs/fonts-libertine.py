from gub import tools
from gub import build

class Fonts_libertine (build.BinaryBuild):
    source = 'http://sourceforge.net/projects/linuxlibertine/files/linuxlibertine/5.3.0/LinLibertineOTF_5.3.0_2012_07_02.tgz&strip=0'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/linux-libertine')
        self.system ('cp %(srcdir)s/*.otf %(install_prefix)s/share/fonts/opentype/linux-libertine/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_libertine__tools (tools.AutoBuild, Fonts_libertine):
    pass
