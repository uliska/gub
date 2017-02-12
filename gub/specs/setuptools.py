from gub import tools
import sys

class Setuptools (tools.PythonBuild):
    source = 'https://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz'
    install_command = 'cd %(srcdir)s && ' + sys.executable + ' %(srcdir)s/setup.py install --prefix=%(tools_prefix)s --root=%(install_root)s'
