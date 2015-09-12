from gub import tools

class Scons__tools (tools.PythonBuild):
    source = 'http://sourceforge.net/projects/scons/files/scons/1.0.0/scons-1.0.0.tar.gz'
    license_files = ['%(srcdir)s/LICENSE.txt']
