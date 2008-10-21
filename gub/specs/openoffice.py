import os
#
from gub import context
from gub import misc
from gub import targetbuild

'''
7 matches for "delivered successfully" in buffer: *shell*
   4642:Module 'solenv' delivered successfully. 0 files copied, 1 files unchanged
   4655:Module 'stlport' delivered successfully. 0 files copied, 8 files unchanged
   4995:Module 'soltools' delivered successfully. 7 files copied, 7 files unchanged
   5069:Module 'external' delivered successfully. 3 files copied, 27 files unchanged
   6288:Module 'libwpd' delivered successfully. 12 files copied, 0 files unchanged
   6397:Module 'xml2cmp' delivered successfully. 3 files copied, 2 files unchanged
'''

class Openoffice (targetbuild.TargetBuild):
#    source = 'svn://gsvn.gnome.org/svn/ooo-build&branch=trunk&revision=14327'
    source = 'svn://svn.gnome.org/svn/ooo-build&branch=trunk'
    patches = ['openoffice-srcdir-build.patch']
    upstream_patches = ['openoffice-config_office-cross.patch', 'openoffice-config_office-gnu-make.patch', 'openoffice-config_office-mingw.patch', 'openoffice-solenv-cross.patch', 'openoffice-solenv.patch', 'openoffice-sal-cross.patch', 'openoffice-soltools-cross.patch', 'openoffice-soltools-mingw.patch']
#    upstream_patches = ['openoffice-config_office-cross.patch', 'openoffice-config_office-mingw.patch']
    def get_build_dependencies (self):
        return ['boost-devel', 'curl', 'db-devel', 'expat', 'fontconfig-devel', 'libjpeg-devel', 'libpng-devel', 'python', 'saxon-java', 'xerces-c', 'zlib-devel']
    def stages (self):
        return misc.list_insert_before (targetbuild.TargetBuild.stages (self),
                                        'compile',
                                        ['dot_download', 'make_unpack', 'patch_upstream'])
    def dot_download (self):
        self.system ('mkdir -p %(downloads)s/openoffice-src')
        self.system ('cd %(builddir)s && ln %(downloads)s/openoffice-src/* src || :')
        self.system ('cd %(builddir)s && ./download')
        self.system ('cd %(builddir)s && ln src/* %(downloads)s/openoffice-src || :')
    @context.subst_method
    def cvs_tag (self):
        return 'ooo300-m9'
    @context.subst_method
    def upstream_dir (self):
        return '%(builddir)s/build/%(cvs_tag)s'
    @context.subst_method
    def OOO_TOOLS_DIR (self):
        # TODO: either make all ooo-tools (soltools: makedepend..., transex3: transex3 ...)
        # self-hosting or compile them as Openoffice__tools package...
        # Shortcut: use precompiled tools from user's system
        return os.environ['OOO_TOOLS_DIR']
    def autoupdate (self):
        # Why is build.py:Build:patch() not doing this?
        map (self.apply_patch, self.__class__.patches)
        self.system ('cd %(srcdir)s && NOCONFIGURE=1 ./autogen.sh --noconfigure')
    def config_cache_overrides (self, str):
        return str + '''
ac_cv_file__usr_share_java_saxon9_jar=${ac_cv_file__usr_share_java_saxon9_jar=yes}
ac_cv_file__usr_share_java_saxon_jar=${ac_cv_file__usr_share_java_saxon_jar=yes}
ac_cv_db_version_minor=${ac_cv_db_version_minor=7}
ac_cv_icu_version_minor=${ac_cv_icu_version_minor=3.81}
'''
    def configure_command (self):
        return (targetbuild.TargetBuild.configure_command (self)
                + misc.join_lines ('''
--with-vendor=\"GUB -- LilyPond.org\"
--disable-Xaw
--disable-access
--disable-activex
--disable-activex-component
--disable-atl
--disable-binfilter
--disable-build-mozilla
--disable-cairo
--disable-crypt-link
--disable-cups
--disable-dbus
--disable-directx
--disable-epm
--disable-evolution2
--disable-extensions
--disable-fontooo
--disable-gio
--disable-gnome-vfs
--disable-gstreamer
--disable-gtk
--disable-kde
--disable-kdeab
--disable-largefile
--disable-layout
--disable-ldap
--disable-ldap
--disable-libsn
--disable-lockdown
--disable-mathmldtd
--disable-mono
--disable-mozilla
--disable-neon
--disable-odk
--disable-opengl
--disable-pam
--disable-pasf
--disable-pch
--disable-qadevooo
--disable-randr
--disable-rpath
--disable-scsolver
--disable-systray
--disable-vba
--disable-vba 
--disable-xrender-link

--enable-fontconfig
--enable-verbose

--without-gpc
--without-agg
--without-java
--without-myspell-dicts

--with-system-boost
--with-system-cairo
--with-system-curl
--with-system-db
--with-system-expat
--with-system-icu
--with-system-jpeg
--with-system-libxslt
--with-system-neon
--with-system-odbc-headers
--with-system-portaudio
--with-system-sablot
--with-system-saxon
--with-system-sndfile
--with-system-xalan
--with-system-xerces
--with-system-xml-apis
--with-system-xrender-headers
--with-saxon-jar=%(system_prefix)s/share/java/saxon9.jar
--without-system-mozilla

--cache-file=%(builddir)s/config.cache

--with-tools-dir=%(OOO_TOOLS_DIR)s

'''))

# TODO:
# --with-system-libwpd
# --with-system-libwps
# --with-system-libwpg

    def make_unpack (self):
        # FIXME: python detection is utterly broken, should use python-config
        self.system ('cd %(builddir)s && make unpack')
        self.system ('cd %(builddir)s && make patch.apply')
    def apply_upstream_patch (self, name, strip_component=0):
        patch_strip_component = str (strip_component)
        self.system ('''
cd %(builddir)s/build/%(cvs_tag)s && patch -p%(patch_strip_component)s < %(patchdir)s/%(name)s
''', locals ())
    def patch_upstream (self):
        base = '%(builddir)s/build/%(cvs_tag)s'
        upstream_dir = self.upstream_dir ()
        for file in (
            'config_office/acinclude.m4',
            'config_office/configure.in',
            'config_office/bootstrap.1',
            'config_office/set_soenv.in',
            'solenv/inc/startup/startup.mk',
            'solenv/inc/wntgcci6.mk',
            'solenv/inc/unitools.mk',
            'solenv/bin/build.pl',
            'solenv/bin/deliver.pl',
            'soltools/util/makefile.pmk',
            'soltools/mkdepend/collectdircontent.cxx',
            'sal/rtl/source/makefile.mk',
            ):
            self.system ('cp -p %(upstream_dir)s/%(file)s.pristine %(upstream_dir)s/%(file)s || cp -p %(upstream_dir)s/%(file)s %(upstream_dir)s/%(file)s.pristine' % locals ())
        map (self.apply_upstream_patch, self.__class__.upstream_patches)

        # FIXME: neutralize silly GNU make check
        # self.system ('''sed -i -e "s@' 3[.]81'@'gpuhleez, we are not even building mozilla'@" %(upstream_dir)s/config_office/configure.in')

        # configure blindly adds /usr includes, even when not necessary
        self.system ('sed -i -e "s@=/usr/include@=%(system_prefix)s/include@" %(upstream_dir)s/config_office/configure.in')

        # configure.in uses AC_CHECK_FILE, which simply assert-fails
        # when cross compiling slated for removal in ~2000
        # http://www.mail-archive.com/autoconf@gnu.org/msg02857.html
        self.system ('sed -i -e "s@AC_CHECK_FILE(@AC_CHECK_FILE_CROSS(@" %(upstream_dir)s/config_office/configure.in')

        # avoid juggling of names for windows-nt
        self.system ('sed -i -e "s@WINNT@WNT@" %(upstream_dir)s/config_office/configure.in')

        # TODO: ASM is handled in individual solenv/inc/*mk
        self.system (misc.join_lines ('''sed -i.guborig
-e 's@\<ar\>@$(AR)@g'
-e 's@\<dlltool\>@$(DLLTOOL)@g'
-e 's@\<ld\>\([^-]\|$\)@$(LD)\\1@g'
-e 's@\<nm\>@$(NM)@g'
-e 's@\<ranlib\>@$(RANLIB)@g'
%(upstream_dir)s/solenv/inc/*mk'''))

        self.system ('chmod +x %(upstream_dir)s/solenv/bin/build.pl %(upstream_dir)s/solenv/bin/deliver.pl')
    def makeflags (self):
        return misc.join_lines ('''
CC_FOR_BUILD=cc
CXX_FOR_BUILD=c++
LDFLAGS_FOR_BUILD=
C_INCLUDE_PATH=
LIBRARY_PATH=
EXECPOST=
''')
##main configure barfs
##CPPFLAGS=
                
class Openoffice__mingw (Openoffice):
    def configure_command (self):
        return (Openoffice.configure_command (self)
                .replace ('--with-system-xrender-headers', '')
                + ' --disable-xrender-link'
                + ' --with-distro=Win32')
