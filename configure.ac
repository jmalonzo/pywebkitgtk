# configure script for pywebkitgtk

m4_define([pywebkitgtk_major_version], [1])
m4_define([pywebkitgtk_minor_version], [0])
m4_define([pywebkitgtk_micro_version], [99])

m4_define([pywebkitgtk_version],
          [pywebkitgtk_major_version.pywebkitgtk_minor_version.pywebkitgtk_micro_version])

AC_INIT([pywebkitgtk],
        [pywebkitgtk_version],
        [http://code.google.com/p/pywebkitgtk/issues])

AC_PREREQ([2.59])
AC_CONFIG_MACRO_DIR([m4])
AC_SUBST(ACLOCAL_AMFLAGS, "-I m4 -I .")

AC_CONFIG_SRCDIR([configure.ac])
AC_CONFIG_HEADERS([config.h])

AC_DEFINE_UNQUOTED(PYWEBKITGTK_VERSION, pywebkitgtk_version,
                   [The release version of Python WebKit Gtk+])
AC_DEFINE_UNQUOTED(PYWEBKITGTK_MAJOR_VERSION, pywebkitgtk_major_version,
                   [The major version of Python WebKit Gtk+.])
AC_DEFINE_UNQUOTED(PYWEBKITGTK_MINOR_VERSION, pywebkitgtk_minor_version,
                   [The minor version of Python WebKit Gtk+.])
AC_DEFINE_UNQUOTED(PYWEBKITGTK_MICRO_VERSION, pywebkitgtk_micro_version,
                   [The micro version of Python WebKit Gtk+.])

AM_INIT_AUTOMAKE([foreign subdir-objects])

AM_PROG_CC_C_O
AC_PROG_LIBTOOL

dnl check for python
AM_PATH_PYTHON(2.4)
AM_CHECK_PYTHON_HEADERS(,[AC_MSG_ERROR(could not find Python headers)])
py_prefix=`$PYTHON -c "import sys; print sys.prefix"`
PYTHON_INCLUDES="-I${py_prefix}/include/python${PYTHON_VERSION}"

dnl from pygtk: get rid of -export-dynamic stuff from the configure flags...
export_dynamic=`(./libtool --config; echo eval echo \\$export_dynamic_flag_spec) | sh`

dnl check for dependencies
dnl Check for libxslt until upstream WebKit checks for it as this is a webkit
dnl dep and not pywebkitgtk's.
PKG_CHECK_MODULES(DEPS, 
                  [libxslt,
                  pygtk-2.0])
AC_SUBST(DEPS_CFLAGS)
AC_SUBST(DEPS_LIBS)
AC_SUBST(DEPS_CPPFLAGS)

dnl python code gen
AC_PATH_PROGS(PYGOBJECT_CODEGEN, pygobject-codegen-2.0 pygtk-codegen-2.0, no)
if test "x$PYGOBJECT_CODEGEN" = xno; then
   AC_MSG_ERROR(could not find pygobject-codegen-2.0 script)
fi

dnl check for pygtk defsdir
AC_MSG_CHECKING(for pygtk defs)
PYGTK_DEFSDIR=`$PKG_CONFIG --variable=defsdir pygtk-2.0`
AC_SUBST(PYGTK_DEFSDIR)
AC_MSG_RESULT($PYGTK_DEFSDIR)

dnl check for pygtk codegen dir
AC_MSG_CHECKING(for pygtk codegendir)
PYGTK_CODEGENDIR=`$PKG_CONFIG --variable=codegendir pygtk-2.0`
AC_SUBST(PYGTK_CODEGENDIR)
AC_MSG_RESULT($PYGTK_CODEGENDIR)

dnl check if Gjs is wanted
AC_MSG_CHECKING([if Gjs will be included])
AC_ARG_WITH(gjs,
            AC_HELP_STRING([--with-gjs=@<:@yes/no@:>@],
                           [Include GJS JavaScriptCore binding [default=no]]),
            [with_gjs="yes"],[with_gjs="no"])
case "$with_gjs" in
     yes|no)     ;;
     *) AC_MSG_ERROR([Invalid option. Should be 'yes' or 'no']) ;;
esac
if test $with_gjs = "yes"; then
   AC_DEFINE([HAVE_GJS],[1],[Define to have GJS Support])
fi
AC_MSG_RESULT([$with_gjs])

dnl check for webkit versions installed
PKG_CHECK_MODULES(WEBKIT, webkit-1.0)
AC_SUBST(WEBKIT_CFLAGS)
AC_SUBST(WEBKIT_LIBS)
AC_SUBST(WEBKIT_CPPFLAGS)

dnl conditionals
AM_CONDITIONAL([HAVE_GJS],[test "$with_gjs" = "yes"])

dnl output
AC_CONFIG_FILES([
Makefile
pywebkitgtk-1.0.pc:pywebkitgtk.pc.in
])

AC_OUTPUT
