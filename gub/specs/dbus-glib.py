from gub import build
from gub import target

class Dbus_glib (target.AutoBuild):
    source = 'http://dbus.freedesktop.org/releases/dbus-glib/dbus-glib-0.82.tar.gz'
    dependencies = [
        'dbus',
        'glib',
        'tools::automake',
        'tools::pkg-config',
        ]
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
ac_cv_have_abstract_sockets=${ac_cv_have_abstract_sockets=yes}
'''
    configure_flags = target.AutoBuild.configure_flags + ' --with-introspect-xml=%(srcdir)s/dbus-bus-introspect.xml '
    def patch (self):
        target.AutoBuild.patch (self)
        self.system ('cp -pv %(sourcefiledir)s/dbus-bus-introspect.xml %(srcdir)s')
        self.file_sub ([('pkg-config', '$PKG_CONFIG')],
                       '%(srcdir)s/configure')
#    def __init__ (self, settings, source):
#        target.AutoBuild.__init__ (self, settings, source)
#        build.append_dict (self, {'PKG_CONFIG': ' --define-variable daemondir=%(system_prefix)s/bin' })

