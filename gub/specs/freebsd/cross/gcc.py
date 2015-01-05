from gub.specs.cross import gcc as cross_gcc
from gub import misc

class Gcc__freebsd (cross_gcc.Gcc):
    dependencies = cross_gcc.Gcc.dependencies + ['tools::mpfr']
    configure_command = (''' LDFLAGS='-L%(tools_prefix)s/lib %(rpath)s' '''
                         + cross_gcc.Gcc.configure_command)
    configure_flags = (cross_gcc.Gcc.configure_flags
                + misc.join_lines ('''
--program-prefix=%(toolchain_prefix)s
--disable-libcilkrts
--disable-__cxa_atexit
'''))
