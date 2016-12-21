from gub import target

class Inputproto (target.AutoBuild):
    source = 'https://xorg.freedesktop.org/releases/X11R7.4/src/everything/inputproto-1.4.4.tar.gz'
    dependencies = ['tools::libtool']
