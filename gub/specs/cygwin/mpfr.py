#
from gub import cygwin
from gub import gup
from gub.specs import mpfr

class Mpfr (mpfr.Mpfr):
#    source = 'http://www.mpfr.org/mpfr-2.3.2/mpfr-2.3.2.tar.gz'
    dependencies = gup.gub_to_distro_deps (mpfr.Mpfr.dependencies,
                                           cygwin.gub_to_distro_dict)
