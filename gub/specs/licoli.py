from gub import target

class Licoli (target.AutoBuild):
    source = 'http://lilypond.org/download/gub-sources/licoli-0.1.tar.gz'
    dependencies = ['tools::libtool']
    subpackage_names = ['']

class Licoli__mingw (Licoli):
    def compile (self):
        Licoli.compile (self)
        self.system ('cd %(builddir)s && make -C src test.exe')
