from gub import cross
from gub.specs.cross import gcc
from gub import misc
        
class Gcc_core (gcc.Gcc__from__source):
    dependencies = [x for x in gcc.Gcc__from__source.dependencies
                    if x != 'glibc-core']
    subpackage_names = ['']
    def name (self):
        return 'cross/gcc-core'
    def file_name (self):
        return 'gcc-core'
    def get_conflict_dict (self):
        return {'': ['cross/gcc', 'cross/gcc-devel', 'cross/gcc-doc', 'cross/gcc-runtime']}
#--prefix=%(cross_prefix)s
#--prefix=%(prefix_dir)s
    configure_flags = (gcc.Gcc__from__source.configure_flags
                       .replace ('enable-shared', 'disable-shared')
                       .replace ('disable-static', 'enable-static')
                       .replace ('enable-threads=posix', 'enable-threads=no')
                       + misc.join_lines ('''
--with-newlib
--enable-threads=no
--without-headers
--disable-shared
--disable-decimal-float
'''))
    make_flags = gcc.Gcc.make_flags + ' all-gcc all-target-libgcc'
    install_flags = (gcc.Gcc.install_flags
                     .replace (' install',
                               ' install-gcc install-target-libgcc'))
    # Gcc moves libs into system lib places, which will
    # make gcc-core conflict with gcc.
    def install (self):
        cross.AutoBuild.install (self)
        self.system('''
mkdir -p %(install_prefix)s%(cross_dir)s/lib/gcc/%(target_architecture)s/%(full_version)s/include/
ln -s ../include-fixed/limits.h %(install_prefix)s%(cross_dir)s/lib/gcc/%(target_architecture)s/%(full_version)s/include/limits.h
''')
    def languages (self):
        return  ['c']
