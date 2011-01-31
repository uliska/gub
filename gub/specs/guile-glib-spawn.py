from gub import target

class Guile_glib_spawn (target.AutoBuild):
    source = 'http://lilypond.org/download/gub-sources/guile-glib-spawn-0.1.tar.gz'
    dependencies = [
        'guile',
        'glib',
        'tools::libtool',
        ]
    subpackage_names = ['']
