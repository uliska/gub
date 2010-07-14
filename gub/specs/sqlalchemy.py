from gub import target

class Sqlalchemy (target.PythonBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/sqlalchemy/0.5.8/SQLAlchemy-0.5.8.tar.gz'
    subpackage_names = ['']
    install_command = 'cd %(srcdir)s && python %(srcdir)s/setup.py install --prefix=%(prefix_dir)s --root=%(install_root)s'
    dependencies = [
        'tools::setuptools',
        ]
