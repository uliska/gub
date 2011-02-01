from gub import target

class Guile_glib_spawn (target.AutoBuild):
    source = 'http://lilypond.org/download/gub-sources/guile-glib-spawn-0.1.tar.gz'
    dependencies = [
        'guile',
        'glib',
        'tools::libtool',
        ]
    subpackage_names = ['']

class Guile_glib_spawn__mingw (Guile_glib_spawn):
    def install (self):
        Guile_glib_spawn.install (self)
        # dlopen-able .la files go in BIN dir, BIN OR LIB package
        self.system ('''mv %(install_prefix)s/lib/libguile-glib-spawn.la %(install_prefix)s/bin''')
