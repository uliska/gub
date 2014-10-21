#
from gub import cygwin
from gub import gup
from gub.specs import gmp

class Gmp (gmp.Gmp):
    source = 'http://ftp.gnu.org/pub/gnu/gmp/gmp-4.2.1.tar.gz'
    patches = []
    dependencies = gup.gub_to_distro_deps (gmp.Gmp.dependencies,
                                           cygwin.gub_to_distro_dict)
