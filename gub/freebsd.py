from gub import context
from gub import cross
from gub import misc

def get_cross_build_dependencies (settings):
    return ['cross/gcc', 'freebsd-runtime']

def change_target_package (package):
    cross.change_target_package (package)

    @context.subst_method
    def rpath (foo):
        return ''
    if not isinstance (package, cross.AutoBuild):
        package.rpath = misc.MethodOverrider (package.nop, rpath)

# FIXME: download from sane place; or rather download only kernel
# headers and build full toolchain from source?
def get_sdk ():
    '''
#! /bin/bash

if test $# != '3'; then
    cat <<EOF
Usage: get-freebsd ARCH VERSION BUILD

Example:
  bash get-freebsd i386 6.2 1
  bash get-freebsd amd64 6.2 2
EOF
    exit 2
fi

arch=$1
version=$2
build=$3

tmp=tmp-freebsd-$arch-$version-$build
mkdir -p $tmp && cd $tmp
wget ftp://ftp-archive.freebsd.org/pub/FreeBSD-Archive/old-releases/$arch/$version-RELEASE/base/base.??
rm -rf root
mkdir -p root
cat base.?? | tar --unlink -xpzf - -C root
cd root && tar --exclude=zlib.h --exclude=zconf.h --exclude=gmp.h --exclude=curses.h --exclude=ncurses.h --exclude=c++ --exclude=g++ -czf ../../downloads/freebsd-runtime/freebsd-runtime-$version-$build.$arch.tar.gz {,usr/}lib/{lib{c,c_r,m,pthread}{.a,.so{,.*}},crt{i,n,1}.o} usr/include
#rm -rf $tmp
'''
