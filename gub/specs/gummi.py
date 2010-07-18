from gub import target

class Gummi (target.PythonBuild):
    source = 'http://dev.midnightcoding.org/redmine/attachments/download/25/gummi-0.4.8.tar.gz'
    patches = [
        'gummi-0.4.8-lily.patch',
        'gummi-0.4.8-reloc.patch',
        ]
    install_command = 'cd %(srcdir)s && python %(srcdir)s/setup.py install --prefix=%(prefix_dir)s --root=%(install_root)s'
    license_files = ['%(srcdir)s/gummi/misc/gummi']
    subpackage_names = ['']
    dependencies = [
        'ctypes',
        'pygtksourceview',
        'pypoppler',
        ]

class Gummi__mingw (Gummi):
    patches = Gummi.patches + [
        'gummi-0.4.8-mingw.patch',
        ]
