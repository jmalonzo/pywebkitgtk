INCLUDES = \
	$(PYTHON_INCLUDES)	\
	$(PYGTK_CFLAGS)		\
	$(WEBKITGTK_CFLAGS)

defsdir = $(datadir)/pygtk/2.0/defs
defs_DATA = webkitgtk.defs

pkgpythondir = $(pyexecdir)/gtk-2.0
pkgpyexecdir = $(pyexecdir)/gtk-2.0

webkitgtkdir = $(pkgpyexecdir)/webkitgtk

pkgpyexec_LTLIBRARIES = webkitgtk.la

webkitgtk_la_CFLAGS = $(GTK_CFLAGS) $(WEBKITGTK_CFLAGS)
webkitgtk_la_LDFLAGS = -module -avoid-version \
	-export-symbols-regex initwebkitgtk
webkitgtk_la_LIBADD = $(WEBKITGTK_LIBS)
webkitgtk_la_SOURCES = webkitgtkmodule.c
nodist_webkitgtk_la_SOURCES = webkitgtk.c

webkitgtk.c: webkitgtk.defs webkitgtk.override

.defs.c:
	(cd $(srcdir)\
	 && $(PYGTK_CODEGEN) \
	    --register $(PYGTK_DEFSDIR)/gdk-types.defs \
	    --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override $*.override \
	    --prefix py$* $*.defs) 2>&1 >gen-$*.c | tee $*.errors \
	&& ! grep -q -v "^\*\*\*INFO\*\*\*" $*.errors \
	&& cp gen-$*.c $*.c \
	&& rm -f gen-$*.c

dist-hook: ChangeLog

ChangeLog: .git/HEAD
	git log --stat > ChangeLog

uninstall-hook:
	-rmdir $(webkitgtkdir)


MAINTAINERCLEANFILES = \
	aclocal.m4 \
	compile \
	config.guess \
	config.sub \
	configure \
	depcomp \
	install-sh \
	ltmain.sh \
	missing \
	Makefile.in   

CLEANFILES = \
	gen-webkitgtk.c \
	webkitgtk.c \
	webkitgtk_la-webkitgtk.loT	

EXTRA_DIST = \
	webbrowser.py \
	webkitgtk.override \
	webkitgtk.defs
