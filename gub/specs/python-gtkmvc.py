from gub import target

class Python_gtkmvc (target.PythonBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/pygtkmvc/python-gtkmvc-1.99.0.tar.gz'
    subpackage_names = ['']
    install_command = 'cd %(srcdir)s && python %(srcdir)s/setup.py install --prefix=%(prefix_dir)s --root=%(install_root)s'
    patches = [
        'python-gtkmvc-cross.patch',
        ]
    dependencies = [
        'pygtk',
        'tools::setuptools',
        ]
