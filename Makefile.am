defsdir = $(datadir)/pygtk/2.0/defs
defs_DATA = $(PYWEBKIT_DEFS)

common_ldflags = -module -avoid-version

pkgpythondir = $(pyexecdir)/gtk-2.0
pkgpyexecdir = $(pyexecdir)/gtk-2.0

webkitdir = $(pkgpyexecdir)/webkit

pkgpyexec_LTLIBRARIES = webkit.la

webkit_la_CPPFLAGS = $(PYTHON_INCLUDES) $(DEPS_CPPFLAGS)
webkit_la_CFLAGS = $(DEPS_CFLAGS)
webkit_la_LDFLAGS = $(common_ldflags) -export-symbols-regex initwebkit
webkit_la_LIBADD = $(DEPS_LIBS)
webkit_la_SOURCES = \
	webkitmodule.c \
	javascriptcore/javascriptcore_types.c \
	javascriptcore/javascriptcore_types.h
nodist_webkit_la_SOURCES = webkit.c

webkit.c: .defs.c

.defs.c: webkit.override webkit-stable.defs webkit-dev.defs
	cp $(PYWEBKIT_DEFS) webkit.defs
	(cd $(srcdir) \
	 && $(PYGOBJECT_CODEGEN) \
	    --register $(PYGTK_DEFSDIR)/gdk-types.defs \
	    --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override webkit.override \
	    --prefix pywebkit webkit.defs) 2>&1 >gen-webkit.c | tee webkit.errors \
	&& ! grep -q -v "^\*\*\*INFO\*\*\*" webkit.errors \
	&& cp gen-webkit.c webkit.c \
	&& rm -f gen-webkit.c

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
	webkit.defs \
	webkit.errors \
	pywebkitgtk-1.0.pc

EXTRA_DIST = \
	AUTHORS \
	COPYING \
	INSTALL \
	MAINTAINERS \
	NEWS \
	README \
	demos/webbrowser.py \
	webkit.override \
	webkit-dev.defs \
	webkit-stable.defs

