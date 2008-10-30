import md5
import os
import re
#
from gub import build
from gub import context
from gub import logging
from gub import misc
from gub import target
from gub import tools

class AutoBuild (build.AutoBuild):
    """Package for cross compilers/linkers etc.
    """
    def get_substitution_dict (self, env={}):
        dict = {
            'C_INCLUDE_PATH': '%(tools_prefix)s/include'
            + misc.append_path (os.environ.get ('C_INCLUDE_PATH', '')),
            'LIBRARY_PATH': '%(tools_prefix)s/lib'
            + misc.append_path (os.environ.get ('LIBRARY_PATH', '')),
            'CPLUS_INCLUDE_PATH': '%(tools_prefix)s/include'
            + misc.append_path (os.environ.get ('CPLUS_INCLUDE_PATH', '')),
            'LD_LIBRARY_PATH': '%(tools_prefix)s/lib'
            + misc.append_path (os.environ.get ('LD_LIBRARY_PATH', '')),
            'PATH': '%(cross_prefix)s/bin:%(tools_prefix)s/bin:' + os.environ['PATH'],
        }
        dict.update (env)
        d = build.AutoBuild.get_substitution_dict (self, dict).copy ()
        return d
    def configure_command (self):
        return (build.AutoBuild.configure_command (self)
            + misc.join_lines ('''
--program-prefix=%(target_architecture)s-
--prefix=%(cross_prefix)s
--with-slibdir=/usr/lib
--target=%(target_architecture)s
--with-sysroot=%(system_root)s
--disable-multilib
'''))
# These should only be necessary for badly behaved packages
# let's hope our cross packages play nice.
#CFLAGS=-I%(tools_prefix)s/include
#LDFLAGS=-L%(tools_prefix)s/lib
#LD_LIBRARY_PATH=%(tools_prefix)s/lib
    def compile_command (self):
        return self.native_compile_command ()
    def install_command (self):
        return '''make DESTDIR=%(install_root)s prefix=/usr/cross install'''
    def get_subpackage_names (self):
        return ['doc', '']
    def install_license (self):
        self.runner.harmless ('not installing license file for cross package: %(name)s' % self.get_substitution_dict ())

def change_target_package (package):
    pass

# GUB compatibility problems:
# GIT: to dowload gub
# make
# tar --strip-component
# /usr/bin/install: coreutils
bootstrap_names = ['tools::librestrict']
def set_cross_dependencies (package_object_dict):
    packs = package_object_dict.values ()

    cross_packs = [p for p in packs if isinstance (p, AutoBuild)]
    sdk_packs = [p for p in packs if isinstance (p, build.SdkBuild)]
    tools_packs = [p for p in packs if isinstance (p, tools.AutoBuild)]
    other_packs = [p for p in packs if (not isinstance (p, AutoBuild)
                                        and not isinstance (p, build.SdkBuild)
                                        and not isinstance (p, build.BinaryBuild)
                                        and not isinstance (p, tools.AutoBuild)
                                        and not p.platform_name () in bootstrap_names)]
    python_packs = [p for p in packs if (isinstance (p, tools.PythonBuild)
                                         or isinstance (p, target.PythonBuild))]
    scons_packs = [p for p in packs if (isinstance (p, tools.SConsBuild)
                                        or isinstance (p, target.SConsBuild))]
    extra_names = []
    if python_packs or scons_packs:
        extra_names += ['tools::python']
    if scons_packs:
        extra_names += ['tools::scons']

    sdk_names = [s.platform_name () for s in sdk_packs]
    cross_names = [s.platform_name () for s in cross_packs]
    for p in other_packs:
        old_callback = p.get_build_dependencies
        p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                         lambda x,y: x+y, (cross_names,))
    for p in other_packs + cross_packs:
        old_callback = p.get_build_dependencies
        p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                         lambda x,y: x+y, (sdk_names,))
    for p in other_packs + cross_packs + tools_packs:
        old_callback = p.get_build_dependencies
        p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                         lambda x,y: x+y, (bootstrap_names,))
    for p in python_packs:
        old_callback = p.get_build_dependencies
        p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                         lambda x,y: x+y, (['tools::python'],))
    for p in scons_packs:
        old_callback = p.get_build_dependencies
        p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                         lambda x,y: x+y, (['tools::scons'],))
    return extra_names

cross_module_checksums = {}
cross_module_cache = {}
def get_cross_module (settings):
    platform = settings.platform
    if cross_module_cache.has_key (platform):
        return cross_module_cache[platform]

    base = re.sub ('[-0-9].*', '', platform)
    gubdir = settings.gubdir
    for name in platform, base:
        file_name = '%(gubdir)s/gub/%(name)s.py' % locals ()
        if os.path.exists (file_name):
            break

    logging.info ('module name: ' + name + '\n')
    module = misc.load_module (file_name, base)

    cross_module_checksums[platform] = md5.md5 (open (file_name).read ()).hexdigest ()
    cross_module_cache[platform] = module
    return module

def get_build_dependencies (settings):
    mod = get_cross_module (settings)
    return bootstrap_names + [misc.with_platform (n, settings.platform) for n in mod.get_cross_build_dependencies (settings)]

def setup_linux_x86 (logger, package, env):
    '''Hack for using 32 bit compiler on linux-64.

    Use linux-x86 cross compiler to compile non-64-bit-clean packages such
    as nsis and odcctools.  A plain 32 bit compiler could also be used,
    but we do not have such a beast.  Make sure to have 32-bit
    compatibility installed:
        apt-get install ia32-libs
    '''

    x86_dir = package.settings.alltargetdir + '/linux-x86'
    x86_cross = (x86_dir
                 + package.settings.root_dir
                 + package.settings.prefix_dir
                 + package.settings.cross_dir)
    x86_bindir = x86_cross + '/bin'
    x86_cross_bin = x86_cross + '/i686-linux' + '/bin'

    compiler = x86_bindir + '/i686-linux-gcc'
    if not os.path.exists (compiler):
        print 'error: cannot find 32 bit compiler: %(compiler)s\n' % locals ()
        raise Exception ('Package %s depends on target/linux-x86.'
                         % package.__class__)
    if os.system ('''echo 'int main () { return 0; }' > 32bit.c && %(compiler)s -o 32bit 32bit.c && ./32bit''' % locals ()):
        print 'error: cannot run 32 bit executable: 32bit\n'
        raise Exception ('Package %s depends on 32 bit libraries'''
                         % package.__class__)
    os.system ('rm -f 32bit 32bit.c')

    def check_link (src, dest):
        dest = x86_cross_bin + '/' + dest
        if not os.path.exists (dest):
            # duh, must chdir for relative link
            #src = '../../bin/i686-linux-' + src
            src = x86_bindir + '/i686-linux-' + src
            os.link (src, dest)

    check_link ('cpp', 'cpp')
    check_link ('gcc', 'cc')
    check_link ('g++', 'c++')
    check_link ('gcc', 'gcc')
    check_link ('g++', 'g++')


def change_target_package_x86 (package, env={'PATH': os.environ['PATH']}):

    x86_dir = package.settings.alltargetdir + '/linux-x86'
    x86_cross = (x86_dir
                 + package.settings.root_dir
                 + package.settings.prefix_dir
                 + package.settings.cross_dir)
    x86_bindir = x86_cross + '/bin'
    x86_cross_bin = x86_cross + '/i686-linux' + '/bin'
    env['PATH'] = x86_cross_bin + ':' + env['PATH']
    env['LIBRESTRICT_ALLOW'] = package.settings.targetdir
    env['CC'] = x86_cross_bin + '/gcc'
    env['CXX'] = x86_cross_bin + '/g++'

    def build_environment (e):
        return env
    
    def patch (foo):
        package.func (setup_linux_x86, package, env)

    # FIXME: we could also add [, build_environment ()] by default
    # to build.py's compile [and install?] functions
    def configure (foo):
        package.system ('mkdir -p %(builddir)s')
        package.system ('cd %(builddir)s && %(configure_command)s', env)
        
    def compile (foo):
        package.system ('cd %(builddir)s && %(compile_command)s', env)
            
    package.build_environment \
        = misc.MethodOverrider (package.nop, build_environment)
    package.patch \
        = misc.MethodOverrider (package.patch, patch)
    package.configure \
            = misc.MethodOverrider (package.nop, configure)
    package.compile \
        = misc.MethodOverrider (package.nop, compile)
