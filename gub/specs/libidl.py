from gub import gnome
from gub import target

class Libidl (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.26/2.26.3/sources/libIDL-0.8.13.tar.gz'
    dependencies = [
        'tools::libtool',
        'glib-devel',
        ]
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
libIDL_cv_long_long_format=ll
'''
