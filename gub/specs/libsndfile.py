from gub import target

class Libsndfile (target.AutoBuild):
    source = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.21.tar.gz'
    dependencies = ['tools::automake', 'tools::pkg-config', 'libtool', 'sqlite']
