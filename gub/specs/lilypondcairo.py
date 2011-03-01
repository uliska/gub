from gub.specs import lilypond

# FIXME: this is a version of lilypond which uses pangocairo used by
# Denemo We probably do not want to build pango + cairo for standalone
# lilypond packages, because that would also pull libX11 dependencies
# in.  Hmm.

class Lilypondcairo (lilypond.Lilypond):
    source = 'http://lilypond.org/download/source/v2.13/lilypond-2.13.51.tar.gz'
    dependencies = [x.replace ('pango', 'pangocairo')
                    for x in lilypond.Lilypond.dependencies]
    patches = [
        '0003-Start-OTF-font-from-E800-avoids-hardcoded-linux-unic.patch',
        '0001-ly-spawn-pass-utf-8-strings-to-g_spawn.-Fixes-1522.patch',
        '0001-Midi2ly-new-option-include-header.-Allows-titling-an.patch',
        '0001-Midi2ly-use-SEQUENCE_TRACK_NAME-to-set-Staff.instrum.patch',
        ]
    def get_conflict_dict (self):
        return {'': ['lilypond']}

class Lilypondcairo__mingw (lilypond.Lilypond__mingw):
    source = Lilypondcairo.source
    dependencies = [x.replace ('pango', 'pangocairo')
                for x in lilypond.Lilypond__mingw.dependencies]
    patches = [
        '0003-Start-OTF-font-from-E800-avoids-hardcoded-linux-unic.patch',
        '0001-ly-spawn-pass-utf-8-strings-to-g_spawn.-Fixes-1522.patch',
        '0001-Midi2ly-new-option-include-header.-Allows-titling-an.patch',
        '0001-Midi2ly-use-SEQUENCE_TRACK_NAME-to-set-Staff.instrum.patch',
        ]
    def get_conflict_dict (self):
        return {'': ['lilypond']}

class Lilypondcairo__darwin (lilypond.Lilypond__darwin):
    source = Lilypondcairo.source
    dependencies = [x.replace ('pango', 'pangocairo')
                for x in lilypond.Lilypond__darwin
                .dependencies]
    def get_conflict_dict (self):
        return {'': ['lilypond']}

class Lilypondcairo__darwin__ppc (lilypond.Lilypond__darwin__ppc):
    source = Lilypondcairo.source
    dependencies = [x.replace ('pango', 'pangocairo')
                for x in lilypond.Lilypond__darwin__ppc
                .dependencies]
    def get_conflict_dict (self):
        return {'': ['lilypond']}
