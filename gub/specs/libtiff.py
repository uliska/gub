from gub import target
from gub import tools

class Libtiff (target.AutoBuild):
    source = 'http://download.osgeo.org/libtiff/tiff-4.0.3.tar.gz'
    dependencies = ['tools::libtool', 'libjpeg-devel', 'zlib-devel']

class Libtiff__tools (tools.AutoBuild, Libtiff):
    dependencies = [
            'libtool',
            'libjpeg-devel',
            'zlib-devel',
#            'system::g++',
            ]
    configure_flags = (tools.AutoBuild.configure_flags
                + ' --disable-cxx')
