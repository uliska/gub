import os
#
from gub import context
from gub import misc
from gub import loggedos
from gub import octal
from gub import repository
from gub import target
from gub import tools
from gub import tools32

class Guile (target.AutoBuild):
    # source = 'git://git.sv.gnu.org/guile.git&branch=branch_release-1-8&revision=bba579611b3671c7e4c1515b100f01c048a07935'
    source = 'http://ftp.gnu.org/pub/gnu/guile/guile-1.8.7.tar.gz'
    source = 'http://alpha.gnu.org/gnu/guile/guile-1.9.15.tar.gz'
    patches = [
        #'guile-reloc-1.8.6.patch',
        'guile-1.9.14-reloc.patch',
        #'guile-cexp.patch',
        'guile-1.8.6-test-use-srfi.patch',
        #'guile-1.8.7-doc-snarfing.patch',
        'guile-1.9.14-configure-cross.patch',
        'guile-1.9.15-cross.patch',
        'guile-1.9.14-gnulib-libunistring.patch',
        #'guile-1.9.14-gnulib-libunistring-retooled.patch',
        ]
    force_autoupdate = True
    dependencies = [
        'gettext-devel',
        'gmp-devel',
        'libtool',
        'libffi',
        'libunistring',
        'libgc',
        'tools::guile',
        'tools::gnulib',
        'tools::pkg-config',
        ]
    guile_configure_flags = misc.join_lines ('''
--without-threads
--with-gnu-ld
--enable-deprecated
--enable-discouraged
--disable-error-on-warning
--enable-relocation
--enable-rpath
--with-pic
''')
    configure_variables = (target.AutoBuild.configure_variables
                           + misc.join_lines ('''
CC_FOR_BUILD="
LD_PRELOAD=
C_INCLUDE_PATH=
CPPFLAGS=
LIBRARY_PATH=
PATH_SEPARATOR=':'
PATH=/usr/bin:$PATH
/usr/bin/cc
-I%(builddir)s
-I%(srcdir)s
-I%(builddir)s/libguile
-I.
-I%(srcdir)s/libguile"
'''))
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
gl_cv_func_svid_putenv=yes
'''
    # FIXME: guile runs gen_scmconfig [when not x-building also guile]
    # without setting the proper LD_LIBRARY_PATH.
    compile_flags_native = (' LD_PRELOAD= '
                            + ' LD_LIBRARY_PATH=%(tools_prefix)s/lib:${LD_LIBRARY_PATH-/foe} '
                            + ' CFLAGS="-I%(srcdir)s -I%(builddir)s -DHAVE_CONFIG_H=1"'
                            + ' LIBFFI_CFLAGS='
                            + ' LDFLAGS='
                            + ' cross_compiling=yes ')
    # FIXME: guile runs gen_scmconfig [when not x-building also guile]
    # without setting the proper LD_LIBRARY_PATH.
    configure_command = ('GUILE_FOR_BUILD=%(tools_archmatch_prefix)s/bin/guile '
                         + target.AutoBuild.configure_command
                         + guile_configure_flags)
    compile_command = ('export preinstguile=%(tools_archmatch_prefix)s/bin/guile; '
                       + target.AutoBuild.compile_command)
    install_command = ('export preinstguile=%(tools_archmatch_prefix)s/bin/guile; '
                       + target.AutoBuild.install_command)
    subpackage_names = ['doc', 'devel', 'runtime', '']
    @staticmethod
    def version_from_VERSION (self):
        return self.version_from_shell_script ('GUILE-VERSION',
                                               'GUILE_MAJOR_VERSION',
                                               '%(GUILE_MAJOR_VERSION)s.%(GUILE_MINOR_VERSION)s.%(GUILE_MICRO_VERSION)s',
                                               '1.8.6')
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        if isinstance (source, repository.Git):
            ##source.version = lambda: '1.8.6'
            source.version = misc.bind_method (Guile.version_from_VERSION,
                                               source)
        self.so_version = '17'
    # REMOVE putenv!
    gnulib_modules = 'alignof alloca-opt announce-gen autobuild byteswap canonicalize-lgpl duplocale environ extensions flock fpieee full-read full-write func gendocs getaddrinfo git-version-gen gitlog-to-changelog gnu-web-doc-update gnupload havelib iconv_open-utf inet_ntop inet_pton isinf isnan lib-symbol-versions lib-symbol-visibility libunistring locale maintainer-makefile nproc stat-time stdlib strcase strftime striconveh string sys_stat verify version-etc-fsf vsnprintf warnings     '
    def patch (self):
        self.dump ('''#!/bin/sh
exec %(tools_archmatch_prefix)s/bin/guile "$@"
''', "%(srcdir)s/pre-inst-guile.in")
        #self.autopatch ()
        self.system ('cp -pv %(sourcefiledir)s/fcntl-o.m4 %(srcdir)s/m4')
        self.system ('%(tools_prefix)s/share/gnulib/gnulib-tool --import --dir=%(srcdir)s --lib=libgnu --source-base=lib --m4-base=m4 --doc-base=doc --tests-base=tests --aux-dir=build-aux --libtool --macro-prefix=gl --no-vc-files %(gnulib_modules)s')
        target.AutoBuild.patch (self)
        self.file_sub ([('putenv', 'gnulib_putenv')], '%(srcdir)s/lib/putenv.c')
        self.file_sub ([('putenv', 'gnulib_putenv')], '%(srcdir)s/lib/stdlib.in.h')
    def autoupdate (self):
        self.system ('cd %(srcdir)s && autoreconf')
        # .libs/libguile_2.0_la-arbiters.o: In function `__gmpz_abs':
        # arbiters.c:(.text+0x0): multiple definition of `__gmpz_abs'
        self.file_sub ([('-std=gnu99', ''),('-std=c99', '')], '%(srcdir)s/configure')
        self.file_sub ([('cross_compiling=(maybe|no|yes)',
                         'cross_compiling=yes')], '%(srcdir)s/configure')
    def autopatch (self):
        self.file_sub ([(r'AC_CONFIG_SUBDIRS\(guile-readline\)', '')],
                       '%(srcdir)s/configure.in')
        self.file_sub ([(r'guile-readline', '')],
                       '%(srcdir)s/Makefile.am')
        # Guile [doc] does not compile with dash *and* not with
        # librestrict-stat.so; patch out.
        if isinstance (self.source, repository.Git):
            self.file_sub ([(' doc ', ' ')], '%(srcdir)s/Makefile.am')
            self.file_sub ([('guile-readline', '')], '%(srcdir)s/Makefile.am')
        else:
            self.file_sub ([(' doc ', ' ')], '%(srcdir)s/Makefile.in')
            self.file_sub ([('guile-readline', '')], '%(srcdir)s/Makefile.in')
        self.dump ('', '%(srcdir)s/doc/ref/version.texi')
        self.dump ('', '%(srcdir)s/doc/tutorial/version.texi')
    def compile (self):
        ## Ugh: broken dependencies break parallel build with make -jX
        self.system ('cd %(builddir)s/libguile && make %(compile_flags_native)s gen-scmconfig guile_filter_doc_snarfage')
        # Remove -L %(system_root)s from `guile-config link'
        self.system ('cd %(builddir)s/libguile && make %(compile_flags_native)slibpath.h')
        self.file_sub ([('''-L *%(system_root)s''', '-L')],
                       '%(builddir)s/libguile/libpath.h')
        target.AutoBuild.compile (self)
    def install (self):
        # with 1.8.7: libtool: cannot install directory not ending in...
        # after config.status is being re-run for building of libpath.h
        self.update_libtool ()
        target.AutoBuild.install (self)
        majmin_version = '.'.join (self.expand ('%(version)s').split ('.')[0:2])
        majmin_version = '2.0'
        
        self.dump ('''
prependdir GUILE_LOAD_PATH=$INSTALLER_PREFIX/share/guile/%(majmin_version)s
prependdir GUILE_LOAD_PATH=$INSTALLER_PREFIX/share/guile/site
prependdir GUILE_LOAD_COMPILED_PATH=$INSTALLER_PREFIX/lib/guile/%(majmin_version)s/ccache
''',
                   '%(install_prefix)s/etc/relocate/guile.reloc',
                   env=locals ())
        version = self.expand ('%(version)s')
        #FIXME: c&p linux.py
        self.dump ('''\
#! /bin/sh
test "$1" = "--version" && echo "%(target_architecture)s-guile-config - Guile version %(version)s"
prefix=%(system_prefix)s
test "$1" = "compile" && echo "-I$prefix/include/guile/2.0"
test "$1" = "link" && echo "-L$prefix/lib -lguile-2.0 -lgmp"
test "$1" = "info" && test "$2" = "guileversion" && echo "%(version)s"
exit 0
''',
             '%(install_prefix)s%(cross_dir)s/bin/%(target_architecture)s-guile-config')
        self.chmod ('%(install_prefix)s%(cross_dir)s/bin/%(target_architecture)s-guile-config', octal.o755)
        self.system ('cd %(install_prefix)s%(cross_dir)s/bin && cp -pv %(target_architecture)s-guile-config guile-config')

class Guile__mingw (Guile):
    def __init__ (self, settings, source):
        Guile.__init__ (self, settings, source)
        # Configure (compile) without -mwindows for console
        self.target_gcc_flags = '-mms-bitfields'
    patches = Guile.patches + [ # [x for x in Guile.patches if not 'libunistring' in x] + [
        'guile-1.9.15-mingw.patch',
        'guile-1.9.14-gnulib-mingw.patch',
        'guile-1.9.14-mingw-dirent.patch',
        #'guile-1.9.14-gnulib-libunistring-retooled.patch',
        ]
    dependencies = (Guile.dependencies
                    + [
            'regex-devel',
            'mingw-extras',
            ])
    configure_flags = (Guile.configure_flags
                       + ' --without-threads')
    configure_variables = (Guile.configure_variables
                           .replace ("':'", "';'")
###we're debugging here
###CFLAGS='-O2 -DHAVE_CONFIG_H=1 -I%(builddir)s'
                + misc.join_lines ('''
CFLAGS='-g -DHAVE_CONFIG_H=1 -I%(builddir)s'
LIBS='-lgc -lmingw-extras'
'''))
    config_cache_overrides = Guile.config_cache_overrides + '''
gl_cv_socket_ipv6=no
guile_cv_have_ipv6=no
scm_cv_struct_timespec=${scm_cv_struct_timespec=no}
guile_cv_func_usleep_declared=${guile_cv_func_usleep_declared=yes}
guile_cv_exeext=${guile_cv_exeext=}
libltdl_cv_sys_search_path=${libltdl_cv_sys_search_path="%(system_prefix)s/lib"}
'''
    def configure (self):
        self.file_sub ([('''^#(LIBOBJS=".*fileblocks.*)''', r'\1')],
                       '%(srcdir)s/configure')
        Guile.configure (self)
        for libtool in ['%(builddir)s/libtool']: # readline patched-out: '%(builddir)s/guile-readline/libtool']:
            self.file_sub ([('-mwindows', '')], libtool)

    gnulib_modules = (Guile.gnulib_modules
                      + 'accept bind close connect getpeername getsockname getsockopt listen recv recv recvfrom send sendto setsockopt shutdown socket ')
    def compile (self):
        ## Why the !?#@$ is .EXE only for guile_filter_doc_snarfage?
        self.system ('''cd %(builddir)s/libguile &&make %(compile_flags_native)sgen-scmconfig guile_filter_doc_snarfage.exe''')
        self.system ('cd %(builddir)s/libguile && cp guile_filter_doc_snarfage.exe guile_filter_doc_snarfage')
        Guile.compile (self)
    def install (self):
        Guile.install (self)
        self.system ('''cd %(install_prefix)s/bin && cp guile.exe guile-windows.exe''')

class Guile__linux (Guile):
    compile_command = ('export LD_LIBRARY_PATH=%(builddir)s/libguile/.libs:$LD_LIBRARY_PATH;'
                       + Guile.compile_command)

class Guile__linux__ppc (Guile__linux):
    config_cache_overrides = Guile__linux.config_cache_overrides + '''
guile_cv_have_libc_stack_end=no
'''

class Guile__freebsd (Guile):
    config_cache_overrides = Guile.config_cache_overrides + '''
ac_cv_type_socklen_t=yes
guile_cv_use_csqrt="no"
'''

class Guile__darwin (Guile):
    patches = Guile.patches + ['guile-1.9.14-pthreads-cross.patch']
    def install (self):
        Guile.install (self)
        def dylib_link (logger, fname):
            directory = os.path.split (fname)[0]
            src = os.path.basename (fname)
            dst = os.path.splitext (os.path.basename (fname))[0] + '.so'
            loggedos.symlink (logger, src, os.path.join (directory, dst))
        self.map_locate (dylib_link,
                         self.expand ('%(install_prefix)s/lib/'),
                         'libguile-srfi*.dylib')
 
class Guile__darwin__x86 (Guile__darwin):
    def configure (self):
        self.file_sub ([('guile-readline', '')],
                       '%(srcdir)s/Makefile.in')
        Guile__darwin.configure (self)

class Guile__linux__x86 (Guile):
    patches = Guile.patches + [
        'guile-1.9.14-pthreads-cross.patch',
        'guile-1.9.14-struct.patch',
        ]
    compile_flags_native = (Guile.compile_flags_native +
                            'CPATH="%(srcdir)s:%(builddir)s:%(system_prefix)s/include" ')

class Guile__tools (tools.AutoBuild, Guile):
    patches = []
    dependencies = (Guile.dependencies
                    + [
                'autoconf',
                'automake',
                'gettext',
                'flex',
                'libtool'
                ])
    make_flags = Guile.make_flags
    # Doing make gen-scmconfig, guile starts a configure recheck:
    #    cd .. && make  am--refresh
    #    /bin/sh ./config.status --recheck
    # leading to
    #    checking size of char... 0
    # Great idea, let's re-check!  You never know... :-)
    compile_flags_native = misc.join_lines ('''
LD_LIBRARY_PATH=%(system_prefix)s/lib
CFLAGS='-O2 -I%(system_prefix)s/include'
LDFLAGS='-L%(system_prefix)s/lib %(rpath)s'
''')
    configure_command = ('LD_LIBRARY_PATH=%(system_prefix)s/lib:${LD_LIBRARY_PATH-/foe} '
                         + tools.AutoBuild.configure_command
                         + Guile.guile_configure_flags)
    # FIXME: when configuring, guile runs binaries linked against
    # libltdl.
    # FIXME: when not x-building, guile runs gen_scmconfig, guile without
    # setting the proper LD_LIBRARY_PATH.
    compile_command = ('export LD_LIBRARY_PATH=%(builddir)s/libguile/.libs:%(system_prefix)s/lib:${LD_LIBRARY_PATH-/foe};'
                + tools.AutoBuild.compile_command)
    install_command = tools.AutoBuild.install_command
    def patch (self):
        tools.AutoBuild.patch (self)
        #Guile.autopatch (self)
        self.system ('cp -pv %(sourcefiledir)s/fcntl-o.m4 %(srcdir)s/m4')
    def autoupdate (self):
        self.system ('cd %(srcdir)s && autoreconf')
        # .libs/libguile_2.0_la-arbiters.o: In function `__gmpz_abs':
        # arbiters.c:(.text+0x0): multiple definition of `__gmpz_abs'
        self.file_sub ([('-std=gnu99', ''),('-std=c99', '')], '%(srcdir)s/configure')
    def install (self):
        tools.AutoBuild.install (self)
        self.system ('cd %(install_root)s%(packaging_suffix_dir)s%(prefix_dir)s/bin && cp guile guile-1.9')
#        self.file_sub ([('[(]string-join other-flags[)]', '(string-join (filter (lambda (x) (not (equal? x "-L/usr/lib"))) other-flags))')],
#                       '%(install_root)s%(packaging_suffix_dir)s%(prefix_dir)s/bin/guile-config',
#                       must_succeed=True)

class Guile__tools32 (tools32.AutoBuild, Guile__tools):
    pass
