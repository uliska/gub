from gub import tools

class Mpfr__tools (tools.AutoBuild):
    source = 'http://www.mpfr.org/mpfr-3.1.2/mpfr-3.1.2.tar.gz'
    dependencies = ['libtool', 'gmp']
