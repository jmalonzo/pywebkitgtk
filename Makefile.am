
srcdir = @srcdir@
VPATH = @srcdir@

webkit_defs :=
webkit_sources :=
webkit_py_sources :=
nodist_webkit_sources :=
webkit_cflags :=

CREATEDEFS = $(PYTHON) $(PYGTK_CODEGENDIR)/createdefs.py

defsdir = $(pkgdatadir)/defs
defs_DATA = $(webkit_defs)

common_ldflags = -module -avoid-version

pkgpythondir = $(pyexecdir)/webkit
pkgpyexecdir = $(pyexecdir)/webkit

webkitdir = $(pkgpyexecdir)/webkit

# pywebkitgtk library
pkgpyexec_LTLIBRARIES = webkit.la

webkit_la_CPPFLAGS = $(PYTHON_INCLUDES) $(DEPS_CPPFLAGS) $(WEBKIT_CPPFLAGS) $(webkit_cflags)
webkit_la_CFLAGS = $(DEPS_CFLAGS) $(WEBKIT_CFLAGS)
webkit_la_LDFLAGS = $(common_ldflags) -export-symbols-regex initwebkit
webkit_la_LIBADD = $(DEPS_LIBS) $(WEBKIT_LIBS)
webkit_la_SOURCES = $(webkit_sources)
nodist_webkit_la_SOURCES = $(nodist_webkit_sources)

# Python sources
webkit_py_sources += \
	webkit/__init__.py
pkgpython_DATA = $(webkit_py_sources)

# Build components
webkit_sources += \
	webkit/webkitmodule.c \
	javascriptcore/javascriptcore_types.c \
	javascriptcore/javascriptcore_types.h
nodist_webkit_sources += webkit/webkit.c

# WebKit/Gtk definitions
webkit_defs += $(srcdir)/webkit/webkit-base-types.defs $(srcdir)/webkit/webkit-1.1-types.defs
webkit_defs += $(srcdir)/webkit/webkit-1.0.2.defs $(srcdir)/webkit/webkit-1.1.defs

webkit_deps := \
	$(srcdir)/webkit/webkit.override \
	webkit/webkit.defs \
	webkit/webkit.defs.c

webkit/webkit.c: $(webkit_deps)

webkit/webkit.defs: $(webkit_defs)
	$(CREATEDEFS) $@ $(webkit_defs)

# FIXME: this is causing a build issue in ArchLinux. Figure out why
# disable for now since line is not really critical.
# 	&& ! grep -q -v "^\*\*\*INFO\*\*\*" $(*D)/$(*F).errors
%.defs.c:
	($(PYGOBJECT_CODEGEN) \
            --register $(PYGTK_DEFSDIR)/gdk-types.defs \
            --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override $(srcdir)/$(*D)/$(*F).override \
	    --prefix py$(*F) $(*D)/$(*F).defs) 2>&1 > $(*D)/gen-$(*F).c | tee $(*D)/$(*F).errors \
	&& cp $(*D)/gen-$(*F).c $(*D)/$(*F).c \
	&& rm -f $(*D)/gen-$(*F).c

dist-hook: ChangeLog

ChangeLog: 
	git log --stat > ChangeLog

uninstall-hook:
	-rmdir $(webkitdir)

MAINTAINERCLEANFILES = \
	ChangeLog \
	$(srcdir)/aclocal.m4 \
	$(srcdir)/config.h.in \
	$(srcdir)/compile \
	$(srcdir)/config.guess \
	$(srcdir)/config.sub \
	$(srcdir)/configure \
	$(srcdir)/depcomp \
	$(srcdir)/install-sh \
	$(srcdir)/ltmain.sh \
	$(srcdir)/missing

CLEANFILES = \
	config.lt \
	demos/inspector.pyc \
	$(srcdir)/webkit/gen-webkit.c \
	$(builddir)/webkit/webkit.c \
	webkit/webkit.defs \
	webkit/webkit-types.defs \
	$(builddir)/webkit/webkit.errors \
	Makefile.in \
	pywebkitgtk-1.0.pc

EXTRA_DIST = \
	AUTHORS \
	COPYING \
	INSTALL \
	MAINTAINERS \
	NEWS \
	README \
	demos/inspector.py \
	demos/browser.py \
	webkit/webkit.override \
	tests/test_webbackforwardlist.py \
	tests/test_webframe.py \
	tests/test_webnavigationaction.py \
	$(webkit_types_defs) \
	$(webkit_defs) \
	$(webkit_py_sources)
