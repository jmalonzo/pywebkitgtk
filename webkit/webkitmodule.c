/*
 * Copyright (C) 2006-2007, Red Hat, Inc.
 * Copyright (C) 2007-2008 Jan Michael Alonzo <jmalonzo@unpluggable.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */
#include <Python.h>
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

/* include this first, before NO_IMPORT_PYGOBJECT is defined */
#include <pygobject.h>
#include <pygtk/pygtk.h>

extern PyMethodDef pywebkit_functions[];

void pywebkit_register_classes (PyObject *d);

#ifdef HAVE_GJS
extern PyMethodDef pygjs_functions[];
void pygjs_register_classes    (PyObject *d);
#endif

DL_EXPORT(void)
initwebkit(void)
{
    PyObject *m, *d;

    if (!pygobject_init(-1, -1, -1)) {
        PyErr_Print();
        Py_FatalError ("can't initialise module gobject");
    }

    init_pygtk();

    /* webkit module */
    m = Py_InitModule ("webkit", pywebkit_functions);
    d = PyModule_GetDict (m);
    pywebkit_register_classes (d);

#ifdef HAVE_GJS
    /* webkit.gjs module */
    m = Py_InitModule ("webkit.gjs", pygjs_functions);
    d = PyModule_GetDict(m);
    pygjs_register_classes (d);
#endif

    if (PyErr_Occurred ()) {
        PyErr_Print();
        Py_FatalError ("can't initialise module webkit.gjs");
    }
}
