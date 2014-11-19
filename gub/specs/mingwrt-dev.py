from gub import build

class Mingwrt_dev (build.BinaryBuild, build.SdkBuild):
    source = 'http://downloads.sourceforge.net/project/mingw/MinGW/Base/mingw-rt/mingwrt-3.20/mingwrt-3.20-mingw32-dev.tar.gz&strip=0'
    def install (self):
        self.system ('''
mkdir -p %(install_prefix)s/include
mkdir -p %(install_prefix)s/lib
mkdir -p %(install_prefix)s/share/doc
cd %(srcdir)s/include/ && tar -C %(srcdir)s/include/ -cf - . | tar -C %(install_prefix)s/include/ -xf -
cd %(srcdir)s/lib/ && tar -C %(srcdir)s/lib/ -cf - . | tar -C %(install_prefix)s/lib/ -xf -
cd %(srcdir)s/share/ && tar -C %(srcdir)s/share/ -cf - . | tar -C %(install_prefix)s/share/ -xf -
cd %(srcdir)s/doc/ && tar -C %(srcdir)s/doc/ -cf - . | tar -C %(install_prefix)s/share/doc/ -xf -
mkdir -p %(install_prefix)s/include/sys
#cp -p %(sourcefiledir)s/mingw-headers/wait.h %(install_prefix)s/include/sys
rm -fr %(srcdir)s/include/ %(srcdir)s/lib/ %(srcdir)s/share/ %(srcdir)s/doc/
''', locals ())
