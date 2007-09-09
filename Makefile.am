INCLUDES =					\
	$(DEPS_CFLAGS)				\
	$(PYTHON_INCLUDES)			\
	$(PYGTK_CFLAGS)				\
	-I$(top_srcdir)/webkitgtk

pkglib_LTLIBRARIES = webkit.la

webkit_la_LDFLAGS = -module -avoid-version
webkit_la_LIBADD = 				\
	-L. -lWebKitGdk

webkit_la_SOURCES = 			\
	webkitgtk.c			\
	webkitgtkmodule.c

webkitgtk.c: webkitgtk.defs webkitgtk.override

CLEANFILES = webkitgtk.c
EXTRA_DIST = webkitgtk.override webkitgtk.defs

.defs.c:
	(cd $(srcdir)\
	 && $(PYGTK_CODEGEN) \
	    --register $(PYGTK_DEFSDIR)/gdk-types.defs \
	    --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override $*.override \
	    --prefix py$* $*.defs) > gen-$*.c \
	&& cp gen-$*.c $*.c \
	&& rm -f gen-$*.c
