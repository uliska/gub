from gub import target

class Libgtksourceview (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/gtksourceview/2.6/gtksourceview-2.6.2.tar.gz'
    dependencies = [
            'gtk+-devel',
            'libxml2-devel',
            'tools::glib',
            'tools::intltool',
            ]

class Libgtksourceview__darwin (Libgtksourceview):
    dependencies = [x for x in Libgtksourceview.dependencies
                if x.replace ('-devel', '') not in [
                'libxml2', # Included in darwin-sdk, hmm?
                ]]

