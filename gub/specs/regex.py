from gub import target

class Regex (target.AutoBuild):
    source = 'http://lilypond.org/downloads/gub-sources/regex/regex-2.3.90-1.tar.bz2'
    dependencies = ['tools::libtool']
