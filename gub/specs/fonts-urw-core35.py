from gub import tools
from gub import build

class Fonts_urw_core35 (build.BinaryBuild):
    # http://git.ghostscript.com/?p=urw-core35-fonts.git;a=commit;h=c983ed400dc278dcf20bdff68252fad6d9db7af9
    revision = 'c983ed400dc278dcf20bdff68252fad6d9db7af9'
    source = 'git://git.ghostscript.com/urw-core35-fonts.git&revision=' + revision
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/type1/urw-core35')
        self.system ('cp %(srcdir)s/*.afm %(install_prefix)s/share/fonts/type1/urw-core35/')
        self.system ('cp %(srcdir)s/*.pf? %(install_prefix)s/share/fonts/type1/urw-core35/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_urw_core35__tools (tools.AutoBuild, Fonts_urw_core35):
    pass
