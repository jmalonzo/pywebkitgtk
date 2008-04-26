defsdir = $(datadir)/pygtk/2.0/defs
defs_DATA = webkit.defs

common_ldflags = -module -avoid-version $(PYTHON_LDFLAGS)

pkgpythondir = $(pyexecdir)/gtk-2.0
pkgpyexecdir = $(pyexecdir)/gtk-2.0

webkitdir = $(pkgpyexecdir)/webkit

pkgpyexec_LTLIBRARIES = webkit.la

webkit_la_CPPFLAGS = $(PYTHON_INCLUDES) $(DEPS_CPPFLAGS)
webkit_la_CFLAGS = $(DEPS_CFLAGS)
webkit_la_LDFLAGS = $(common_ldflags) -export-symbols-regex initwebkit
webkit_la_LIBADD = $(DEPS_LIBS) $(PYTHON_LIBS)
webkit_la_SOURCES = \
	webkitmodule.c \
	javascriptcore/javascriptcore_types.c \
	javascriptcore/javascriptcore_types.h
nodist_webkit_la_SOURCES = webkit.c

webkit.c: webkit.defs webkit.override

.defs.c:
	(cd $(srcdir) \
	 && $(PYGTK_CODEGEN) \
	    --register $(PYGTK_DEFSDIR)/gdk-types.defs \
	    --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override $*.override \
	    --prefix py$* $*.defs) 2>&1 >gen-$*.c | tee $*.errors \
	&& ! grep -q -v "^\*\*\*INFO\*\*\*" $*.errors \
	&& cp gen-$*.c $*.c \
	&& rm -f gen-$*.c

dist-hook: ChangeLog

ChangeLog: 
	git log --stat > ChangeLog

uninstall-hook:
	-rmdir $(webkitdir)

MAINTAINERCLEANFILES = \
	ChangeLog \
	aclocal.m4 \
	config.h.in \
	compile \
	config.guess \
	config.sub \
	configure \
	depcomp \
	install-sh \
	ltmain.sh \
	missing

CLEANFILES = \
	gen-webkit.c \
	webkit.c \
	Makefile.in \
	webkit.errors

EXTRA_DIST = \
	demos/webbrowser.py \
	webkit.override \
	webkit.defs
