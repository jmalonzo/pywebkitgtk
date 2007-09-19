INCLUDES = \
	$(PYTHON_INCLUDES)	\
	$(PYGTK_CFLAGS)		\
	$(WEBKITGDK_CFLAGS)

defsdir = $(datadir)/pygtk/2.0/defs
defs_DATA = webkitgtk.defs

pkgpythondir = $(pyexecdir)/gtk-2.0
pkgpyexecdir = $(pyexecdir)/gtk-2.0

webkitgtkdir = $(pkgpyexecdir)/webkitgtk

pkgpyexec_LTLIBRARIES = webkitgtk.la

webkitgtk_la_CFLAGS = $(GTK_CFLAGS) $(WEBKITGDK_CFLAGS)
webkitgtk_la_LDFLAGS = -module -avoid-version \
	-export-symbols-regex initwebkitgtk
webkitgtk_la_LIBADD = $(WEBKITGDK_LIBS)
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

uninstall-hook:
	-rmdir $(webkitgtkdir)

CLEANFILES = \
	webkitgtk.c \
	webkitgtk_la-webkitgtk.loT	

EXTRA_DIST = \
	webkitgtk.override \
	webkitgtk.defs
