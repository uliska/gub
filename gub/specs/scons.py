from gub import tools

class Scons__tools (tools.PythonBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/scons/scons-0.98.4.tar.gz'
    def license_files (self):
        return ['%(srcdir)s/LICENSE.txt']
