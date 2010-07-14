from gub import target

class Pysqlite (target.PythonBuild):
    source = 'http://pypi.python.org/packages/source/p/pysqlite/pysqlite-2.6.0.tar.gz'
    subpackage_names = ['']
    def patch (self):
        def defer (logger):
            dist_fix = '''
import os
import sys
from distutils import sysconfig
def get_python_inc(plat_specific=0, prefix='%(system_prefix)s'):
    return os.path.join(prefix, "include", "python" + sys.version[:3])
sysconfig.get_python_inc = get_python_inc

from distutils.command import build_ext
build_ext.build_ext._get_libraries = build_ext.build_ext.get_libraries
def get_libraries (self, ext):
    return self._get_libraries (ext) + ['python2.4']
build_ext.build_ext.get_libraries = get_libraries
'''
            setup = self.expand ('%(srcdir)s/setup.py')
            s = open (setup).read ()
            open (setup, 'w').write (self.expand (dist_fix) + s)
        self.func (defer)
    install_command = 'cd %(srcdir)s && SO=%(so_extension)s LDSHARED="$CC -shared" LDFLAGS="-L%(system_prefix)s/bin -lpython2.4" CFLAGS="--verbose" python %(srcdir)s/setup.py install --prefix=%(prefix_dir)s --root=%(install_root)s'
    dependencies = [
        'sqlite',
        'tools::setuptools',
        ]
