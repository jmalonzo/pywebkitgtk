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
