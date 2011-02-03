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
    patches = [
        #'0001-Revert-Enable-images-and-toolbar.-Move-patching-out-.patch',
        ]
    branch = 'master'
    subpackage_names = ['']
    dependencies = [
        'guile-gnome',
        'guile-library',
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
        self.dump ('''
prependdir GUILE_LOAD_PATH=$INSTALLER_PREFIX/share/guile/site
prependdir PATH=$INSTALLER_PREFIX/bin
''',
                   '%(install_prefix)s/etc/relocate/schikkers-list.reloc',
                   env=locals ())
        self.file_sub ([(' guile-gnome-2 ', ' $(dirname $0)/guile '),
                        (' -L [$][(]dirname [$]0[)]', ''),
                        ],
                       '%(install_prefix)s/bin/ikli', must_succeed=True)
        self.system ('cd %(install_prefix)s/bin && rm -f ikli')

class Schikkers_list__mingw (Schikkers_list):
    dependencies = Schikkers_list.dependencies + [
        'guile-glib-spawn',
        ]
    def install (self):
        Schikkers_list.install (self)
        self.system ('cd %(install_prefix)s/bin && rm -f ikli')
        self.system ('cd %(install_prefix)s/bin && mv schikkers-list schikkers-list.scm')
