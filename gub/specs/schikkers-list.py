import re
#
from gub import misc
from gub import repository
from gub import target

class Schikkers_list (target.PythonBuild):
    '''A program for tree inventory and management
'''
    #source = 'git://github.com/janneke/schikkers-list.git'
    source = 'git+file://localhost/home/janneke/vc/schikkers-list'
    branch = 'master'
    subpackage_names = ['']
    dependencies = [
        'guile-gnome',
        'lilypondcairo',
        ]
    def __init__ (self, settings, source):
        target.PythonBuild.__init__ (self, settings, source)
        if isinstance (source, repository.Git):
            def version_from_NEWS (self, file_name='NEWS', default_version='0.0.0'):
                try:
                    news = self.read_file (file_name)
                    return re.match ('^RELEASE v(([0-9]+[.]){2}[0-9]+)', news).group (1)
                except:
                    return default_version
            source.version = misc.bind_method (version_from_NEWS, source)
    def compile (self):
        self.system ('mkdir -p %(builddir)s')
    def install (self):
        target.PythonBuild.install (self)
        self.system ('cd %(install_prefix)s/bin && cp -pv ikli schikkers-list')

class Schikkers_list__mingw (Schikkers_list):
    def install (self):
        Schikkers_list.install (self)
        self.system ('cd %(install_prefix)s/bin && cp -pv ikli run-ikli.scm')
        self.system ('cd %(install_prefix)s/bin && cp -pv schikkers-list schikkers-list.scm')
