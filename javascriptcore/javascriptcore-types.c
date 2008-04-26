/* PyWebKitGtk - Python bindings to WebKit/GTK+
 *
 * Copyright (C) 2007  Jan Michael Alonzo <jmalonzo@unpluggable.com>
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

#include "javascriptcore-types.h"

/** functions to wrap C objects -> Python Objects */

PyObject* wrap_JSGlobalContextRef(JSGlobalContextRef jsglobalref)
{
    PyObject *ret;

    if (jsglobalref == NULL) {
        Py_INCREF (Py_None);
        return (Py_None);
    }

    ret = PyCObject_FromVoidPtrAndDesc ((void *) jsglobalref, (char *)
                                        "JSGlobalContextRef", NULL);
    return (ret);
}


 
