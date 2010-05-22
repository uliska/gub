#
from gub import cygwin
from gub import gup
from gub.specs import libgd

class Libgd (libgd.Libgd):
    dependencies = gup.gub_to_distro_deps (libgd.Libgd.dependencies,
                                           cygwin.gub_to_distro_dict)
