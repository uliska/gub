from gub import target
from gub import tools

class Lcms (target.AutoBuild):
    source = 'http://sourceforge.net/projects/lcms/files/lcms/1.18/lcms-1.18a.tar.gz'
    dependencies = ['tools::libtool']
    def configure (self):
        target.AutoBuild.configure (self)
        self.system ('rm -f %(srcdir)s/include/icc34.h')

class Lcms__tools (tools.AutoBuild, Lcms):
    def configure (self):
        tools.AutoBuild.configure (self)
        self.system ('rm -f %(srcdir)s/include/icc34.h')
