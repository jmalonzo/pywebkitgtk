/*
 * Copyright (C) 2006-2007, Red Hat, Inc.
 * Copyright (C) 2009 Jan Michael Alonzo <jmalonzo@gmail.com>
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

#include <glib.h>
/* include this first, before NO_IMPORT_PYGOBJECT is defined */
#include <pygobject.h>
#include <pygtk/pygtk.h>

#include <libsoup/soup.h>


void *webkit_get_default_session(void);
void pywebkit_register_classes (PyObject *d);
void pywebkit_add_constants(PyObject *module, const gchar *strip_prefix);


static PyObject *
pywebkit_set_proxy(PyObject *obj, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"proxy_uri", 0};
    const char *uri;
    SoupSession *session;
    SoupURI *proxy_uri;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", kwlist, &uri))
        return NULL;

    proxy_uri = soup_uri_new(uri);
    if (!proxy_uri) {
        PyErr_SetString(PyExc_ValueError, "malformed proxy uri");
        return NULL;
    }
    session = webkit_get_default_session();
    g_object_set(session, "proxy-uri", proxy_uri, NULL);
    soup_uri_free(proxy_uri);
    
    Py_INCREF(Py_None);
    return Py_None;
}


extern PyMethodDef pywebkit_functions[];

static PyMethodDef pywebkit_extras[] = {
    {"set_proxy", (PyCFunction)pywebkit_set_proxy, METH_VARARGS | METH_KEYWORDS,
        PyDoc_STR("set_proxy(proxy_uri) - set the webkit proxy")},
    {NULL, NULL}
};

static PyMethodDef *__methods;


/*
 * Return the number of method definitions found. 
 */
static size_t
_count_methods(PyMethodDef *methods)
{
    size_t i = 0;

    while (methods[i].ml_name) 
        i++;
    return i;
}


/*
 * Concatenate the local function definitions with those created by
 * pygobject's code generator.
 */
static PyMethodDef *
_merge_methods(PyMethodDef *md1, PyMethodDef *md2)
{
    PyMethodDef *methods;
    size_t md1_size;
    size_t md2_size;
    size_t total;
    int i;
    int j;

    /* compute size of new merged array */
    md1_size = _count_methods(md1);
    md2_size = _count_methods(md2);
    total = md1_size + md2_size + 1;

    /* allocate new array and copy method defs */
    methods = calloc(total, sizeof(PyMethodDef));
    j = 0;
    for (i = 0; i < md1_size; i++) {
        methods[j++] = md1[i];
    }
    /* copy md2 and include its sentinel */
    for (i = 0; i < md2_size + 1; i++) {
        methods[j++] = md2[i];
    }
    return methods;
}


/*
 * Clean up so Valgrind is happy.
 */
static void
_release_global_methods(void)
{
    if (__methods) {
        free(__methods);
        __methods = NULL;
    }
}


DL_EXPORT(void)
initwebkit(void)
{
    PyObject *m, *d;

    if (!pygobject_init(-1, -1, -1)) {
        PyErr_Print();
        Py_FatalError ("can't initialise module gobject");
    }

    init_pygobject();
    
    __methods = _merge_methods(pywebkit_functions, pywebkit_extras);
    m = Py_InitModule ("webkit", __methods);

    d = PyModule_GetDict (m);
    pywebkit_register_classes (d);
    pywebkit_add_constants (m, "WEBKIT_");

    if (PyErr_Occurred ()) {
        PyErr_Print();
        Py_FatalError ("can't initialise module webkit");
    }
    Py_AtExit(_release_global_methods);
}


