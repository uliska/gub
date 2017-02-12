from gub import target

class Xineramaproto (target.AutoBuild):
    source = 'https://xorg.freedesktop.org/releases/X11R7.4/src/proto/xineramaproto-1.1.2.tar.gz'
    dependencies = ['tools::libtool']
