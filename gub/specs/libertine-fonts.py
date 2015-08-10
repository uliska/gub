from gub import tools
from gub import build

class Libertine_fonts (build.BinaryBuild):
    source = 'http://sourceforge.net/projects/linuxlibertine/files/linuxlibertine/5.3.0/LinLibertineOTF_5.3.0_2012_07_02.tgz&strip=0'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/linux-libertine')
        self.system ('cp %(srcdir)s/* %(install_prefix)s/share/fonts/opentype/linux-libertine/')
    def package (self):
        build.AutoBuild.package (self)

class Libertine_fonts__tools (tools.AutoBuild, Libertine_fonts):
    pass
