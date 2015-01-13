from gub import tools

class Mpc__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/gnu/mpc/mpc-1.0.2.tar.gz'
    dependencies = ['gmp', 'mpfr']
