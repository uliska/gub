from gub import target

class Guile_library (target.AutoBuild):
    source = 'http://download.savannah.gnu.org/releases/guile-lib/guile-lib-0.1.9.tar.gz'
    dependencies = [
        'guile',
        ]
    subpackage_names = ['']
