from gub import mirrors
from gub.specs.cross import gcc as cross_gcc
from gub import misc

class Gcc (cross_gcc.Gcc_from_source):
    def patch (self):
        cross_gcc.Gcc_from_source.patch (self)
        self.system ('''
''')
    configure_flags = (cross_gcc.Gcc_from_source.configure_flags
                + misc.join_lines ('''
--with-float=soft
#--with-fpu=vfp
'''))
