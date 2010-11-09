from gub import target

class Guile_library (target.AutoBuild):
    source = 'http://download.gna.org/guile-lib/guile-lib-0.1.6.tar.gz'
    dependencies = [
        'guile',
        ]
    subpackage_names = ['']
