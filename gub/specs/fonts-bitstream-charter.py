from gub import tools
from gub import build

class Fonts_bitstream_charter (build.BinaryBuild):
    source = 'http://mirrors.ctan.org/fonts/charter.zip'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/type1/bitstream/charter')
        self.system ('cp %(srcdir)s/charter/*.afm %(install_prefix)s/share/fonts/type1/bitstream/charter/')
        self.system ('cp %(srcdir)s/charter/*.pf? %(install_prefix)s/share/fonts/type1/bitstream/charter/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_bitstream_charter__tools (tools.AutoBuild, Fonts_bitstream_charter):
    pass
