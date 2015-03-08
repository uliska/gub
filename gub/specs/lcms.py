from gub import target
from gub import tools

class Lcms (target.AutoBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/lcms/lcms-1.18.tar.gz'
    #source = 'http://www.littlecms.com/lcms/2.1/lcms2-2.1.tar.gz/
    dependencies = ['tools::libtool']
    def configure (self):
        target.AutoBuild.configure (self)
        self.system ('rm -f %(srcdir)s/include/icc34.h')

class Lcms__tools (tools.AutoBuild, Lcms):
    def configure (self):
        tools.AutoBuild.configure (self)
        self.system ('rm -f %(srcdir)s/include/icc34.h')
