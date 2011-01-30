from gub import target

class Guile_cairo (target.AutoBuild):
    source = 'http://download.gna.org/guile-cairo/guile-cairo-1.4.0.tar.gz'
    dependencies = [
        'cairo-devel',
        'guile-devel',
        ]
    subpackage_names = ['']
    make_flags = target.AutoBuild.make_flags + '"CPP=%(toolchain_prefix)sgcc -E "'
    def install (self):
        target.AutoBuild.install (self)
        self.dump ('''
(define (get-prefix-dir) (dirname (dirname (car (command-line)))))
(define *cairo-lib-path* (string-append (get-prefix-dir) "/lib/libguile-cairo"))
''',
                   '%(install_prefix)s/share/guile/site/cairo/config.scm',
                   mode='a')
