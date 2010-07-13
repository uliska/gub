from gub import target

class Pygobject (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.16/pygobject-2.16.1.tar.gz'
    #source = 'http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.21/pygobject-2.21.5.tar.gz'
    force_autoupdate = True
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
ac_cv_setwakeupfd_ok=yes
'''
    def aclocal_path (self):
        return (target.AutoBuild.aclocal_path (self)
                + ['%(srcdir)s/m4', '%(srcdir)s'])
    configure_command = ('PYTHON=%(tools_prefix)s/bin/python PYTHON_INCLUDES=-I%(system_prefix)s/include/python2.4 '
                         + target.AutoBuild.configure_command)
    patches = [
        'pygobject-cross.patch',
        ]
    dependencies = [
        'python',
        'glib',
        ]
    def compile (self):
        self.system ('''cd %(builddir)s/gobject && make generate_constants_LINK='gcc -o$@' CC=gcc constants.py''')
        target.AutoBuild.compile (self)

class Pygobject__mingw (Pygobject):
    patches = Pygobject.patches + [
        'pygobject-mingw.patch',
        ]
    configure_variables = (Pygobject.configure_variables
                  + ' LDFLAGS="-lpython2.4"'  % locals ())
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
ac_cv_setwakeupfd_ok=no
'''
    def patch (self):
        self.file_sub ([('have_giounix=true', 'have_giounix=false')], '%(srcdir)s/configure.ac', must_succeed=True)
        Pygobject.patch (self)
