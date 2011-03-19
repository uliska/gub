;;;; schikkers-list.nsi -- Schikkers-List installer script for Microsoft Windows
;;;; (c) 2005--2011
;;;; Jan Nieuwenhuizen <janneke@gnu.org>
;;;; Han-Wen Nienhuys <janneke@gnu.org>
;;;; licence: GNU GPL

;; For quick [wine] test runs
;; !define TEST "1"


;;; substitutions

!define ENVIRON "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"

!define UNINSTALL \
	"Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRETTY_NAME}"
!define USER_SHELL_FOLDERS \
	"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"

!define UninstLog "files.txt"
Var UninstLog

; Uninstall log file missing.
LangString UninstLogMissing ${LANG_ENGLISH} "${UninstLog} not found.$\r$\nCannot uninstall."

!include "substitute.nsh"
${StrLoc}
${UnStrLoc}

;;SetCompressor lzma  ; very slow
;;SetCompressor zlib
SetCompressor bzip2  ;;

Name "${PRETTY_NAME}"

Caption "${PRETTY_NAME} ${INSTALLER_VERSION} for Microsoft Windows"
BrandingText "${PRETTY_NAME} installer v1.0"


InstallDir $PROGRAMFILES\${PRETTY_NAME}
InstallDirRegKey HKLM "Software\${PRETTY_NAME}" "Install_Dir"

CRCCheck on
XPStyle on
InstallColors /windows

BGGradient 000000 E8FFE8 FFFFFF

;; Use Finish iso Close for the [close button text]
;; Although nothing happens after Close, experienced Windows users feel
;; much more with "Finish" than with Close.
MiscButtonText Back Next Cancel Finish

LicenseText "Conditions for redistributing ${PRETTY_NAME}" "Next"
LicenseData "${ROOT}\license\${NAME}"
LicenseForceSelection off

Page license

;; FIXME: the installer will crash on File /r commands if Page
;; directory is not used.
Page directory

Page components

;; Put a note to look at the Help page of the website on the
;; window when the install is completed
CompletedText "Install completed.  Please see $INSTDIR\usr\bin\${CANARY_EXE}."
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

Section "${PRETTY_NAME} (required)"
	;; always generate install log
	Logset on

silent:
	IfFileExists $INSTDIR\usr\bin\${CANARY_EXE}.exe no_overwrite_error fresh_install
no_overwrite_error:
	MessageBox MB_OK "Previous version of ${PRETTY_NAME} found$\r$\nUninstall the old version first."
	Abort "Previous version of ${PRETTY_NAME} found$\r$\nUninstall the old version first."

fresh_install:
	SetOverwrite on
	AllowSkipFiles on
	SetOutPath $INSTDIR

	File /r "${ROOT}\usr"
	File /r "${ROOT}\license"
	File /r "${ROOT}\files.txt"

	WriteUninstaller "uninstall.exe"
	CreateDirectory "$INSTDIR\usr\bin"

	Call registry_installer
	Call registry_path
	Call postinstall_schikkers_list
SectionEnd

Function registry_path
	ReadRegStr $R0 HKLM "${ENVIRON}" "PATH"
	WriteRegExpandStr HKLM "${ENVIRON}" "PATH" "$R0;$INSTDIR\usr\bin"
FunctionEnd

;; copy & paste from the NSIS code examples
Function un.install_installed_files
 IfFileExists "$INSTDIR\${UninstLog}" +3
  MessageBox MB_OK|MB_ICONSTOP "$(UninstLogMissing)"
   Abort

 Push $R0
 Push $R1
 Push $R2
 SetFileAttributes "$INSTDIR\${UninstLog}" NORMAL
 FileOpen $UninstLog "$INSTDIR\${UninstLog}" r
 StrCpy $R1 -1

 GetLineCount:
  ClearErrors
  FileRead $UninstLog $R0
  IntOp $R1 $R1 + 1
  StrCpy $R0 "$INSTDIR\$R0" -2
  Push $R0
  IfErrors 0 GetLineCount

 Pop $R0

 LoopRead:
  StrCmp $R1 0 LoopDone
  Pop $R0

  IfFileExists "$R0\*.*" 0 +3
   RMDir $R0  #is dir
  Goto +3
  IfFileExists "$R0" 0 +2
   Delete "$R0" #is file

  IntOp $R1 $R1 - 1
  Goto LoopRead
 LoopDone:
 FileClose $UninstLog

 Pop $R2
 Pop $R1
 Pop $R0

FunctionEnd
;; end copy & paste

;; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"
	;; First install for all users, if anything fails, install
	;; for current user only.
	ClearErrors

	;; The OutPath specifies the CWD of the command.  For desktop
	;; shortcuts, set to a string that expands to the desktop folder
	;; of the user who runs LilyPond.
	ReadRegStr $R0 HKCU "${USER_SHELL_FOLDERS}" "Desktop"
	SetOutPath '"$R0"'
	SetShellVarContext all

	;; Working directory: %USERPROFILE%\<locale's-desktop-folder-name>,
	;; but that string is not expanded.

	;; Let's see what happens when outputting to the shared desktop.
	;; Let's not--
 	;; Goto current_user

	SetOutPath "$DESKTOP"
	Call create_shortcuts

	;; That also did not work, often the other users do no write access
	;; there.

	;; If no write access for all, delete common stuff and opt for
	;; install for current user only.
	IfErrors 0 exit
	Delete "$DESKTOP\Schikkers-List.lnk"
	Delete "$SMPROGRAMS\Schikkers-List\*.*"
	RMDir "$SMPROGRAMS\Schikkers-List"

	;; $DESKTOP should expand to the same location as the outpath above,
	;; but nsis may handle anomalies better.

current_user:
	SetShellVarContext current
	SetOutPath "$DESKTOP"
	Call create_shortcuts

exit:
	SetShellVarContext current
	SetOutPath $INSTDIR
SectionEnd

;; Optional section (can be disabled by the user)
Section "Bundled Python"
    ;; Only make bundled python interpreter the default
    ;; if user wants it to be (i.e.  for the average windows
    ;; user who only cares that software works just like that)
    Call registry_python
SectionEnd

;; Optional section (can be disabled by the user)
Section "Bundled Guile"
    ;; Only make bundled guile interpreter the default
    ;; if user wants it to be (i.e.  for the average windows
    ;; user who only cares that software works just like that)
    Call registry_guile
SectionEnd

Section "Uninstall"
	ifSilent 0 silent
	Logset on

silent:
	DeleteRegKey HKLM SOFTWARE\${PRETTY_NAME}
	DeleteRegKey HKLM "${UNINSTALL}"

	DeleteRegKey HKCR "${PRETTY_NAME}" ""


	ReadRegStr $R0 HKLM "${ENVIRON}" "PATH"
	${UnStrLoc} $0 $R0 "$INSTDIR\usr\bin;" >

path_loop:
	StrCmp $0 "" path_done
	StrLen $1 "$INSTDIR\usr\bin;"
	IntOp $2 $0 + $1
	StrCpy $3 $R0 $0 0
	StrCpy $4 $R0 10000 $2
	WriteRegExpandStr HKLM "${ENVIRON}" "PATH" "$3$4"
	ReadRegStr $R0 HKLM "${ENVIRON}" "PATH"
	${UnStrLoc} $0 $R0 "$INSTDIR\usr\bin;" >
	StrCmp $0 "" path_done path_loop

path_done:
	call un.install_installed_files

	;; Remove shortcuts, if any
	SetShellVarContext all
	Delete "$SMPROGRAMS\${PRETTY_NAME}\*.*"
	Delete "$DESKTOP\${PRETTY_NAME}.lnk"
	RMDir "$SMPROGRAMS\${PRETTY_NAME}"

	SetShellVarContext current
	Delete "$SMPROGRAMS\${PRETTY_NAME}\*.*"
	Delete "$DESKTOP\${PRETTY_NAME}.lnk"
	RMDir "$SMPROGRAMS\${PRETTY_NAME}"

	;; Remove directories used
	RMDir "$SMPROGRAMS\${PRETTY_NAME}"
	RMDir "$INSTDIR\usr\bin"
	RMDir "$INSTDIR\usr\"
	Delete "$INSTDIR\uninstall.exe"
	Delete "$INSTDIR\files.txt"

	RMDir "$INSTDIR"
SectionEnd

Function registry_installer
	WriteRegStr HKLM "SOFTWARE\${PRETTY_NAME}" "Install_Dir" "$INSTDIR"
	WriteRegStr HKLM "${UNINSTALL}" "DisplayName" "${PRETTY_NAME}"
	WriteRegStr HKLM "${UNINSTALL}" "UninstallString" '"$INSTDIR\uninstall.exe"'
	WriteRegDWORD HKLM "${UNINSTALL}" "NoModify" 1
	WriteRegDWORD HKLM "${UNINSTALL}" "NoRepair" 1
FunctionEnd

Function create_shortcuts
	;; Start menu
	CreateDirectory "$SMPROGRAMS\Schikkers-List"
	CreateShortCut "$SMPROGRAMS\Schikkers-List\Schikkers-List.lnk" \
		"$INSTDIR\usr\bin\schikkers-list.scm" ""\
 		"$INSTDIR\usr\share\guile\site\ikli\images\note-elevator.ico" 0 SW_SHOWNORMAL
	CreateShortCut "$SMPROGRAMS\Schikkers-List\Schikkers-List Website.lnk" \
		"http://schikkers-list.org/" "" \
		"firefox.exe" 0
	CreateShortCut "$SMPROGRAMS\Schikkers-List\Uninstall.lnk" \
		"$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0

	;; Desktop
	ClearErrors

	;; Desktop link always on current user's desktop
	SetShellVarContext current
 	SetOutPath "$DESKTOP"

	ReadRegStr $R0 HKLM \
		"SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion
	CreateShortCut "$DESKTOP\Schikkers-List.lnk" \
		"$INSTDIR\usr\bin\schikkers-list.scm" ""\
 		"$INSTDIR\usr\share\ikli\images\note-elevator.ico" 0 SW_SHOWNORMAL
FunctionEnd

Function registry_python
	ReadRegStr $R0 HKLM "${ENVIRON}" "PATHEXT"
 	${StrLoc} $0 $R0 ".PY;" >
	StrCmp $0 "" 0 py_done
	WriteRegStr HKLM "${ENVIRON}" "PATHEXT" ".PY;$R0"

py_done:
	WriteRegStr HKCR ".py" "" "Python"
	WriteRegStr HKCR ".py" "Python" "Python"
	WriteRegStr HKCR ".py" "Content Type" "text/x-python"

;;py_open:
	ReadRegStr $R0 HKCR "Python\shell\open\command" ""
	;;StrCmp $R0 "" 0 py_auto_file
	WriteRegStr HKCR "Python\shell" "" "open"
	# %1 is the PYTHON command, so must be quoted bo the space
	WriteRegExpandStr HKCR "Python\shell\open\command" "" '"$INSTDIR\usr\bin\python-windows.exe" "%1" %2 %3 %4 %5 %6 %7 %8 %9'

;;py_auto_file:
	ReadRegStr $R0 HKCR "py_auto_file\shell\open\command" ""
	;;StrCmp $R0 "" 0 py_end
	WriteRegStr HKCR "py_auto_file\shell" "" "open"
	# %1 is the PYTHON command, so must be quoted bo the space
	WriteRegExpandStr HKCR "py_auto_file\shell\open\command" "" '"$INSTDIR\usr\bin\python-windows.exe" "%1" %2 %3 %4 %5 %6 %7 %8 %9'
;;py_end:	
FunctionEnd

Function registry_guile
	WriteRegStr HKLM "${ENVIRON}" "XDG_CACHE_HOME" "$LOCALAPPDATA\cache"
	ReadRegStr $R0 HKLM "${ENVIRON}" "PATHEXT"
 	${StrLoc} $0 $R0 ".SCM;" >
	StrCmp $0 "" 0 scm_done
	WriteRegStr HKLM "${ENVIRON}" "PATHEXT" ".SCM;$R0"

scm_done:
	WriteRegStr HKCR ".scm" "" "Guile"
	WriteRegStr HKCR ".scm" "Guile" "Guile"
	WriteRegStr HKCR ".scm" "Content Type" "text/x-guile"

;;scm_open:
	ReadRegStr $R0 HKCR "Guile\shell\open\command" ""
	;;StrCmp $R0 "" 0 scm_auto_file
	WriteRegStr HKCR "Guile\shell" "" "open"
	# %1 is the GUILE command, so must be quoted bo the space
	WriteRegExpandStr HKCR "Guile\shell\open\command" "" '"$INSTDIR\usr\bin\guile-windows.exe" "%1" %2 %3 %4 %5 %6 %7 %8 %9'

;;scm_auto_file:
	ReadRegStr $R0 HKCR "scm_auto_file\shell\open\command" ""
	;;StrCmp $R0 "" 0 scm_end
	WriteRegStr HKCR "scm_auto_file\shell" "" "open"
	# %1 is the GUILE command, so must be quoted bo the space
	WriteRegExpandStr HKCR "scm_auto_file\shell\open\command" "" '"$INSTDIR\usr\bin\guile-windows.exe" "%1" %2 %3 %4 %5 %6 %7 %8 %9'
;;scm_end:	
FunctionEnd

!include "FontName.nsh"
!include "FontReg.nsh"

Function postinstall_schikkers_list
;;	!insertmacro InstallTTFFont "${ROOT}\usr\share\lilypond\current\fonts\ttf\Emmentaler-20.ttf"

	StrCpy $FONT_DIR "$WINDIR\Fonts"

	CopyFiles /silent "$INSTDIR\usr\share\lilypond\current\fonts\otf\Emmentaler-20.otf" "$WINDIR\Fonts\Emmentaler-20.otf"
	!insertmacro InstallFONFont "${ROOT}\usr\share\lilypond\current\fonts\otf\Emmentaler-20.otf" "Emmentaler-20 (OpenType)"

	CopyFiles /silent "$INSTDIR\usr\share\lilypond\current\fonts\otf\CenturySchL-BoldItal.otf" "$WINDIR\Fonts\CenturySchL-BoldItal.otf"
	!insertmacro InstallFONFont "${ROOT}\usr\share\lilypond\current\fonts\otf\CenturySchL-BoldItal.otf" "Century Schoolbook Bold Italic (Open Type)"

	CopyFiles /silent "$INSTDIR\usr\share\lilypond\current\fonts\otf\CenturySchL-Bold.otf" "$WINDIR\Fonts\CenturySchL-Bold.otf"
	!insertmacro InstallFONFont "${ROOT}\usr\share\lilypond\current\fonts\otf\CenturySchL-Bold.otf" "Century Schoolbook Bold (OpenType)"

	CopyFiles /silent "$INSTDIR\usr\share\lilypond\current\fonts\otf\CenturySchL-Ital.otf" "$WINDIR\Fonts\CenturySchL-Ital.otf"
	!insertmacro InstallFONFont "${ROOT}\usr\share\lilypond\current\fonts\otf\CenturySchL-Ital.otf" "Century Schoolbook Italic (OpenType)"

	CopyFiles /silent "$INSTDIR\usr\share\lilypond\current\fonts\otf\CenturySchL-Roma.otf" "$WINDIR\Fonts\CenturySchL-Roma.otf"
	!insertmacro InstallFONFont "${ROOT}\usr\share\lilypond\current\fonts\otf\CenturySchL-Roma.otf" "Century Schoolbook Roman (OpenType)"

	ClearErrors
FunctionEnd

Function un.install_schikkers_list_ttf
;	!insertmacro RemoveFONFont "Emmentaler-20.otf"
	Delete "$WINDIR\Fonts\Emmentaler-20.otf"
	Delete "$WINDIR\Fonts\CenturySchL-BoldItal.otf"
	Delete "$WINDIR\Fonts\CenturySchL-Bold.otf"
	Delete "$WINDIR\Fonts\CenturySchL-Ital.otf"
	Delete "$WINDIR\Fonts\CenturySchL-Roma.otf"
	ClearErrors
FunctionEnd
