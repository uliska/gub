from gub import build

class Mingwrt_dev (build.BinaryBuild, build.SdkBuild):
    source = 'http://downloads.sourceforge.net/project/mingw/MinGW/Base/mingw-rt/mingwrt-3.20/mingwrt-3.20-mingw32-dev.tar.gz&strip=0'
    def install (self):
        self.system ('''
mkdir -p %(install_prefix)s/share
cd %(srcdir)s && tar -C %(srcdir)s/ -cf - . | tar -C %(install_prefix)s -xf -
mkdir -p %(install_prefix)s/include/sys
#cp -p %(sourcefiledir)s/mingw-headers/wait.h %(install_prefix)s/include/sys
mv %(install_prefix)s/doc %(install_root)s/share
''', locals ())
