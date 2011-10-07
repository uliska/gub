from gub import build

class Osx_lilypad (build.NullBuild):
    pass

class Osx_lilypad__darwin__ppc (build.NullBuild):
    # yes, we really need the old version here!
    # 0.5 was built for lion 10.7, which doesn't have any ppc support
    source = 'http://lilypond.org/download/gub-sources/osx-lilypad-universal-0.4.tar.gz'

class Osx_lilypad__darwin__x86 (build.NullBuild):
    source = 'http://lilypond.org/download/gub-sources/osx-lilypad-universal-0.5.tar.gz'
