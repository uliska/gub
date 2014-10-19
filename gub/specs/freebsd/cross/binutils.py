from gub.specs.cross import binutils as cross_binutils
from gub import misc

class Binutils__freebsd (cross_binutils.Binutils):
        # Add --program-prefix, otherwise we get
        # i686-freebsd-FOO iso i686-freebsd4-FOO.
    configure_flags = (cross_binutils.Binutils.configure_flags
                + misc.join_lines ('''
--program-prefix=%(toolchain_prefix)s
'''))

class Binutils__freebsd__x86 (cross_binutils.Binutils):
    patches = cross_binutils.Binutils.patches + [
        'binutils-2.24-freebsd4.patch' # This patch will not be needed from binutils 2.25.
        ]
