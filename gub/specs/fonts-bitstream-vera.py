from gub import tools
from gub import build

class Fonts_bitstream_vera (build.BinaryBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/ttf-bitstream-vera/1.10/ttf-bitstream-vera-1.10.tar.bz2'
    dependencies = ['tools::bzip2']
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/truetype/bitstream/vera')
        self.system ('cp %(srcdir)s/*.ttf %(install_prefix)s/share/fonts/truetype/bitstream/vera/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_bitstream_vera__tools (tools.AutoBuild, Fonts_bitstream_vera):
    pass
