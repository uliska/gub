from gub import build

class Mingwrt_dll (build.BinaryBuild, build.SdkBuild):
    source = 'http://downloads.sourceforge.net/project/mingw/MinGW/Base/mingw-rt/mingwrt-3.20/mingwrt-3.20-mingw32-dll.tar.gz&strip=0'
    def install (self):
        self.system ('''
rm -fr %(srcdir)s/doc/
mkdir -p %(install_prefix)s/bin/
cd %(srcdir)s/bin/ && tar -C %(srcdir)s/bin/ -cf - . | tar -C %(install_prefix)s/bin/ -xf -
''', locals ())
