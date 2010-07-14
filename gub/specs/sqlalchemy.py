from gub import target

class Sqlalchemy (target.PythonBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/sqlalchemy/0.5.8/SQLAlchemy-0.5.8.tar.gz'
    install_command = 'cd %(srcdir)s && python %(srcdir)s/setup.py install --prefix=%(tools_prefix)s --root=%(install_root)s'
    dependencies = [
        'tools::setuptools',
        ]
