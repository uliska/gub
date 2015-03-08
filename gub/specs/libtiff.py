from gub import target
from gub import tools

class Libtiff (target.AutoBuild):
    source = 'http://dl.maptools.org/dl/libtiff/tiff-3.8.2.tar.gz'
    dependencies = ['tools::libtool', 'libjpeg-devel', 'zlib']

class Libtiff__tools (tools.AutoBuild, Libtiff):
    dependencies = [
            'libtool',
            'libjpeg-devel',
            'zlib',
#            'system::g++',
            ]
    configure_flags = (tools.AutoBuild.configure_flags
                + ' --disable-cxx')
