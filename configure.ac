# configure script for pywebkitgtk

m4_define([pywebkitgtk_major_version], [1])
m4_define([pywebkitgtk_minor_version], [0])
m4_define([pywebkitgtk_micro_version], [99])

m4_define([pywebkitgtk_version],
          [pywebkitgtk_major_version.pywebkitgtk_minor_version.pywebkitgtk_micro_version])

m4_define([webkit_stable_version], [1.0.2])

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
                  pygtk-2.0,
                  webkit-1.0])
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

dnl check which .defs file we should use
dnl 
dnl webkit-stable.defs is for upstream webkit/gtk stable releases
dnl webkit-dev.defs is for webkit/gtk ToT installations
AC_MSG_CHECKING(which definitions file to use)
PYWEBKIT_DEFS="webkit-stable.defs"
webkit_installed_version=`$PKG_CONFIG --modversion webkit-1.0`
if test $webkit_installed_version > $webkit_stable_version; then
   PYWEBKIT_DEFS="webkit-dev.defs"
fi
AC_SUBST(PYWEBKIT_DEFS)
AC_MSG_RESULT($PYWEBKIT_DEFS)

dnl output
AC_CONFIG_FILES([
Makefile
pywebkitgtk-1.0.pc:pywebkitgtk.pc.in
])

AC_OUTPUT
