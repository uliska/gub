from gub import misc
from gub import target

class LilyPad (target.AutoBuild):
    source = 'http://lilypond.org/download/gub-sources/lilypad-0.0.8-1-src.tar.bz2'
    destdir_install_broken = True
    # FIXME: -DUNICODE is broken, notably for opening files.
    make_flags = ' CPPFLAGS=-UUNICODE'
    license_files = ['']

Lilypad = LilyPad
