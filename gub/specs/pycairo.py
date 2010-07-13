from gub import target

class Pycairo (target.AutoBuild):
# python 2.6
#    source = 'http://cairographics.org/releases/pycairo-1.8.8.tar.gz'
# python 2.5
#    source = 'http://cairographics.org/releases/pycairo-1.8.0.tar.gz'
#    source = 'http://cairographics.org/releases/pycairo-1.6.4.tar.gz'
    force_autoupdate = True
    source = 'http://cairographics.org/releases/pycairo-1.4.12.tar.gz'
    configure_command = ('PYTHON=%(tools_prefix)s/bin/python PYTHON_INCLUDES=-I%(system_prefix)s/include/python2.4 '
                         + target.AutoBuild.configure_command)
    patches = [
        'pycairo-cross.patch',
        ]
    dependencies = [
        'python',
        'cairo',
        ]

class Pycairo__mingw (Pycairo):
    configure_variables = (Pycairo.configure_variables
                  + ' LDFLAGS="-lpython2.4"'  % locals ())
