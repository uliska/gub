from gub import target
from gub import misc

class Pygtksourceview (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/pygtksourceview/2.10/pygtksourceview-2.10.1.tar.gz'
    configure_command = (misc.join_lines ('''
PYTHON=%(tools_prefix)s/bin/python
PYTHON_HOME=%(system_prefix)s
PYTHON_VERSION=2.4
PYTHON_GTK_DIR=%(system_prefix)s/lib/python2.4/site-packages
PYTHON_INCLUDES=-I%(system_prefix)s/include/python2.4
PYTHON_LIBS="-L%(system_prefix)s/bin -lpython2.4"
''')
                         + target.AutoBuild.configure_command)
    dependencies = [
        'gtksourceview',
        'python',
        ]
    
