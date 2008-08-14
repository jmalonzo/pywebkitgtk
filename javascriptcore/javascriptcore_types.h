/* PyWebKitGtk - Python bindings to WebKit/GTK+
 *
 * Copyright (C) 2007-2008  Jan Michael Alonzo <jmalonzo@unpluggable.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA  02110-1301 USA
 */

#ifndef PYWEBKITGTK_WRAP_JSC_H
#define PYWEBKITGTK_WRAP_JSC_H

#undef _POSIX_C_SOURCE
#include <Python.h>

#include <JavaScriptCore/JSContextRef.h>

typedef struct {
    PyObject_HEAD
    JSGlobalContextRef obj;
} JSGlobalContextRef_object;

/* Functions to wrap JavaScriptCore Python objects -> JavaScriptCore C objects */
#define JSGlobalContextRef_get(v) (((v) == Py_None) ? NULL : (((JSGlobalContextRef_object *)(PyObject_GetAttr(v,PyString_FromString("_o"))))->obj));

PyObject* wrap_JSGlobalContextRef(JSGlobalContextRef jsglobalref);

#endif /* PYWEBKITGTK_WRAP_JSC_H */
