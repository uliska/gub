from gub.specs.cross import gcc as cross_gcc
from gub import debian

class Gcc__debian (cross_gcc.Gcc):
    source = 'http://ftp.gnu.org/pub/gnu/gcc/gcc-4.8.2/gcc-4.8.2.tar.bz2'
    dependencies = ['cross/binutils', 'libc6', 'libc6-dev', 'linux-kernel-headers']
    ## TODO: should detect whether libc supports TLS 
    configure_flags = cross_gcc.Gcc.configure_flags + ' --disable-tls '

class Gcc__debian__arm (Gcc__debian):
    source = 'http://ftp.gnu.org/pub/gnu/gcc/gcc-4.8.2/gcc-4.8.2.tar.bz2'
