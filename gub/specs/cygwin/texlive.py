#
from gub import cygwin
from gub import gup
from gub import loggedos
from gub import misc
from gub import target
from gub.specs import texlive

class Texlive (texlive.Texlive):
    patches = texlive.Texlive.patches + [
        'texlive-kpathsea-dll.patch',
        ]
    config_cache_overrides = texlive.Texlive.config_cache_overrides + '''
xdvi_cv_bitmap_type=${xdvi_cv_bitmap_type='BMTYPE=int BMBYTES=4'}
xdvi_cv_func_poll=${xdvi_cv_func_poll=yes}
xdvi_cv_sys_streams=${xdvi_cv_sys_streams=no}
xdvi_cv_sys_sunos_4=${xdvi_cv_sys_sunos_4=no}
xdvi_cv_motif_include=${xdvi_cv_motif_include=no}
xdvi_cv_motif_libdir=${xdvi_cv_motif_libdir=no}
xdvi_cv_func_good_vsnprintf=${xdvi_cv_func_good_vsnprintf=yes}
ac_cv_func_vfork_works=${ac_cv_func_vfork_works=yes}
xdvi_cv_setsid_in_vfork=${xdvi_cv_setsid_in_vfork=yes}
lt_cv_cc_dll_switch=${lt_cv_cc_dll_switch="-Wl,--dll -nostartfiles"}
'''
    dependencies = gup.gub_to_distro_deps (texlive.Texlive.dependencies + [
            'libncurses-devel'],
                                           cygwin.gub_to_distro_dict)
    configure_flags = (target.AutoBuild.configure_flags
                       + '%(common_configure_flags)s'
                       + misc.join_lines ('''
--with-x
--with-mf-x-toolkit=xaw
--with-xdvi-x-toolkit=xaw
--x-includes=%(system_prefix)s/X11R6/include
--x-libraries=%(system_prefix)s/X11R6/lib
''')
                       + "CFLAGS='-O2 -g -DKPSE_DLL'")
    def patch (self):
        texlive.Texlive.patch (self)
        # FIXME: duh: cross-compile auto-enables t1lib
        def defer (logger, i):
            loggedos.file_sub (logger, [
                    ('ac_compile_t1lib=1', 'ac_compile_t1lib=0'),
                    ('-lpng ', '-lpng12 '),
                    ('-lpng"', '-lpng12"'),
                    ], i)
        self.map_find_files (defer, '%(srcdir)s', 'configure')
        self.file_sub ([('^(/\* kpsewhich --)', '#undef KPSE_DLL\n\\1')],
                       '%(srcdir)s/texk/kpathsea/kpsewhich.c')
    xmake_flags = (texlive.Texlive.make_flags
                + misc.join_lines ('''
CFLAGS='-O2 -g -DKPSE_DLL'
'''))
    def install (self):
        self.pre_install_smurf_exe ()
        texlive.Texlive.install (self)
    # FIXME: we do most of this for all cygwin packages
    def category_dict (self):
        return {'': 'Text Publishing',
                'base': 'Text Publishing',
                'extra': 'Text Publishing',}
    def description_dict (self):
        # FIXME: fairly uninformative description for packages,
        # unlike, eg, guile-devel.  This is easier, though.
        d = {}
        for i in self.subpackage_names:
            d[i] = self.get_subpackage_doc (i)
        return d
    def get_subpackage_doc (self, split):
        flavor = {'': 'installer helper',
                  'bin': 'executables',
                  'base': 'base texmf tree',
                  'extra': 'full texmf tree',
                  'devel': 'development',
                  'doc': 'documentation',
                  'runtime': 'runtime',
                  'x11': 'x11 executables',
                  }[split]
        return (texlive.Texlive.__doc__.replace ('\n', ' - %(flavor)s\n', 1)
                % locals ())
