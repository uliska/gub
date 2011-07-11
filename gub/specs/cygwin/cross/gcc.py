#
from gub.specs.cross import gcc as cross_gcc
from gub import cygwin
from gub import misc

# http://gcc.gnu.org/PR24196
#class this_works_but_has_string_exception_across_dll_bug_Gcc__cygwin (cross_gcc.Gcc__mingw):
class Gcc__cygwin (cross_gcc.Gcc__mingw):
#    source = 'http://ftp.gnu.org/pub/gnu/gcc/gcc-4.1.2/gcc-4.1.2.tar.bz2'
    source = 'http://ftp.gnu.org/pub/gnu/gcc/gcc-4.3.4/gcc-4.3.4.tar.bz2'
    patches = cross_gcc.Gcc__mingw.patches + [
        'gcc-4.3.4-strsignal-cygwin.patch',
        ]
    dependencies = (cross_gcc.Gcc__mingw.dependencies
                    + ['cygwin',
                       'libiconv',
                       'libmpfr-devel',
#                       'tools::mpfr', # ugh: use apt-get install libmpfr-dev
                       'w32api-in-usr-lib'])
    configure_flags = (cross_gcc.Gcc__mingw.configure_flags
                       + misc.join_lines ('''
--with-newlib
--enable-threads
'''))
    make_flags = misc.join_lines ('''
tooldir="%(cross_prefix)s/%(target_architecture)s"
gcc_tooldir="%(cross_prefix)s/%(target_architecture)s"
''')

#class okGcc__cygwin (cross_gcc.Gcc):
class above_is_okay_now_cygwin_has_switched_Gcc__cygwin (cross_gcc.Gcc):
    source = 'http://ftp.gnu.org/pub/gnu/gcc/gcc-3.4.4/gcc-3.4.4.tar.bz2'
    patches = ['gcc-3.4.4-cygwin-3.patch']
    dependencies = (cross_gcc.Gcc.dependencies
                    + ['cygwin', 'w32api-in-usr-lib'])
    # We must use --with-newlib, otherwise configure fails:
    # No support for this host/target combination.
    # [configure-target-libstdc++-v3]
    configure_flags = (cross_gcc.Gcc.configure_flags
                + misc.join_lines ('''
--with-newlib
--verbose
--enable-nls
--without-included-gettext
--enable-version-specific-runtime-libs
--without-x
--enable-libgcj
--with-system-zlib
--enable-interpreter
--disable-libgcj-debug
--enable-threads=posix
--disable-win32-registry
--enable-sjlj-exceptions
--enable-hash-synchronization
--enable-libstdcxx-debug
'''))
