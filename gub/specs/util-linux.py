from gub import tools
import os
if 'BOOTSTRAP' in os.environ.keys (): from gub import target as tools

class Util_linux__tools (tools.AutoBuild):
    source = 'http://www.nl.kernel.org/pub/linux/utils/util-linux-ng/v2.16/util-linux-ng-2.16.tar.gz'
    def _get_build_dependencies (self):
        return ['libtool']
    def configure_command (self):
        return (tools.AutoBuild.configure_command (self)
                + ' --disable-tls'
                + ' --disable-makeinstall-chown'
                + ''' CFLAGS='-DLINE_MAX=1024' ''')