from gub import misc
gcc = misc.load_spec ('cross/gcc-core')

class Gcc_core (gcc.Gcc_core):
    source = 'http://ftp.gnu.org/pub/gnu/gcc/gcc-4.8.2/gcc-4.8.2.tar.bz2'
    def patch (self):
        gcc.Gcc_core.patch (self)
        self.system ('''
''')
    configure_flags = (gcc.Gcc_core.configure_flags
                + misc.join_lines ('''
--with-float=soft
#--with-fpu=vfp
'''))

