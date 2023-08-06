/*[clinic input]
preserve
[clinic start generated code]*/

PyDoc_STRVAR(_fspacker_dumps__doc__,
"dumps($module, obj, /, *, version=2, recursiveLimit=512)\n"
"--\n"
"\n"
"Pack all supported variable type to bytes\n"
"\n"
"  obj\n"
"    Object to pack\n"
"  version\n"
"    Protocol version\n"
"  recursiveLimit\n"
"    Recursive limit");

#define _FSPACKER_DUMPS_METHODDEF    \
    {"dumps", (PyCFunction)(void(*)(void))_fspacker_dumps, METH_FASTCALL|METH_KEYWORDS, _fspacker_dumps__doc__},

static PyObject *
_fspacker_dumps_impl(PyObject *module, PyObject *obj, Py_ssize_t version,
                     Py_ssize_t recursiveLimit);

static PyObject *
_fspacker_dumps(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    static const char * const _keywords[] = {"", "version", "recursiveLimit", NULL};
    static _PyArg_Parser _parser = {NULL, _keywords, "dumps", 0, 0, 0, 0, 0, 0};
    PyObject *argsbuf[3];
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 1;
    PyObject *obj;
    Py_ssize_t version = 2;
    Py_ssize_t recursiveLimit = 512;

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser, 1, 1, 0, argsbuf);
    if (!args) {
        goto exit;
    }
    obj = args[0];
    if (!noptargs) {
        goto skip_optional_kwonly;
    }
    if (args[1]) {
        {
            Py_ssize_t ival = -1;
            PyObject *iobj = PyNumber_Index(args[1]);
            if (iobj != NULL) {
                ival = PyLong_AsSsize_t(iobj);
                Py_DECREF(iobj);
            }
            if (ival == -1 && PyErr_Occurred()) {
                goto exit;
            }
            version = ival;
        }
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    {
        Py_ssize_t ival = -1;
        PyObject *iobj = PyNumber_Index(args[2]);
        if (iobj != NULL) {
            ival = PyLong_AsSsize_t(iobj);
            Py_DECREF(iobj);
        }
        if (ival == -1 && PyErr_Occurred()) {
            goto exit;
        }
        recursiveLimit = ival;
    }
skip_optional_kwonly:
    return_value = _fspacker_dumps_impl(module, obj, version, recursiveLimit);

exit:
    return return_value;
}

PyDoc_STRVAR(_fspacker_dump__doc__,
"dump($module, obj, file, /, *, version=2, recursiveLimit=512)\n"
"--\n"
"\n"
"Pack all supported variable type to bytes\n"
"\n"
"  obj\n"
"    Object to pack\n"
"  file\n"
"    Writeable stream in byte mode\n"
"  version\n"
"    Protocol version\n"
"  recursiveLimit\n"
"    Recursive limit\n"
"\n"
"The *file* argument must have a write() method that accepts a single\n"
"bytes argument.  It can thus be a file object opened for binary\n"
"writing, an io.BytesIO instance, or any other custom object that meets\n"
"this interface.");

#define _FSPACKER_DUMP_METHODDEF    \
    {"dump", (PyCFunction)(void(*)(void))_fspacker_dump, METH_FASTCALL|METH_KEYWORDS, _fspacker_dump__doc__},

static PyObject *
_fspacker_dump_impl(PyObject *module, PyObject *obj, PyObject *file,
                    Py_ssize_t version, Py_ssize_t recursiveLimit);

static PyObject *
_fspacker_dump(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    static const char * const _keywords[] = {"", "", "version", "recursiveLimit", NULL};
    static _PyArg_Parser _parser = {NULL, _keywords, "dump", 0, 0, 0, 0, 0, 0};
    PyObject *argsbuf[4];
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 2;
    PyObject *obj;
    PyObject *file;
    Py_ssize_t version = 2;
    Py_ssize_t recursiveLimit = 512;

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser, 2, 2, 0, argsbuf);
    if (!args) {
        goto exit;
    }
    obj = args[0];
    file = args[1];
    if (!noptargs) {
        goto skip_optional_kwonly;
    }
    if (args[2]) {
        {
            Py_ssize_t ival = -1;
            PyObject *iobj = PyNumber_Index(args[2]);
            if (iobj != NULL) {
                ival = PyLong_AsSsize_t(iobj);
                Py_DECREF(iobj);
            }
            if (ival == -1 && PyErr_Occurred()) {
                goto exit;
            }
            version = ival;
        }
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    {
        Py_ssize_t ival = -1;
        PyObject *iobj = PyNumber_Index(args[3]);
        if (iobj != NULL) {
            ival = PyLong_AsSsize_t(iobj);
            Py_DECREF(iobj);
        }
        if (ival == -1 && PyErr_Occurred()) {
            goto exit;
        }
        recursiveLimit = ival;
    }
skip_optional_kwonly:
    return_value = _fspacker_dump_impl(module, obj, file, version, recursiveLimit);

exit:
    return return_value;
}

PyDoc_STRVAR(_fspacker_loads__doc__,
"loads($module, obj, /, *, maxIndexSize=0, recursiveLimit=512)\n"
"--\n"
"\n"
"Unpack bytes.\n"
"\n"
"  obj\n"
"    Object to pack\n"
"  maxIndexSize\n"
"    Maximum index size\n"
"  recursiveLimit\n"
"    Recursive limit");

#define _FSPACKER_LOADS_METHODDEF    \
    {"loads", (PyCFunction)(void(*)(void))_fspacker_loads, METH_FASTCALL|METH_KEYWORDS, _fspacker_loads__doc__},

static PyObject *
_fspacker_loads_impl(PyObject *module, PyObject *obj,
                     Py_ssize_t maxIndexSize, Py_ssize_t recursiveLimit);

static PyObject *
_fspacker_loads(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    static const char * const _keywords[] = {"", "maxIndexSize", "recursiveLimit", NULL};
    static _PyArg_Parser _parser = {NULL, _keywords, "loads", 0, 0, 0, 0, 0, 0};
    PyObject *argsbuf[3];
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 1;
    PyObject *obj;
    Py_ssize_t maxIndexSize = 0;
    Py_ssize_t recursiveLimit = 512;

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser, 1, 1, 0, argsbuf);
    if (!args) {
        goto exit;
    }
    obj = args[0];
    if (!noptargs) {
        goto skip_optional_kwonly;
    }
    if (args[1]) {
        {
            Py_ssize_t ival = -1;
            PyObject *iobj = PyNumber_Index(args[1]);
            if (iobj != NULL) {
                ival = PyLong_AsSsize_t(iobj);
                Py_DECREF(iobj);
            }
            if (ival == -1 && PyErr_Occurred()) {
                goto exit;
            }
            maxIndexSize = ival;
        }
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    {
        Py_ssize_t ival = -1;
        PyObject *iobj = PyNumber_Index(args[2]);
        if (iobj != NULL) {
            ival = PyLong_AsSsize_t(iobj);
            Py_DECREF(iobj);
        }
        if (ival == -1 && PyErr_Occurred()) {
            goto exit;
        }
        recursiveLimit = ival;
    }
skip_optional_kwonly:
    return_value = _fspacker_loads_impl(module, obj, maxIndexSize, recursiveLimit);

exit:
    return return_value;
}

PyDoc_STRVAR(_fspacker_load__doc__,
"load($module, file, /, *, maxIndexSize=0, recursiveLimit=512)\n"
"--\n"
"\n"
"Unpack bytes.\n"
"\n"
"  file\n"
"    Readable file stream in byte mode\n"
"  maxIndexSize\n"
"    Maximum index size\n"
"  recursiveLimit\n"
"    Recursive limit");

#define _FSPACKER_LOAD_METHODDEF    \
    {"load", (PyCFunction)(void(*)(void))_fspacker_load, METH_FASTCALL|METH_KEYWORDS, _fspacker_load__doc__},

static PyObject *
_fspacker_load_impl(PyObject *module, PyObject *stream,
                    Py_ssize_t maxIndexSize, Py_ssize_t recursiveLimit);

static PyObject *
_fspacker_load(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    static const char * const _keywords[] = {"", "maxIndexSize", "recursiveLimit", NULL};
    static _PyArg_Parser _parser = {NULL, _keywords, "load", 0, 0, 0, 0, 0, 0};
    PyObject *argsbuf[3];
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 1;
    PyObject *stream;
    Py_ssize_t maxIndexSize = 0;
    Py_ssize_t recursiveLimit = 512;

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser, 1, 1, 0, argsbuf);
    if (!args) {
        goto exit;
    }
    stream = args[0];
    if (!noptargs) {
        goto skip_optional_kwonly;
    }
    if (args[1]) {
        {
            Py_ssize_t ival = -1;
            PyObject *iobj = PyNumber_Index(args[1]);
            if (iobj != NULL) {
                ival = PyLong_AsSsize_t(iobj);
                Py_DECREF(iobj);
            }
            if (ival == -1 && PyErr_Occurred()) {
                goto exit;
            }
            maxIndexSize = ival;
        }
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    {
        Py_ssize_t ival = -1;
        PyObject *iobj = PyNumber_Index(args[2]);
        if (iobj != NULL) {
            ival = PyLong_AsSsize_t(iobj);
            Py_DECREF(iobj);
        }
        if (ival == -1 && PyErr_Occurred()) {
            goto exit;
        }
        recursiveLimit = ival;
    }
skip_optional_kwonly:
    return_value = _fspacker_load_impl(module, stream, maxIndexSize, recursiveLimit);

exit:
    return return_value;
}
/*[clinic end generated code: output=5a8d51595fe59862 input=a9049054013a1b77]*/
