from gub import target

class Guile_cairo (target.AutoBuild):
    source = 'http://download.gna.org/guile-cairo/guile-cairo-1.4.0.tar.gz'
    dependencies = [
        'guile',
        ]
    subpackage_names = ['']
