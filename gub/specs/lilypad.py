from gub import misc
from gub import target

class LilyPad (target.AutoBuild):
    source = 'http://lilypond.org/download/gub-sources/lilypad/lilypad-0.1.2.0-src.tar.bz2'
    dependencies = [ 'tools::automake' ]
    destdir_install_broken = True
    license_files = ['']

Lilypad = LilyPad
