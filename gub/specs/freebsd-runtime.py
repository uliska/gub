from gub import build

class Freebsd_runtime (build.BinaryBuild, build.SdkBuild):
    source = 'http://lilypond.org/downloads/gub-sources/freebsd-runtime/freebsd-runtime-6.2-1.%(package_arch)s.tar.gz&strip=0'
    def untar (self):
        build.BinaryBuild.untar (self)
        self.system ('''
# blocks installing db, and runtime lacks binary libdb.*
rm -f %(srcdir)s%(prefix_dir)s/include/db.h
# blocks installing flex, and runtime lacks binary flex, liby.*
rm -f %(srcdir)s%(prefix_dir)s/include/FlexLexer.h
''')

class Freebsd_runtime__freebsd__64 (Freebsd_runtime):
    source = 'http://lilypond.org/downloads/gub-sources/freebsd-runtime/freebsd-runtime-6.2-2.%(package_arch)s.tar.gz&strip=0'
