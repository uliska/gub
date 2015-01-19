import os
#
from gub.specs.cross import gcc as cross_gcc
from gub import loggedos
from gub import cross

class Gcc__darwin (cross_gcc.Gcc):
    dependencies = ['odcctools']
    patches = cross_gcc.Gcc.patches + [
        'gcc-4.8.2-darwin-fixinc.patch',
        'gcc-4.8.2-darwin-libgcc.patch',
    ]
    configure_flags = (cross_gcc.Gcc.configure_flags
                       + ' --disable-libcilkrts'
    )
    def languages (self):
        # objective-c is used for quartz's Carbon/Carbon.h in pango, gtk+
        return cross_gcc.Gcc.languages (self) + ['objc', 'obj-c++']
    def install (self):
        cross_gcc.Gcc.install (self)
        # conflicts with darwin-SDK
        self.system ('mv %(install_prefix)s/lib/libsupc++.a %(install_prefix)s/lib/libsupc++.a-')

class Gcc__darwin__ppc (Gcc__darwin):
    configure_flags = (Gcc__darwin.configure_flags
                       + ' --disable-libitm'
    )
