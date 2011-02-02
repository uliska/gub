from gub import tools

class Gnulib__tools (tools.BinaryBuild):
    source = 'http://lilypond.org/download/gub-sources/gnulib-0.0.6491120.tar.gz'
    def untar (self):
        tools.BinaryBuild.untar (self)
        prefix = self.expand ('%(system_prefix)s')
        refix = prefix[1:]
        first = refix[:refix.index ('/')]
        self.system ('''
cd %(srcdir)s && mkdir -p .%(refix)s/share/gnulib
cd %(srcdir)s && mv * .%(refix)s/share/gnulib
cd %(srcdir)s && mv .%(first)s %(first)s
''', locals ())
