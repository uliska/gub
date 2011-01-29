from gub import build
from gub import octal

class Guile_config (build.SdkBuild):
    source = 'url://host/guile-config-1.8.7.tar.gz'
    source = 'url://host/guile-config-1.9.14.tar.gz'
    def install (self):
        build.SdkBuild.install (self)
        self.system ('mkdir -p %(cross_prefix)s%(prefix_dir)s/bin')
        version = self.version ()
        #FIXME: c&p guile.py
        self.dump ('''\
#! /bin/sh
test "$1" = "--version" && echo "%(target_architecture)s-guile-config - Guile version %(version)s"
#prefix=$(dirname $(dirname $0))
prefix=%(system_prefix)s
test "$1" = "compile" && echo "-I$prefix/include/guile/2.0"
test "$1" = "link" && echo "-L$prefix/lib -lguile-2.0 -lgmp"
test "$1" = "info" && test "$2" = "guileversion" && echo "%(version)s"
exit 0
''',
             '%(install_prefix)s%(cross_dir)s/bin/guile-config',
                   permissions=octal.o755)

class Guile_config__debian (build.SdkBuild):
    source = 'url://host/guile-config-1.8.7.tar.gz'
    def install (self):
        build.SdkBuild.install (self)
        self.system ('mkdir -p %(cross_prefix)s%(prefix_dir)s/bin')
        version = self.version ()
        #FIXME: c&p guile.py
        self.dump ('''\
#! /bin/sh
test "$1" = "--version" && echo "%(target_architecture)s-guile-config - Guile version %(version)s"
#prefix=$(dirname $(dirname $0))
prefix=%(system_prefix)s
test "$1" = "compile" && echo "-I$prefix/include"
test "$1" = "link" && echo "-L$prefix/lib -lguile -ldl -lcrypt -lm"
exit 0
''',
             '%(install_prefix)s%(cross_dir)s/bin/guile-config',
                   permissions=octal.o755)
