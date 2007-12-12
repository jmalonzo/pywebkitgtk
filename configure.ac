dnl configure script for pywebkitgtk
dnl Copyright (C) Jan Michael Alonzo jmalonzo@unpluggable.com

AC_INIT([pywebkitgtk],[0.3],[jmalonzo@unpluggable.com])

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

GTK_DOC_CHECK

dnl get rid of -export-dynamic stuff from the configure flags...
export_dynamic=`(./libtool --config; echo eval echo \\$export_dynamic_flag_spec) | sh`

dnl check for gtk+
PKG_CHECK_MODULES(GTK, gtk+-2.0)

dnl check for pygtk
PKG_CHECK_MODULES(PYGTK, pygtk-2.0)
AC_SUBST(PYGTK_CFLAGS)

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

dnl check for webkitgtk
PKG_CHECK_MODULES(WEBKITGTK, WebKitGtk)
AC_SUBST(WEBKITGTK_CFLAGS)
AC_SUBST(WEBKITGTK_LIBS)

dnl output
AC_OUTPUT([
Makefile
])
