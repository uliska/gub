from toolpackage import ToolBuildSpecification
import download

class Flex (ToolBuildSpecification):
    def srcdir (self):
        return '%(allsrcdir)s/flex-2.5.4'

    def install_command (self):
        return self.broken_install_command ()
        
    def patch (self):
        self.system ("cd %(srcdir)s && patch -p1 < %(patchdir)s/flex-2.5.4a-FC4.patch")

    def __init__ (self, settings):
        ToolBuildSpecification.__init__ (self, settings)
        self.with (version="2.5.4a",
             mirror=download.nongnu, format='gz'),
