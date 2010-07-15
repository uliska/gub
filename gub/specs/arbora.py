import re
#
from gub import misc
from gub import repository
from gub import target

class Arbora (target.PythonBuild):
    '''A program for tree inventory and management
'''
    #source = 'ssh+git://lilypond.org/~/arbora.git'
    source = 'git+file://localhost/home/janneke/vc/arbora'
    branch = 'master'
    subpackage_names = ['']
    dependencies = [
        'elixir',
        'python-gtkmvc',
        'pysqlite',
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

class Arbora__mingw (Arbora):
    def install (self):
        Arbora.install (self)
        self.system ('cd %(install_prefix)s/bin && cp -pv arbora run-arbora.py')
