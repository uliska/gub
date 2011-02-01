from gub import target
from gub import tools

class Libgc (target.AutoBuild):
    source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-7.1.tar.gz'
    configure_flags = target.AutoBuild.configure_flags + '--enable-threads=pthreads '
    #source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc6.8.tar.gz&version=6.8'

class Libgc__linux (Libgc):
    configure_flags = (Libgc.configure_flags
                       + 'CFLAGS=-fno-stack-protector ')

class Libgc__freebsd (Libgc):
    make_flags = 'THREADDLLIBS=-pthread'

class Libgc__freebsd__x86 (Libgc__freebsd):
    source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc6.8.tar.gz&version=6.8'
    #patches = ['libgc-6.8-freebsd-x86_64.patch']

class Libgc__mingw (Libgc):
    dependencies = [
        'pthreads-w32',
        ]
    patches = [
        #'libgc-6.8-mingw-pthreads.patch',
        #'libgc-7.2-mingw-pthreads.patch',
        'libgc-7.2-mingw-threads.patch',
        ]
    force_autoupdate = True
    #source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc6.8.tar.gz&version=6.8'
    source = 'http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-7.2alpha4.tar.gz&version=7.2.4'

class Libgc (tools.AutoBuild, Libgc):
    pass
