from gub import build

class W32api (build.BinaryBuild, build.SdkBuild):
    source = 'http://sourceforge.net/projects/mingw/files/MinGW/Base/w32api/w32api-3.17/w32api-3.17-2-mingw32-dev.tar.lzma&strip=0'
    dependencies = [ 'tools::xzutils' ]
    def install (self):
        self.system ('''
mkdir -p %(install_prefix)s/include
mkdir -p %(install_prefix)s/lib
cd %(srcdir)s/include/ && tar -C %(srcdir)s/include/ -cf - . | tar -C %(install_prefix)s/include/ -xf -
cd %(srcdir)s/lib/ && tar -C %(srcdir)s/lib/ -cf - . | tar -C %(install_prefix)s/lib/ -xf -
rm -fr %(srcdir)s/include/ %(srcdir)s/lib/
''', locals ())
