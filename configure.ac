# configure script for pywebkitgtk

# Version numbers. This follows the upstream WebKit versioning
# If there is a discrepancy, please file a defect report against pywebkitgtk
m4_define([pywebkitgtk_major_version], [1])
m4_define([pywebkitgtk_minor_version], [0])
m4_define([pywebkitgtk_micro_version], [2])
m4_define([pywebkitgtk_version],
          [pywebkitgtk_major_version.pywebkitgtk_minor_version.pywebkitgtk_micro_version])

# Set some build info. Right now it's a string and datetime
# format: snapshot-yymmdd
m4_define(pywebkitgtk_build_info, [snapshot-080717])

AC_INIT([pywebkitgtk],
        [pywebkitgtk_version-pywebkitgtk_build_info],
        [http://code.google.com/p/pywebkitgtk/issues])

AC_PREREQ([2.59])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_SRCDIR([configure.ac])
AC_CONFIG_HEADERS([config.h])

AM_INIT_AUTOMAKE([1.9])

AM_MAINTAINER_MODE

AC_DISABLE_STATIC
AC_PROG_LIBTOOL

dnl check for python
AM_PATH_PYTHON(2.4)
AM_CHECK_PYTHON_HEADERS(,[AC_MSG_ERROR(could not find Python headers)])

dnl get rid of -export-dynamic stuff from the configure flags...
export_dynamic=`(./libtool --config; echo eval echo \\$export_dynamic_flag_spec) | sh`

dnl check for dependencies
PKG_CHECK_MODULES(DEPS, 
                  [libxslt,
                  pygtk-2.0,
                  webkit-1.0])
AC_SUBST(DEPS_CFLAGS)
AC_SUBST(DEPS_LIBS)
AC_SUBST(DEPS_CPPFLAGS)

dnl python code gen
AC_PATH_PROG(PYGTK_CODEGEN, pygtk-codegen-2.0, no)
if test "x$PYGTK_CODEGEN" = xno; then
   AC_MSG_ERROR(could not find pygtk-codegen-2.0 script)
fi

dnl check for pygtk defsdir
AC_MSG_CHECKING(for pygtk defs)
PYGTK_DEFSDIR=`$PKG_CONFIG --variable=defsdir pygtk-2.0`
AC_SUBST(PYGTK_DEFSDIR)
AC_MSG_RESULT($PYGTK_DEFSDIR)

dnl output
AC_OUTPUT([
Makefile
])
