#
from gub import misc
from gub import target
from gub import tools

class Expat (target.AutoBuild):
    source = 'http://sourceforge.net/projects/expat/files/expat/2.1.0/expat-2.1.0.tar.gz'
    dependencies = ['libtool', 'tools::expat']

class Expat__linux__arm__vfp (Expat):
    patches = []
    source = 'http://sourceforge.net/projects/expat/files/expat/2.0.0/expat-2.0.0.tar.gz'
    def patch (self):
        self.system ('touch %(srcdir)s/tests/xmltest.sh.in')
        target.AutoBuild.patch (self)

class Expat__darwin (Expat):
    dependencies = [x for x in Expat.dependencies
                if x.replace ('-devel', '') not in [
                'libxml2', # Included in darwin-sdk, hmm?
                ]]

class Expat__tools (tools.AutoBuild, Expat):
    dependencies = [
            'automake',
            'libtool',
            ]
