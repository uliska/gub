import download
import targetpackage

class Regex (targetpackage.TargetBuildSpec):
    def __init__ (self, settings):
        targetpackage.TargetBuildSpec.__init__ (self, settings)
        self.with (version='2.3.90-1', mirror=download.hw, format='bz2')

    def license_file (self):
        return '%(srcdir)s/COPYING.LIB'
