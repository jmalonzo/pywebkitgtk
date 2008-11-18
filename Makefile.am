
webkit_defs :=
webkit_sources :=
nodist_webkit_sources :=
webkit_override :=
webkit_cflags :=

CREATEDEFS = $(PYTHON) $(PYGTK_CODEGENDIR)/createdefs.py

defsdir = $(PYGTK_DEFSDIR)
defs_DATA = $(webkit_defs)

common_ldflags = -module -avoid-version

pkgpythondir = $(pyexecdir)/gtk-2.0
pkgpyexecdir = $(pyexecdir)/gtk-2.0

webkitdir = $(pkgpyexecdir)/webkit

pkgpyexec_LTLIBRARIES = webkit.la

webkit_la_CPPFLAGS = $(PYTHON_INCLUDES) $(DEPS_CPPFLAGS) $(webkit_cflags)
webkit_la_CFLAGS = $(DEPS_CFLAGS)
webkit_la_LDFLAGS = $(common_ldflags) -export-symbols-regex initwebkit
webkit_la_LIBADD = $(DEPS_LIBS)
webkit_la_SOURCES = $(webkit_sources)
nodist_webkit_la_SOURCES = $(nodist_webkit_sources)

webkit_defs += $(PYWEBKIT_DEFS)
webkit_override += webkit/webkit.override
webkit_sources += \
	webkit/webkitmodule.c \
	javascriptcore/javascriptcore_types.c \
	javascriptcore/javascriptcore_types.h
nodist_webkit_sources += webkit/webkit.c

if HAVE_GJS
webkit_defs += gjs/gjs.defs
webkit_override += gjs/gjs.override
webkit_cflags += -I$(srcdir)/gjs
webkit_sources += gjs/gjs_internal.c
nodist_webkit_sources += gjs/gjs.c

gjs/gjs.c: gjs/gjs.defs gjs/gjs.override gjs/gjs.defs.c

endif

webkit/webkit.c: $(PYWEBKIT_DEFS) webkit/webkit.override webkit/webkit.defs webkit/webkit.defs.c

webkit/webkit.defs: $(PYWEBKIT_DEFS)
	$(CREATEDEFS) $@ $(PYWEBKIT_DEFS)

%.defs.c:
	(cd $(srcdir) \
	 && $(PYGOBJECT_CODEGEN) \
	    --register $(PYGTK_DEFSDIR)/gdk-types.defs \
	    --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override $(*D)/$(*F).override \
	    --prefix py$(*F) $(*D)/$(*F).defs) 2>&1 > $(*D)/gen-$(*F).c | tee $(*D)/$(*F).errors \
	&& ! grep -q -v "^\*\*\*INFO\*\*\*" $(*D)/$(*F).errors \
	&& cp $(*D)/gen-$(*F).c $(*D)/$(*F).c \
	&& rm -f $(*D)/gen-$(*F).c

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
	gjs/gen-gjs.c \
	gjs/gjs.errors \
	gjs/gjs.c \
	webkit/gen-webkit.c \
	webkit/webkit.c \
	webkit/webkit.defs \
	webkit/webkit.errors \
	Makefile.in \
	dummy.0.2 \
	pywebkitgtk-1.0.pc

EXTRA_DIST = \
	AUTHORS \
	COPYING \
	INSTALL \
	MAINTAINERS \
	NEWS \
	README \
	demos/webbrowser.py \
	gjs/gjs.defs \
	gjs/gjs.override \
	webkit/webkit.override \
	webkit/webkit-dev.defs \
	webkit/webkit-stable.defs
