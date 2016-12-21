from gub import target

class Libxinerama (target.AutoBuild):
    source = 'https://xorg.freedesktop.org/releases/X11R7.4/src/lib/libXinerama-1.0.3.tar.gz'
    dependencies = ['tools::libtool', 'libx11-devel', 'xineramaproto-devel']
