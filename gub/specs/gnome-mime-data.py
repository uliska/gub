from gub import gnome
from gub import target

class Gnome_mime_data (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.26/2.26.3/sources/gnome-mime-data-2.18.0.tar.gz'
    dependencies = [
        'tools::libtool',
        ]
    subpackage_names = ['']
