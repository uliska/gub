from gub import target

class Licoli (target.AutoBuild):
    source = 'http://lilypond.org/downloads/gub-sources/licoli-0.1.2.tar.gz'
    dependencies = ['tools::libtool']
    subpackage_names = ['']

class Licoli__mingw (Licoli):
    def compile (self):
        Licoli.compile (self)
        self.system ('cd %(builddir)s && make -C src test.exe')
    def install (self):
        Licoli.install (self)
        self.system ('cp -pv %(builddir)s/src/test.exe %(install_prefix)s/bin/test-licoli.exe')
