#include "Python.h"
#include <vector>
#include "_fspacker.h"
#include "clinic/_fspacker.cpp.h"
// CONSTANTS
static const Py_ssize_t ITEM_LIMIT = 4294967295;
// #define FSPACKER_DEBUG

// MEMOTABLE
#define MT_MINSIZE 16
#define PERTURB_SHIFT 5
struct PyMemoEntry {
	PyObject *me_key;
	Py_ssize_t me_value;
};
struct PyMemoTable {
	size_t mt_mask;
	size_t mt_used;
	size_t mt_allocated;
	PyMemoEntry *mt_table;
};
static PyMemoTable* PyMemoTable_New() {
	PyMemoTable *memo = (PyMemoTable*)PyMem_Malloc(sizeof(PyMemoTable));
	if (memo == NULL) {
		goto memoryError;
	}
	memo->mt_used = 0;
	memo->mt_allocated = MT_MINSIZE;
	memo->mt_mask = MT_MINSIZE - 1;
	memo->mt_table = (PyMemoEntry*)PyMem_Malloc(MT_MINSIZE * sizeof(PyMemoEntry));
	if (memo->mt_table == NULL) {
		goto memoryError;
	}
	memset(memo->mt_table, 0, MT_MINSIZE * sizeof(PyMemoEntry));
	return memo;
	memoryError:
	PyMem_Free(memo);
	PyErr_NoMemory();
	return NULL;
}
static void PyMemoTable_Clear(PyMemoTable *self) {
	self->mt_used = 0;
	memset(self->mt_table, 0, self->mt_allocated * sizeof(PyMemoEntry));
}
static void PyMemoTable_Del(PyMemoTable *self) {
	if (self == NULL)
		return;
	PyMemoTable_Clear(self);

	PyMem_Free(self->mt_table);
	PyMem_Free(self);
}
static PyMemoEntry* _PyMemoTable_Lookup(PyMemoTable *self, PyObject *key) {
	size_t i;
	size_t perturb;
	size_t mask = self->mt_mask;
	PyMemoEntry *table = self->mt_table;
	PyMemoEntry *entry;
	Py_hash_t hash = (Py_hash_t)key >> 3;

	i = hash & mask;
	entry = &table[i];
	if (entry->me_key == NULL || entry->me_key == key)
		return entry;

	for (perturb = hash; ; perturb >>= PERTURB_SHIFT) {
		i = (i << 2) + i + perturb + 1;
		entry = &table[i & mask];
		if (entry->me_key == NULL || entry->me_key == key)
			return entry;
	}
	Py_UNREACHABLE();
}
static int _PyMemoTable_ResizeTable(PyMemoTable *self, size_t min_size) {
	PyMemoEntry *oldtable = NULL;
	PyMemoEntry *oldentry, *newentry;
	size_t new_size = MT_MINSIZE;
	size_t to_process;

	assert(min_size > 0);

	if (min_size > PY_SSIZE_T_MAX) {
		PyErr_NoMemory();
		return -1;
	}

	/* Find the smallest valid table size >= min_size. */
	while (new_size < min_size) {
		new_size <<= 1;
	}
	/* new_size needs to be a power of two. */
	assert((new_size & (new_size - 1)) == 0);

	/* Allocate new table. */
	oldtable = self->mt_table;
	self->mt_table = PyMem_NEW(PyMemoEntry, new_size);
	if (self->mt_table == NULL) {
		self->mt_table = oldtable;
		PyErr_NoMemory();
		return -1;
	}
	self->mt_allocated = new_size;
	self->mt_mask = new_size - 1;
	memset(self->mt_table, 0, sizeof(PyMemoEntry) * new_size);

	/* Copy entries from the old table. */
	to_process = self->mt_used;
	for (oldentry = oldtable; to_process > 0; oldentry++) {
		if (oldentry->me_key != NULL) {
			to_process--;
			/* newentry is a pointer to a chunk of the new
				mt_table, so we're setting the key:value pair
				in-place. */
			newentry = _PyMemoTable_Lookup(self, oldentry->me_key);
			newentry->me_key = oldentry->me_key;
			newentry->me_value = oldentry->me_value;
		}
	}

	/* Deallocate the old table. */
	PyMem_Free(oldtable);
	return 0;
}
static Py_ssize_t* PyMemoTable_Get(PyMemoTable *self, PyObject *key) {
	PyMemoEntry *entry = _PyMemoTable_Lookup(self, key);
	if (entry->me_key == NULL)
		return NULL;
	return &entry->me_value;
}
static int PyMemoTable_Set(PyMemoTable *self, PyObject *key, Py_ssize_t value) {
	PyMemoEntry *entry;
	assert(key != NULL);
	entry = _PyMemoTable_Lookup(self, key);
	if (entry->me_key != NULL) {
		entry->me_value = value;
		return 0;
	}
	entry->me_key = key;
	entry->me_value = value;
	self->mt_used++;

	/* If we added a key, we can safely resize. Otherwise just return!
	 * If used >= 2/3 size, adjust size. Normally, this quaduples the size.
	 *
	 * Quadrupling the size improves average table sparseness
	 * (reducing collisions) at the cost of some memory. It also halves
	 * the number of expensive resize operations in a growing memo table.
	 *
	 * Very large memo tables (over 50K items) use doubling instead.
	 * This may help applications with severe memory constraints.
	 */
	if (SIZE_MAX / 3 >= self->mt_used && self->mt_used * 3 < self->mt_allocated * 2) {
		return 0;
	}
	// self->mt_used is always < PY_SSIZE_T_MAX, so this can't overflow.
	size_t desired_size = (self->mt_used > 50000 ? 2 : 4) * self->mt_used;
	return _PyMemoTable_ResizeTable(self, desired_size);
}
#undef MT_MINSIZE
#undef PERTURB_SHIFT

// MISC
struct bufferObject {
	char *buf;
	size_t length;
	size_t buf_size;
};
static int __fspacker_buffer_append(bufferObject *b, const char *data, size_t l) {
	char *buf = b->buf;
	size_t bs = b->buf_size;
	size_t len = b->length;
	#if defined(FSPACKER_DEBUG)
		printf("Writing %ld data to buffer: %ld/%ld\n", l, len, bs);
	#endif
	if (len + l > bs) {
		bs += l+((bs+l) >> 3);
		if (b->buf_size >= bs) {
			PyErr_SetNone(PyExc_OverflowError);
			return -1;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Resizing %zd buffer from %ld to %ld size\n", (size_t)buf, b->buf_size, bs);
		#endif
		buf = (char*)PyMem_Realloc(buf, bs);
		#if defined(FSPACKER_DEBUG)
			printf("New buffer pointer: %zd \n", (size_t)buf);
		#endif
		if (!buf) {
			PyErr_NoMemory();
			return -1;
		}
	}
	memcpy(buf + len, data, l);
	len += l;
	b->buf = buf;
	b->buf_size = bs;
	b->length = len;
	return 0;
}
#define _fspacker_buffer_append(buff, cache, len) __fspacker_buffer_append(buff, (const char*)cache, (size_t)len)
static PyObject* _fspacker_returnWithVersion(Py_ssize_t version, PyObject *ret) {
	if ( ret == NULL ) {
		return NULL;
	}
	PyObject *pret = PyTuple_New(2);
	PyObject *ver = PyLong_FromSsize_t(version);
	if (PyTuple_SetItem(pret, 0, ver) == -1 || PyTuple_SetItem(pret, 1, ret) == -1) {
		Py_DECREF(ver);
		Py_DECREF(ret);
		PyErr_NoMemory();
		return NULL;
	}
	return pret;
}

// _fspacker MODULE
static struct PyMethodDef _fspacker_methods[] = {
	_FSPACKER_DUMPS_METHODDEF
	_FSPACKER_DUMP_METHODDEF
	_FSPACKER_LOADS_METHODDEF
	_FSPACKER_LOAD_METHODDEF
	{NULL, NULL, 0, 0} /* sentinel */
};
struct FSPackerState {
	PyObject *PackerError;
	PyObject *PackingError;
	PyObject *UnpackingError;
};
static FSPackerState *_FSPacker_GetState(PyObject *module) {
	return (FSPackerState *)PyModule_GetState(module);
}
static int  _fspacker_traverse(PyObject *m, visitproc visit, void *arg) {
	FSPackerState *st = _FSPacker_GetState(m);
	Py_VISIT(st->PackerError);
	Py_VISIT(st->PackingError);
	Py_VISIT(st->UnpackingError);
	return 0;
}
static void _fspacker_ClearState(FSPackerState *st) {
	Py_CLEAR(st->PackerError);
	Py_CLEAR(st->PackingError);
	Py_CLEAR(st->UnpackingError);
}
static void _fspacker_free(PyObject *m) {
	_fspacker_ClearState(_FSPacker_GetState(m));
}
static int  _fspacker_clear(PyObject *m) {
	_fspacker_ClearState(_FSPacker_GetState(m));
	return 0;
}
PyDoc_STRVAR(_fspacker_module_doc, "C implementation for the FSPacker module.");
static struct PyModuleDef _fspackermodule = {
	PyModuleDef_HEAD_INIT,
	"_fspacker",             /* m_name */
	_fspacker_module_doc,    /* m_doc */
	sizeof(FSPackerState),   /* m_size */
	_fspacker_methods,       /* m_methods */
	NULL,                    /* m_reload */
	_fspacker_traverse,      /* m_traverse */
	_fspacker_clear,         /* m_clear */
	(freefunc)_fspacker_free /* m_free */
};
static FSPackerState* _fspacker_GetGlobalState(void) {
    return _FSPacker_GetState(PyState_FindModule(&_fspackermodule));
}
/*[clinic input]
module _fspacker
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=42a086fb32787909]*/
PyMODINIT_FUNC PyInit__fspacker(void) {
	PyObject *m;
	FSPackerState *st;

	m = PyState_FindModule(&_fspackermodule);
	if (m != NULL) {
		Py_INCREF(m);
		return m;
	}
	m = PyModule_Create(&_fspackermodule);
	if (m == NULL) {
		goto memoryError;
	}
	st = _FSPacker_GetState(m);
	st->PackerError = PyErr_NewException("_fspacker.PackerError", NULL, NULL);
	if (st->PackerError == NULL) {
		goto memoryError;
	}
	st->PackingError = PyErr_NewException("_fspacker.PackingError", st->PackerError, NULL);
	if (st->PackingError == NULL) {
		goto memoryError;
	}
	st->UnpackingError = PyErr_NewException("_fspacker.UnpackingError", st->PackerError, NULL);
	if (st->UnpackingError == NULL) {
		goto memoryError;
	}
	Py_INCREF(st->PackerError);
	if (PyModule_AddObject(m, "PackerError", st->PackerError) < 0) {
		goto memoryError;
	}
	Py_INCREF(st->PackingError);
	if (PyModule_AddObject(m, "PackingError", st->PackingError) < 0) {
		goto memoryError;
	}
	Py_INCREF(st->UnpackingError);
	if (PyModule_AddObject(m, "UnpackingError", st->UnpackingError) < 0)
	{
		goto memoryError;
	}
	return m;
	memoryError:
	PyErr_NoMemory();
	return NULL;
}

// EXPORTED FUNCTIONS
/*[clinic input]
_fspacker.dumps
  obj: object
    Object to pack
  /
  *
  version: Py_ssize_t = 2
    Protocol version
  recursiveLimit: Py_ssize_t = 512
    Recursive limit

Pack all supported variable type to bytes
[clinic start generated code]*/

static PyObject *
_fspacker_dumps_impl(PyObject *module, PyObject *obj, Py_ssize_t version,
                     Py_ssize_t recursiveLimit)
/*[clinic end generated code: output=46ce5ee15b3a51d5 input=7ec1b9be2ca05d90]*/
{
	(void)module;
	FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
	if ( recursiveLimit == 0 ) {
		PyErr_SetString(FSPackerModule->PackingError, "Recursive limit is invalid");
	}
	if (version == 2) {
		return _fspacker_packer_ver2(obj, NULL, recursiveLimit);
	}
	PyErr_Format(FSPackerModule->PackingError, "Unsupported packer version: %d", version);
	return NULL;
}


/*[clinic input]
_fspacker.dump
  obj: object
    Object to pack
  file: object
    Writeable stream in byte mode
  /
  *
  version: Py_ssize_t = 2
    Protocol version
  recursiveLimit: Py_ssize_t = 512
    Recursive limit

Pack all supported variable type to bytes

The *file* argument must have a write() method that accepts a single
bytes argument.  It can thus be a file object opened for binary
writing, an io.BytesIO instance, or any other custom object that meets
this interface.

[clinic start generated code]*/

static PyObject *
_fspacker_dump_impl(PyObject *module, PyObject *obj, PyObject *file,
                    Py_ssize_t version, Py_ssize_t recursiveLimit)
/*[clinic end generated code: output=8a8f1ba5f527a131 input=a26e53750a541ec9]*/
{
	(void)module;
	FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
	if ( recursiveLimit == 0 ) {
		PyErr_SetString(FSPackerModule->PackingError, "Recursive limit is invalid");
	}
	if (version == 2) {
		return _fspacker_packer_ver2(obj, file, recursiveLimit);
	}
	PyErr_Format(FSPackerModule->PackingError, "Unsupported packer version: %d", version);
	return NULL;
}


/*[clinic input]
_fspacker.loads
  obj: object
    Object to pack
  /
  *
  maxIndexSize: Py_ssize_t = 0
    Maximum index size
  recursiveLimit: Py_ssize_t = 512
    Recursive limit

Unpack bytes.
[clinic start generated code]*/

static PyObject *
_fspacker_loads_impl(PyObject *module, PyObject *obj,
                     Py_ssize_t maxIndexSize, Py_ssize_t recursiveLimit)
/*[clinic end generated code: output=3f2c98315ce4c9d3 input=b8fa4cf530eb7a29]*/
{
	(void)module;
	FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
	Py_ssize_t len;
	if (!PyBytes_CheckExact(obj)) {
		PyTypeObject *type = Py_TYPE(obj);
		PyErr_Format(FSPackerModule->UnpackingError, "Only bytes can be unpacked, not %.200s", type->tp_name);
		return NULL;
	}
	len = PyBytes_GET_SIZE(obj);
	if (!len) {
		PyErr_SetString(FSPackerModule->UnpackingError, "Nothing to unpack");
		return NULL;
	}
	const char *input = PyBytes_AS_STRING(obj);
	uint8_t version = (uint8_t)input[0];
	if (version == 0x02) {
		return _fspacker_returnWithVersion(2, _fspacker_unpacker_ver2(input, len, maxIndexSize, recursiveLimit));
	}
	else {
		PyErr_Format(FSPackerModule->UnpackingError, "Unsupported packed version: %d", version);
		return NULL;
	}
}


/*[clinic input]
_fspacker.load
  file as stream: object
    Readable file stream in byte mode
  /
  *
  maxIndexSize: Py_ssize_t = 0
    Maximum index size
  recursiveLimit: Py_ssize_t = 512
    Recursive limit

Unpack bytes.
[clinic start generated code]*/

static PyObject *
_fspacker_load_impl(PyObject *module, PyObject *stream,
                    Py_ssize_t maxIndexSize, Py_ssize_t recursiveLimit)
/*[clinic end generated code: output=8442d46cefe538dc input=7505c61f2bff2eed]*/
{
	(void)module;
	FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
	PyObject *readMethod = NULL;
	PyObject *obj = NULL;
	PyObject *ret = NULL;
	const char *input = NULL;
	PyTypeObject *type;
	uint8_t version;
	Py_ssize_t len;
	//
	// TODO Recode for on the fly data reading
	_Py_IDENTIFIER(read);
	if (_PyObject_LookupAttrId(stream, &PyId_read, &readMethod) < 0) {
		PyErr_SetString(FSPackerModule->UnpackingError, "Stream does not have read method");
		goto error;
	}
	if (readMethod == NULL) {
		PyErr_SetString(FSPackerModule->UnpackingError, "Unable to read from the stream");
		goto error;
	}
	obj = PyObject_CallFunctionObjArgs(readMethod, NULL);
	if (PyErr_Occurred() != NULL) {
		goto error;
	}
	if (obj == NULL) {
		PyErr_SetString(FSPackerModule->UnpackingError, "Unable to read from the stream");
		goto error;
	}
	len = PyObject_Length(obj);
	if (!len) {
		PyErr_SetString(FSPackerModule->UnpackingError, "Nothing to unpack");
		goto error;
	}
	type = Py_TYPE(obj);
	if (type != &PyBytes_Type) {
		PyErr_SetString(FSPackerModule->UnpackingError, "Stream is not in byte mode");
		goto error;
	}
	input = PyBytes_AS_STRING(obj);
	version = (uint8_t)input[0];
	if (version == 0x02) {
		ret = _fspacker_returnWithVersion(2, _fspacker_unpacker_ver2(input, len, maxIndexSize, recursiveLimit));
		Py_XDECREF(readMethod);
		Py_XDECREF(obj);
		return ret;
	}
	PyErr_Format(FSPackerModule->UnpackingError, "Unsupported packer version: %d", version);
	//
	if (0) {
		error:
		Py_XDECREF(readMethod);
		Py_XDECREF(obj);
	}
	return NULL;
}


// ===== PROTOCOL VERSION 2 =====
const uint8_t VER2_VINT_2BYTES           = 0xE5;
const uint8_t VER2_VINT_3BYTES           = 0xE6;
const uint8_t VER2_VINT_4BYTES           = 0xE7;
const uint8_t VER2_OP_NONE               = 0xE8;
const uint8_t VER2_OP_BOOL_FALSE         = 0xE9;
const uint8_t VER2_OP_BOOL_TRUE          = 0xEA;
const uint8_t VER2_OP_INTERGER           = 0xEB;
const uint8_t VER2_OP_NEG_INTERGER       = 0xEC;
const uint8_t VER2_OP_ZERO_INTERGER      = 0xED;
const uint8_t VER2_OP_CHAR_INTERGER      = 0xEE;
const uint8_t VER2_OP_NEG_CHAR_INTERGER  = 0xEF;
const uint8_t VER2_OP_SHORT_INTERGER     = 0xF0;
const uint8_t VER2_OP_NEG_SHORT_INTERGER = 0xF1;
const uint8_t VER2_OP_FLOAT              = 0xF2;
const uint8_t VER2_OP_ZERO_FLOAT         = 0xF3;
const uint8_t VER2_OP_INF_FLOAT          = 0xF4;
const uint8_t VER2_OP_NEG_INF_FLOAT      = 0xF5;
const uint8_t VER2_OP_UNICODE            = 0xF6;
const uint8_t VER2_OP_ZERO_UNICODE       = 0xF7;
const uint8_t VER2_OP_BYTES              = 0xF8;
const uint8_t VER2_OP_ZERO_BYTES         = 0xF9;
const uint8_t VER2_OP_LIST               = 0xFA;
const uint8_t VER2_OP_ZERO_LIST          = 0xFB;
const uint8_t VER2_OP_DICT               = 0xFC;
const uint8_t VER2_OP_ZERO_DICT          = 0xFD;
const uint8_t VER2_OP_SET                = 0xFE;
const uint8_t VER2_OP_ZERO_SET           = 0xFF;
// ---- PACKER ----
struct packerObject_ver2 {
	bufferObject *output;
	PyObject *stream;
	PyMemoTable *memo;
	FSPackerState *module;
	Py_ssize_t counter;
	Py_ssize_t stack;
	Py_ssize_t recursiveLimit;
};
// abstract
static int _fspacker_packer_ver2_parser(packerObject_ver2 *self, PyObject *obj);
// misc
static int _fspacker_ver2_write_indexNr(bufferObject *b, Py_ssize_t val) {
	unsigned char buf[5];
	size_t l = 1;
	if (val < VER2_VINT_2BYTES) {
		buf[0] = (unsigned char)(val & 0xff);
	}
	else if(val <= 0xFFFF) {
		l = 3;
		buf[0] = (unsigned char)VER2_VINT_2BYTES;
		buf[1] = (unsigned char)(val & 0xff);
		buf[2] = (unsigned char)((val >> 8) & 0xff);
	}
	else if(val <= 0xFFFFFF) {
		l = 4;
		buf[0] = (unsigned char)VER2_VINT_3BYTES;
		buf[1] = (unsigned char)(val & 0xff);
		buf[2] = (unsigned char)((val >> 8) & 0xff);
		buf[3] = (unsigned char)((val >> 16) & 0xff);
	}
	else if(val <= 0xFFFFFFFF) {
		l = 5;
		buf[0] = (unsigned char)VER2_VINT_4BYTES;
		buf[1] = (unsigned char)(val & 0xff);
		buf[2] = (unsigned char)((val >> 8) & 0xff);
		buf[3] = (unsigned char)((val >> 16) & 0xff);
		buf[4] = (unsigned char)((val >> 24) & 0xff);
	}
	else {
		FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
		PyErr_SetString(FSPackerModule->PackingError, "Too big number");
		return -1;
	}
	return _fspacker_buffer_append(b, buf, l);
}
static int _fspacker_ver2_write_vin(bufferObject *b, Py_ssize_t val) {
	unsigned char buf[5];
	size_t l = 1;
	if (val < 0xFD) {
		buf[0] = (unsigned char)(val & 0xff);
	}
	else if(val <= 0xFFFF) {
		l = 3;
		buf[0] = (unsigned char)0xFD;
		buf[1] = (unsigned char)(val & 0xff);
		buf[2] = (unsigned char)((val >> 8) & 0xff);
	}
	else if(val <= 0xFFFFFF) {
		l = 4;
		buf[0] = (unsigned char)0xFE;
		buf[1] = (unsigned char)(val & 0xff);
		buf[2] = (unsigned char)((val >> 8) & 0xff);
		buf[3] = (unsigned char)((val >> 16) & 0xff);
	}
	else if(val <= 0xFFFFFFFF) {
		l = 5;
		buf[0] = (unsigned char)0xFF;
		buf[1] = (unsigned char)(val & 0xff);
		buf[2] = (unsigned char)((val >> 8) & 0xff);
		buf[3] = (unsigned char)((val >> 16) & 0xff);
		buf[4] = (unsigned char)((val >> 24) & 0xff);
	}
	else {
		FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
		PyErr_SetString(FSPackerModule->PackingError, "Too big number");
		return -1;
	}
	return _fspacker_buffer_append(b, buf, l);
}
static int _fspacker_packer_ver2_register(packerObject_ver2 *self, PyObject *obj) {
	Py_ssize_t idx = self->counter;
	Py_ssize_t *indexNr = PyMemoTable_Get(self->memo, obj);
	if (indexNr != NULL) {
		#if defined(FSPACKER_DEBUG)
			printf("Already indexed on #%ld\n", (Py_ssize_t)*indexNr);
		#endif
		if (_fspacker_ver2_write_indexNr(self->output, (Py_ssize_t)*indexNr) < 0) {
			return -1;
		}
		return 1;
	}
	else {
		self->counter += 1;
		if (PyMemoTable_Set(self->memo, obj, idx) < 0) {
			PyErr_NoMemory();
			return -1;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Indexed to #%ld\n", idx);
		#endif
	}
	return 0;
}
// types
static int _fspacker_packer_ver2_list(packerObject_ver2 *self, PyObject *obj) {
	Py_ssize_t len = PyList_Size(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing list with length: %ld ...\n", len);
	#endif
	if (len > ITEM_LIMIT) {
		PyErr_SetString(self->module->PackingError, "Too big list to pack");
		return -1;
	}
	else if (len == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_LIST, 1);
	}
	if (_fspacker_buffer_append(self->output, &VER2_OP_LIST, 1) < 0) {
		return -1;
	}
	if (_fspacker_ver2_write_vin(self->output, len) < 0) {
		return -1;
	}
	self->stack++;
	PyObject *firstitem = NULL;
	PyObject *item = NULL;
	PyObject *iter = NULL;
	#if defined(FSPACKER_DEBUG)
		Py_ssize_t itemCounter = 0;
	#endif
	iter = PyObject_GetIter(obj);
	if (iter == NULL) {
		PyErr_NoMemory();
		goto error;
	}
	firstitem = PyIter_Next(iter);
	if (firstitem == NULL) {
		if (PyErr_Occurred()) {
			PyErr_SetNone(PyExc_RuntimeError);
			goto error;
		}
		self->stack--;
		return 0;
	}
	item = PyIter_Next(iter);
	if (item == NULL) {
		if (PyErr_Occurred()) {
			PyErr_SetNone(PyExc_RuntimeError);
			goto error;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing list item #0 ...\n");
		#endif
		if (_fspacker_packer_ver2_parser(self, firstitem) < 0) {
			goto error;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing list item #0 done\n");
		#endif
		Py_CLEAR(firstitem);
		self->stack--;
		return 0;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Packing list item #0 ...\n");
	#endif
	if (_fspacker_packer_ver2_parser(self, firstitem) < 0) {
		goto error;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Packing list item #0 done\n");
	#endif
	Py_CLEAR(firstitem);
	while (item) {
		#if defined(FSPACKER_DEBUG)
			itemCounter++;
			printf("Packing list item #%ld ...\n", itemCounter);
		#endif
		if ( _fspacker_packer_ver2_parser(self, item) < 0 ) {
			goto error;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing list item #%ld done\n", itemCounter);
		#endif
		Py_CLEAR(item);
		item = PyIter_Next(iter);
		if (item == NULL) {
			if (PyErr_Occurred()){
				PyErr_SetNone(PyExc_RuntimeError);
				goto error;
			}
			break;
		}
	}
	self->stack--;
	Py_XDECREF(firstitem);
	Py_XDECREF(item);
	Py_XDECREF(iter);
	#if defined(FSPACKER_DEBUG)
		printf("Packing list done\n");
	#endif
	return 0;
	error:
	Py_XDECREF(firstitem);
	Py_XDECREF(item);
	Py_XDECREF(iter);
	return -1;
}
static int _fspacker_packer_ver2_tuple(packerObject_ver2 *self, PyObject *obj) {
	Py_ssize_t len = PyTuple_Size(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing tuple with length: %ld ...\n", len);
	#endif
	if (len > ITEM_LIMIT) {
		PyErr_SetString(self->module->PackingError, "Too big tuple to pack");
		return -1;
	}
	else if (len == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_LIST, 1);
	}
	if (_fspacker_buffer_append(self->output, &VER2_OP_LIST, 1) < 0) {
		return -1;
	}
	if (_fspacker_ver2_write_vin(self->output, len) < 0) {
		return -1;
	}
	self->stack++;
	for (int i = 0; i < len; i++) {
		PyObject *item = PyTuple_GET_ITEM(obj, i);
		if (item == NULL) {
			PyErr_SetNone(PyExc_RuntimeError);
			return -1;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing tuple item #%d ...\n", i);
		#endif
		if ( _fspacker_packer_ver2_parser(self, item) == -1 ) {
			return -1;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing tuple item #%d done\n", i);
		#endif
	}
	self->stack--;
	#if defined(FSPACKER_DEBUG)
		printf("Packing tuple done\n");
	#endif
	return 0;
}
static int _fspacker_packer_ver2_set(packerObject_ver2 *self, PyObject *obj) {
	PyObject *item;
	Py_hash_t hash;
	Py_ssize_t ppos = 0;
	Py_ssize_t len = PySet_GET_SIZE(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing set with length: %ld ...\n", len);
	#endif
	if (len > ITEM_LIMIT) {
		PyErr_SetString(self->module->PackingError, "Too big tuple to pack");
		return -1;
	}
	else if (len == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_SET, 1);
	}
	if (_fspacker_buffer_append(self->output, &VER2_OP_SET, 1) < 0) {
		return -1;
	}
	if (_fspacker_ver2_write_vin(self->output, len) < 0) {
		return -1;
	}
	self->stack++;
	while (_PySet_NextEntry(obj, &ppos, &item, &hash)) {
		#if defined(FSPACKER_DEBUG)
			printf("Packing set item #%ld ...\n", ppos);
		#endif
		if ( _fspacker_packer_ver2_parser(self, item) == -1 ) {
			return -1;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing set item #%ld done\n", ppos);
		#endif
	}
	self->stack--;
	#if defined(FSPACKER_DEBUG)
		printf("Packing set done\n");
	#endif
	return 0;
}
static int _fspacker_packer_ver2_dict(packerObject_ver2 *self, PyObject *obj) {
	PyObject *key = NULL;
	PyObject *value = NULL;
	Py_ssize_t ppos = 0;
	Py_ssize_t len = PyDict_GET_SIZE(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing dict with length: %ld...\n", len);
	#endif
	if (len > ITEM_LIMIT) {
		PyErr_SetString(self->module->PackingError, "Too big dict to pack");
		return -1;
	}
	else if (len == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_DICT, 1);
	}
	if (_fspacker_buffer_append(self->output, &VER2_OP_DICT, 1) < 0) {
		return -1;
	}
	if (_fspacker_ver2_write_vin(self->output, len) < 0) {
		return -1;
	}
	self->stack++;
	while (PyDict_Next(obj, &ppos, &key, &value)) {
		#if defined(FSPACKER_DEBUG)
			printf("Packing dict #%ld key...\n", ppos-1);
		#endif
		if ( _fspacker_packer_ver2_parser(self, key) == -1 ) {
			return -1;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing dict #%ld key done\n", ppos-1);
			printf("Packing dict #%ld value...\n", ppos-1);
		#endif
		if ( _fspacker_packer_ver2_parser(self, value) == -1 ) {
			return -1;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Packing dict #%ld value done\n", ppos-1);
		#endif
	}
	self->stack--;
	#if defined(FSPACKER_DEBUG)
		printf("Packing dict done\n");
	#endif
	return 0;
}
static int _fspacker_packer_ver2_int(packerObject_ver2 *self, PyObject *obj) {
	int sign = _PyLong_Sign(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing int...\n");
	#endif
	if (sign == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_INTERGER, 1);
	}
	int isNeg = sign<0;
	PyObject *absVal = NULL;
	unsigned char *pdata = NULL;
	PyObject *repr = NULL;
	Py_ssize_t nbits = 0;
	Py_ssize_t nbytes = 0;
	switch (_fspacker_packer_ver2_register(self, obj)) {
		case 1:
			goto done;
		case 0:
			break;
		case -1:
			return -1;
	}
	if ( isNeg ) {
		absVal = PyNumber_Absolute(obj);
		if ( absVal == NULL ) {
			goto memoryError;
		}
		nbits = _PyLong_NumBits(absVal);
		nbytes = (nbits >> 3)+1;
		if (nbytes > ITEM_LIMIT) {
			PyErr_SetString(self->module->PackingError, "Too big integer to pack");
			goto error;
		}
		repr = PyBytes_FromStringAndSize(NULL, nbytes);
		if (repr == NULL) {
			goto memoryError;
		}
		pdata = (unsigned char *)PyBytes_AS_STRING(repr);
		Py_DECREF(repr);
		if (_PyLong_AsByteArray((PyLongObject *)(absVal), pdata, nbytes, 1, 0) < 0) {
			goto memoryError;
		}
		Py_DECREF(absVal);
	} else {
		nbits = _PyLong_NumBits(obj);
		nbytes = (nbits >> 3)+1;
		if (nbytes > ITEM_LIMIT) {
			PyErr_SetString(self->module->PackingError, "Too big integer to pack");
			goto error;
		}
		repr = PyBytes_FromStringAndSize(NULL, nbytes);
		if (repr == NULL) {
			goto memoryError;
		}
		pdata = (unsigned char *)PyBytes_AS_STRING(repr);
		Py_DECREF(repr);
		if (_PyLong_AsByteArray((PyLongObject *)(obj), pdata, nbytes, 1, 0) < 0) {
			goto memoryError;
		}
	}
	if ((nbytes*8)-nbits >= 8 ) {
		nbytes -= 1;
	}
	if (nbytes == 1) {
		if (_fspacker_buffer_append(self->output, &(isNeg ? VER2_OP_NEG_CHAR_INTERGER:VER2_OP_CHAR_INTERGER), 1) < 0) {
			goto error;
		}
	}
	else if (nbytes == 2) {
		if (_fspacker_buffer_append(self->output, &(isNeg ? VER2_OP_NEG_SHORT_INTERGER:VER2_OP_SHORT_INTERGER), 1) < 0) {
			goto error;
		}
	}
	else {
		if (_fspacker_buffer_append(self->output, &(isNeg ? VER2_OP_NEG_INTERGER:VER2_OP_INTERGER), 1) < 0) {
			goto error;
		}
		if (_fspacker_ver2_write_vin(self->output, nbytes) < 0) {
			goto error;
		}
	}
	if (_fspacker_buffer_append(self->output, pdata, nbytes) < 0) {
		goto error;
	}
	done:
	#if defined(FSPACKER_DEBUG)
		printf("Packing int done\n");
	#endif
	return 0;
	memoryError:
	PyErr_NoMemory();
	error:
	Py_XDECREF(absVal);
	return -1;
}
static int _fspacker_packer_ver2_float(packerObject_ver2 *self, PyObject *obj) {
	#if defined(FSPACKER_DEBUG)
		printf("Packing float...\n");
	#endif
	double val = PyFloat_AS_DOUBLE((PyFloatObject *)obj);
	if (val == 0.0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_FLOAT, 1);
	}
	if (isinf(val)) {
		if (signbit(val)) {
			return _fspacker_buffer_append(self->output, &VER2_OP_NEG_INF_FLOAT, 1);
		} else {
			return _fspacker_buffer_append(self->output, &VER2_OP_INF_FLOAT, 1);
		}
	}
	switch (_fspacker_packer_ver2_register(self, obj)) {
		case 1:
			goto done;
		case 0:
			break;
		case -1:
			return -1;
	}
	if (_fspacker_buffer_append(self->output, &VER2_OP_FLOAT, 1) < 0) {
		return -1;
	}
	unsigned char dval[8];
	if (_PyFloat_Pack8(val, &dval[0], 1) < 0) {
		return -1;
	}
	if (_fspacker_buffer_append(self->output, &dval[0], 8) < 0) {
		return -1;
	}
	done:
	#if defined(FSPACKER_DEBUG)
		printf("Packing float done\n");
	#endif
	return 0;
}
static int _fspacker_packer_ver2_bytes(packerObject_ver2 *self, PyObject *obj) {
	Py_ssize_t len = PyBytes_GET_SIZE(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing bytes [%zd] with length: %ld ...\n", (size_t)obj, len);
	#endif
	if (len > ITEM_LIMIT) {
		PyErr_SetString(self->module->PackingError, "Too big bytes to pack");
		return -1;
	}
	else if (len == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_BYTES, 1);
	}
	const char *data = NULL;
	switch (_fspacker_packer_ver2_register(self, obj)) {
		case 1:
			goto done;
		case 0:
			break;
		case -1:
			return -1;
	}
	data = PyBytes_AS_STRING(obj);
	if (_fspacker_buffer_append(self->output, &VER2_OP_BYTES, 1) < 0) {
		return -1;
	}
	if (_fspacker_ver2_write_vin(self->output, len) < 0) {
		return -1;
	}
	if (_fspacker_buffer_append(self->output, &data[0], len) < 0) {
		return -1;
	}
	done:
	#if defined(FSPACKER_DEBUG)
		printf("Packing bytes done\n");
	#endif
	return 0;
}
static int _fspacker_packer_ver2_bytearray(packerObject_ver2 *self, PyObject *obj) {
	Py_ssize_t len = PyByteArray_GET_SIZE(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing bytearray with length: %ld ...\n", len);
	#endif
	if (len > ITEM_LIMIT) {
		PyErr_SetString(self->module->PackingError, "Too big bytearray to pack");
		return -1;
	}
	else if (len == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_BYTES, 1);
	}
	const char *data = NULL;
	switch (_fspacker_packer_ver2_register(self, obj)) {
		case 1:
			goto done;
		case 0:
			break;
		case -1:
			return -1;
	}
	data = PyByteArray_AS_STRING(obj);
	if (_fspacker_buffer_append(self->output, &VER2_OP_BYTES, 1) < 0) {
		return -1;
	}
	if (_fspacker_ver2_write_vin(self->output, len) < 0) {
		return -1;
	}
	if (_fspacker_buffer_append(self->output, &data[0], len) < 0) {
		return -1;
	}
	done:
	#if defined(FSPACKER_DEBUG)
		printf("Packing bytearray done\n");
	#endif
	return 0;
}
static int _fspacker_packer_ver2_unicode(packerObject_ver2 *self, PyObject *obj) {
	Py_ssize_t len = PyUnicode_GetLength(obj);
	#if defined(FSPACKER_DEBUG)
		printf("Packing unicode [%zd] with length: %ld ...\n", (size_t)obj, len);
	#endif
	if (len == 0) {
		return _fspacker_buffer_append(self->output, &VER2_OP_ZERO_UNICODE, 1);
	}
	PyObject *escapedStr = NULL;
	Py_ssize_t strLen;
	const char *data;
	switch (_fspacker_packer_ver2_register(self, obj)) {
		case 1:
			goto done;
		case 0:
			break;
		case -1:
			return -1;
	}
	if (_fspacker_buffer_append(self->output, &VER2_OP_UNICODE, 1) < 0) {
		return -1;
	}
	escapedStr = PyUnicode_AsEncodedString(obj, "utf8", "surrogatepass");
	if ( escapedStr == NULL ) {
		PyErr_SetString(self->module->PackingError, "UNICODE encode failed");
		goto error;
	}
	strLen = PyObject_Length(escapedStr);
	data = PyBytes_AS_STRING(escapedStr);
	if ( data == NULL ) {
		goto memoryError;
	}
	if (_fspacker_ver2_write_vin(self->output, strLen) < 0) {
		goto error;
	}
	if (_fspacker_buffer_append(self->output, &data[0], strLen) < 0) {
		goto error;
	}
	done:
	#if defined(FSPACKER_DEBUG)
		printf("Packing unicode done\n");
	#endif
	Py_XDECREF(escapedStr);
	return 0;
	memoryError:
	PyErr_NoMemory();
	error:
	Py_XDECREF(escapedStr);
	return -1;
}
// parser
static int _fspacker_packer_ver2_parser(packerObject_ver2 *self, PyObject *obj) {
	#if defined(FSPACKER_DEBUG)
		printf("Recursive limit: %ld/%ld\n", self->stack, self->recursiveLimit);
	#endif
	if (self->stack == self->recursiveLimit) {
		PyErr_SetString(self->module->PackingError, "Recusive limit reached");
		return -1;
	}
	if (obj == Py_None) {
		#if defined(FSPACKER_DEBUG)
			printf("Packing None...\n");
			int ret = _fspacker_buffer_append(self->output, &VER2_OP_NONE, 1);
			printf("Packing None done\n");
			return ret;
		#else
			return _fspacker_buffer_append(self->output, &VER2_OP_NONE, 1);
		#endif
	}
	else if (obj == Py_False) {
		#if defined(FSPACKER_DEBUG)
			printf("Packing False...\n");
			int ret = _fspacker_buffer_append(self->output, &VER2_OP_BOOL_FALSE, 1);
			printf("Packing False done\n");
			return ret;
		#else
			return _fspacker_buffer_append(self->output, &VER2_OP_BOOL_FALSE, 1);
		#endif
	}
	else if (obj == Py_True) {
		#if defined(FSPACKER_DEBUG)
			printf("Packing True...\n");
			int ret = _fspacker_buffer_append(self->output, &VER2_OP_BOOL_TRUE, 1);
			printf("Packing True done\n");
			return ret;
		#else
			return _fspacker_buffer_append(self->output, &VER2_OP_BOOL_TRUE, 1);
		#endif
	}
	PyTypeObject *type = Py_TYPE(obj);
	if (type == &PyLong_Type) {
		return _fspacker_packer_ver2_int(self, obj);
	}
	else if (type == &PyFloat_Type) {
		return _fspacker_packer_ver2_float(self, obj);
	}
	else if (type == &PyBytes_Type) {
		return _fspacker_packer_ver2_bytes(self, obj);
	}
	else if (type == &PyUnicode_Type) {
		return _fspacker_packer_ver2_unicode(self, obj);
	}
	else if (type == &PySet_Type) {
		return _fspacker_packer_ver2_set(self, obj);
	}
	else if (type == &PyList_Type) {
		return _fspacker_packer_ver2_list(self, obj);
	}
	else if (type == &PyTuple_Type) {
		return _fspacker_packer_ver2_tuple(self, obj);
	}
	else if (type == &PyDict_Type) {
		return _fspacker_packer_ver2_dict(self, obj);
	}
	else if (type == &PyByteArray_Type) {
		return _fspacker_packer_ver2_bytearray(self, obj);
	}
	PyErr_Format(self->module->PackingError, "Packing %.200s type is not supported", type->tp_name);
	return -1;
	
}
PyObject *_fspacker_packer_ver2(PyObject *obj, PyObject *stream, Py_ssize_t recursiveLimit) {
	#if defined(FSPACKER_DEBUG)
		printf("Packing version 2 recursiveLimit: %ld\n", recursiveLimit);
	#endif
	FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
	size_t bufferLength = 64;
	packerObject_ver2 packer;
	packer.memo = NULL;
	bufferObject output;
	PyObject *ret = NULL;
	PyObject *writeMethod = NULL;
	PyObject *methodRet = NULL;
	const char ver = 0x02;
	output.buf = (char*)PyMem_Malloc(bufferLength);
	if (output.buf == NULL) {
		goto memoryError;
	}
	packer.memo = PyMemoTable_New();
	if (packer.memo == NULL) {
		goto memoryError;
	}
	packer.output = &output;
	packer.module = FSPackerModule;
	packer.stream = NULL;
	packer.counter = 0;
	packer.stack = 0;
	packer.recursiveLimit = recursiveLimit;
	output.buf_size = bufferLength;
	output.length = 1;
	//
	memcpy(output.buf, &ver, 1);
	if ( _fspacker_packer_ver2_parser(&packer, obj) < 0 ) {
		goto error;
	}
	ret = PyBytes_FromStringAndSize(output.buf, output.length);
	if (ret == NULL) {
		goto memoryError;
	}
	PyMem_Free(output.buf);
	PyMemoTable_Del(packer.memo);
	packer.memo = NULL;
	if (stream != NULL) {
		_Py_IDENTIFIER(write);
		if (_PyObject_LookupAttrId(stream, &PyId_write, &writeMethod) < 0) {
			PyErr_SetString(packer.module->PackingError, "Stream does not have write method");
			goto error;
		}
		if (writeMethod == NULL) {
			PyErr_SetString(packer.module->PackingError, "Unable to write to the stream");
			goto error;
		}
		methodRet = PyObject_CallFunctionObjArgs(writeMethod, ret, NULL);
		if (PyErr_Occurred() != NULL) {
			goto error;
		}
		if (methodRet == NULL) {
			PyErr_SetString(packer.module->PackingError, "Unable to write to the stream");
			goto error;
		}
		Py_DECREF(methodRet);
		Py_DECREF(writeMethod);
		Py_RETURN_NONE;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Packing done\n");
	#endif
	return ret;
	memoryError:
	PyErr_NoMemory();
	error:
	Py_XDECREF(methodRet);
	Py_XDECREF(writeMethod);
	Py_XDECREF(ret);
	PyMem_Free(output.buf);
	PyMemoTable_Del(packer.memo);
	#if defined(FSPACKER_DEBUG)
		printf("Packing ERROR\n");
	#endif
	return NULL;
}

// ---- UNPACKER -----
struct unpackerObject_ver2 {
	const char *input;
	Py_ssize_t input_pos;
	Py_ssize_t input_length;
	PyObject **memo;
	Py_ssize_t memo_length;
	Py_ssize_t memo_size;
	Py_ssize_t maxIndexSize;
	Py_ssize_t stack;
	Py_ssize_t recursiveLimit;
	FSPackerState *module;
	std::vector<PyObject*> allObject;
};
// abstract
static PyObject* _fspacker_unpacker_ver2_parser(unpackerObject_ver2 *self);
// misc
static Py_ssize_t _fspacker_unpacker_ver2_read_indexNr(unpackerObject_ver2 *self) {
	Py_ssize_t ret;
	if ( self->input_length - self->input_pos < 1 ) {
		goto EOFError;
	}
	if ( (uint8_t)(self->input[self->input_pos]) < VER2_VINT_2BYTES ) {
		ret = (uint8_t)self->input[self->input_pos];
		self->input_pos++;
	} else {
		if ( (uint8_t)(self->input[self->input_pos]) == VER2_VINT_2BYTES ) {
			if ( self->input_length - self->input_pos < 3 ) {
				goto EOFError;
			}
			ret =(uint8_t)(self->input[self->input_pos+1]);
			ret += (uint8_t)(self->input[self->input_pos+2]) << 8;
			self->input_pos += 3;
		}
		else if ( (uint8_t)(self->input[self->input_pos]) == VER2_VINT_3BYTES ) {
			if ( self->input_length - self->input_pos < 4 ) {
				goto EOFError;
			}
			ret = (uint8_t)(self->input[self->input_pos+1]);
			ret += (uint8_t)(self->input[self->input_pos+2]) << 8;
			ret += (uint8_t)(self->input[self->input_pos+3]) << 16;
			self->input_pos += 4;
		}
		else if ( (uint8_t)(self->input[self->input_pos]) == VER2_VINT_4BYTES ) {
			if ( self->input_length - self->input_pos < 5 ) {
				goto EOFError;
			}
			ret = (uint8_t)(self->input[self->input_pos+1]);
			ret += (uint8_t)(self->input[self->input_pos+2]) << 8;
			ret += (uint8_t)(self->input[self->input_pos+3]) << 16;
			ret += (uint8_t)(self->input[self->input_pos+4]) << 24;
			self->input_pos += 5;
		}
		else {
			PyErr_SetString(self->module->UnpackingError, "Invalid integer size");
			return 0;
		}
	}
	#if defined(FSPACKER_DEBUG)
		printf("vIn return: %lu\n", ret);
	#endif
	return ret;
	EOFError:
		PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
		return 0;
}
static Py_ssize_t _fspacker_unpacker_ver2_read_vin(unpackerObject_ver2 *self) {
	Py_ssize_t ret;
	if ( self->input_length - self->input_pos < 1 ) {
		goto EOFError;
	}
	if ( (uint8_t)(self->input[self->input_pos]) < 0xFD ) {
		ret = (uint8_t)self->input[self->input_pos];
		self->input_pos++;
	} else {
		if ( (uint8_t)(self->input[self->input_pos]) == 0xFD ) {
			if ( self->input_length - self->input_pos < 3 ) {
				goto EOFError;
			}
			ret =(uint8_t)(self->input[self->input_pos+1]);
			ret += (uint8_t)(self->input[self->input_pos+2]) << 8;
			self->input_pos += 3;
		}
		else if ( (uint8_t)(self->input[self->input_pos]) == 0xFE ) {
			if ( self->input_length - self->input_pos < 4 ) {
				goto EOFError;
			}
			ret = (uint8_t)(self->input[self->input_pos+1]);
			ret += (uint8_t)(self->input[self->input_pos+2]) << 8;
			ret += (uint8_t)(self->input[self->input_pos+3]) << 16;
			self->input_pos += 4;
		}
		else if ( (uint8_t)(self->input[self->input_pos]) == 0xFF ) {
			if ( self->input_length - self->input_pos < 5 ) {
				goto EOFError;
			}
			ret = (uint8_t)(self->input[self->input_pos+1]);
			ret += (uint8_t)(self->input[self->input_pos+2]) << 8;
			ret += (uint8_t)(self->input[self->input_pos+3]) << 16;
			ret += (uint8_t)(self->input[self->input_pos+4]) << 24;
			self->input_pos += 5;
		}
	}
	#if defined(FSPACKER_DEBUG)
		printf("vIn return: %lu\n", ret);
	#endif
	return ret;
	EOFError:
		PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
		return 0;
}
static int _fspacker_unpacker_ver2_register(unpackerObject_ver2 *self, PyObject *obj) {
	Py_ssize_t l = self->memo_length;
	Py_ssize_t s = self->memo_size;
	#if defined(FSPACKER_DEBUG)
		printf("Registering %zd object to memo: %ld/%ld\n", (size_t)obj, l, s);
	#endif
	if (l == s) {
		if (self->maxIndexSize > 0 && self->maxIndexSize == self->memo_length) {
			PyErr_SetString(self->module->UnpackingError, "Max index size reached");
			return -1;
		}
		s += ((s >> 3) + 8);
		#if defined(FSPACKER_DEBUG)
			printf("Resizing %zd memo from %ld to %ld size\n", (size_t)self->memo, self->memo_size, s);
		#endif
		if (self->memo_size >= s) {
			PyErr_SetNone(PyExc_OverflowError);
			return -1;
		}
		PyMem_RESIZE(self->memo, PyObject *, s);
		#if defined(FSPACKER_DEBUG)
			printf("New memo: %zd \n", (size_t)self->memo);
		#endif
		if (self->memo == NULL) {
			PyErr_NoMemory();
			return -1;
		}
	}
	self->memo[l] = obj;
	#if defined(FSPACKER_DEBUG)
		printf("Indexed to #%ld\n", l);
	#endif
	l += 1;
	self->memo_length = l;
	self->memo_size = s;
	return 0;
}
// types
static PyObject* _fspacker_unpacker_ver2_tuple(unpackerObject_ver2 *self) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking tuple...\n");
	#endif
	PyObject *ret = NULL;
	PyObject *value = NULL;
	Py_ssize_t vLen = _fspacker_unpacker_ver2_read_vin(self);
	Py_ssize_t i;
	if ( vLen == 0 ) {
		goto EOFError;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Tuple length: %ld\n", vLen);
	#endif
	ret = PyTuple_New(vLen);
	self->stack++;
	for ( i=0 ; i<vLen ; i++ ) {
		#if defined(FSPACKER_DEBUG)
			printf("Unpacking tuple item #%ld\n", i);
		#endif
		value = _fspacker_unpacker_ver2_parser(self);
		if ( value == NULL ) {
			goto error;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Tuple item #%ld unpacked\n", i);
		#endif
		Py_INCREF(value);
		PyTuple_SET_ITEM(ret, i, value);
		value = NULL;
	}
	self->stack--;
	#if defined(FSPACKER_DEBUG)
		printf("Tuple unpacked\n");
	#endif
	return ret;
	EOFError:
	PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	error:
	Py_XDECREF(ret);
	return NULL;
}
static PyObject* _fspacker_unpacker_ver2_set(unpackerObject_ver2 *self) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking set...\n");
	#endif
	PyObject *ret = NULL;
	PyObject *value = NULL;
	Py_ssize_t vLen = _fspacker_unpacker_ver2_read_vin(self);
	Py_ssize_t i;
	if ( vLen == 0 ) {
		goto EOFError;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Set length: %ld\n", vLen);
	#endif
	ret = PySet_New(NULL);
	self->stack++;
	for ( i=0 ; i<vLen ; i++ ) {
		#if defined(FSPACKER_DEBUG)
			printf("Unpacking set #%ld ...\n", i);
		#endif
		value = _fspacker_unpacker_ver2_parser(self);
		if ( value == NULL ) {
			goto error;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Set item #%ld unpacked\n", i);
		#endif
		if ( PySet_Add(ret, value) < 0 ) {
			goto memoryError;
		}
		value = NULL;
	}
	self->stack--;
	#if defined(FSPACKER_DEBUG)
		printf("Set unpacked\n");
	#endif
	return ret;
	memoryError:
	PyErr_NoMemory();
	if (0) {
		EOFError:
		PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	}
	error:
	Py_XDECREF(ret);
	return NULL;
}
static PyObject* _fspacker_unpacker_ver2_dict(unpackerObject_ver2 *self) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking dict...\n");
	#endif
	PyObject *ret = NULL;
	PyObject *key = NULL;
	PyObject *value = NULL;
	Py_ssize_t vLen = _fspacker_unpacker_ver2_read_vin(self);
	Py_ssize_t i;
	if ( vLen == 0 ) {
		goto EOFError;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Dict length: %ld\n", vLen);
	#endif
	ret = PyDict_New();
	self->stack++;
	for ( i=0 ; i<vLen ; i++ ) {
		#if defined(FSPACKER_DEBUG)
			printf("Unpacking dict #%ld key...\n", i);
		#endif
		key = _fspacker_unpacker_ver2_parser(self);
		if ( key == NULL ) {
			goto error;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Dict #%ld key unpacked\n", i);
			printf("Unpacking dict #%ld value...\n", i);
		#endif
		value = _fspacker_unpacker_ver2_parser(self);
		if ( value == NULL ) {
			goto error;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Dict #%ld value unpacked\n", i);
		#endif
		if ( PyDict_SetItem(ret, key, value) < 0 ) {
			PyErr_SetNone(PyExc_RuntimeError);
			goto error;
		}
		key = NULL;
		value = NULL;
	}
	self->stack--;
	#if defined(FSPACKER_DEBUG)
		printf("Dict unpacked\n");
	#endif
	return ret;
	EOFError:
	PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	error:
	Py_XDECREF(ret);
	return NULL;
}
static PyObject* _fspacker_unpacker_ver2_int(unpackerObject_ver2 *self, bool isNeg, Py_ssize_t vLen) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking int [vLen %ld]...\n", vLen);
	#endif
	PyObject *tmp = NULL;
	PyObject *ret = NULL;
	if (vLen == 0) {
		vLen = _fspacker_unpacker_ver2_read_vin(self);
	}
	if ( vLen == 0 ) {
		goto EOFError;
	}
	if (self->input_pos+vLen > self->input_length) {
		goto EOFError;
	}
	ret = _PyLong_FromByteArray((unsigned char*)&self->input[self->input_pos], vLen, 1, 0);
	if ( ret == NULL ) {
		goto memoryError;
	}
	self->input_pos += vLen;
	if (isNeg) {
		tmp = PyNumber_Negative(ret);
		Py_DECREF(ret);
		ret = tmp;
		if ( ret == NULL ) {
			goto memoryError;
		}
	}
	if (_fspacker_unpacker_ver2_register(self, ret) < 0) {
		goto error;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Int unpacked\n");
	#endif
	return ret;
	memoryError:
	PyErr_NoMemory();
	if (0) {
		EOFError:
		PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	}
	error:
	Py_XDECREF(ret);
	return NULL;
}
static PyObject* _fspacker_unpacker_ver2_float(unpackerObject_ver2 *self) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking float...\n");
	#endif
	PyObject *ret = NULL;
	double val;
	if ((self->input_pos+(Py_ssize_t)sizeof(double)) > self->input_length) {
		goto EOFError;
	}
	val = _PyFloat_Unpack8((const unsigned char*)&self->input[self->input_pos], 1);
	ret = PyFloat_FromDouble(val);
	if (ret == NULL) {
		goto memoryError;
	}
	self->input_pos += sizeof(double);
	if (_fspacker_unpacker_ver2_register(self, ret) < 0) {
		goto error;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Float unpacked\n");
	#endif
	return ret;
	memoryError:
	PyErr_NoMemory();
	if (0) {
		EOFError:
		PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	}
	error:
	Py_XDECREF(ret);
	return NULL;
}
static PyObject* _fspacker_unpacker_ver2_bytes(unpackerObject_ver2 *self) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking bytes...\n");
	#endif
	PyObject *ret = NULL;
	Py_ssize_t vLen = _fspacker_unpacker_ver2_read_vin(self);
	if ( vLen == 0 ) {
		goto EOFError;
	}
	if (self->input_pos+vLen > self->input_length) {
		goto EOFError;
	}
	ret = PyBytes_FromStringAndSize(&self->input[self->input_pos], vLen);
	self->input_pos += vLen;
	if (_fspacker_unpacker_ver2_register(self, ret) < 0) {
		goto error;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Bytes unpacked\n");
	#endif
	return ret;
	EOFError:
	PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	error:
	Py_XDECREF(ret);
	return NULL;
}
static PyObject* _fspacker_unpacker_ver2_unicode(unpackerObject_ver2 *self) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking unicode..\n");
	#endif
	PyObject *ret = NULL;
	Py_ssize_t vLen = _fspacker_unpacker_ver2_read_vin(self);
	if ( vLen == 0 ) {
		goto EOFError;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Unicode length: %ld\n", vLen);
	#endif
	if (self->input_pos+vLen > self->input_length) {
		goto EOFError;
	}
	ret = PyUnicode_DecodeUTF8(&self->input[self->input_pos], vLen, "surrogatepass");
	if (ret == NULL) {
		return NULL;
	}
	self->input_pos += vLen;
	if (_fspacker_unpacker_ver2_register(self, ret) < 0) {
		goto error;
	}
	#if defined(FSPACKER_DEBUG)
		printf("Unicode unpacked\n");
	#endif
	return ret;
	EOFError:
	PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	error:
	Py_XDECREF(ret);
	return NULL;
}
// parser
static PyObject* _fspacker_unpacker_ver2_parser(unpackerObject_ver2 *self) {
	#if defined(FSPACKER_DEBUG)
		printf("Parsing.. buffer: %ld/%ld\n", self->input_pos, self->input_length);
	#endif
	if (self->stack == self->recursiveLimit) {
		PyErr_SetString(self->module->UnpackingError, "Recusive limit reached");
		return NULL;
	}
	Py_ssize_t indexPos;
	uint8_t op;
	PyObject *ret = NULL;
	if ( self->input_pos >= self->input_length ) {
		goto EOFError;
	}
	op = self->input[self->input_pos];
	if (op >= VER2_OP_NONE) {
		self->input_pos++;
		#if defined(FSPACKER_DEBUG)
			printf("Readed OP code: %u buffer: %ld/%ld\n", op, self->input_pos, self->input_length);
		#endif
		switch (op) {
			case VER2_OP_NONE:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking None...\n");
				#endif
				ret = Py_None;
				Py_INCREF(ret);
				#if defined(FSPACKER_DEBUG)
					printf("None unpacked\n");
				#endif
				break;
			case VER2_OP_BOOL_FALSE:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking False...\n");
				#endif
				ret = Py_False;
				Py_INCREF(ret);
				#if defined(FSPACKER_DEBUG)
					printf("False unpacked\n");
				#endif
				break;
			case VER2_OP_BOOL_TRUE:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking True...\n");
				#endif
				ret = Py_True;
				Py_INCREF(ret);
				#if defined(FSPACKER_DEBUG)
					printf("True unpacked\n");
				#endif
				break;
			case VER2_OP_ZERO_INTERGER:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking zero integer...\n");
				#endif
				ret = PyLong_FromSsize_t(0);
				#if defined(FSPACKER_DEBUG)
					printf("Zero integer unpacked\n");
				#endif
				break;
			case VER2_OP_INTERGER:
				ret = _fspacker_unpacker_ver2_int(self, false, 0);
				break;
			case VER2_OP_NEG_INTERGER:
				ret = _fspacker_unpacker_ver2_int(self, true, 0);
				break;
			case VER2_OP_CHAR_INTERGER:
				ret = _fspacker_unpacker_ver2_int(self, false, 1);
				break;
			case VER2_OP_NEG_CHAR_INTERGER:
				ret = _fspacker_unpacker_ver2_int(self, true, 1);
				break;
			case VER2_OP_SHORT_INTERGER:
				ret = _fspacker_unpacker_ver2_int(self, false, 2);
				break;
			case VER2_OP_NEG_SHORT_INTERGER:
				ret = _fspacker_unpacker_ver2_int(self, true, 2);
				break;
			case VER2_OP_FLOAT:
				ret = _fspacker_unpacker_ver2_float(self);
				break;
			case VER2_OP_ZERO_FLOAT:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking zero float...\n");
				#endif
				ret = PyFloat_FromDouble((double)0);
				#if defined(FSPACKER_DEBUG)
					printf("Zero float unpacked\n");
				#endif
				break;
			case VER2_OP_INF_FLOAT:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking infinity float...\n");
				#endif
				ret = PyFloat_FromDouble(Py_HUGE_VAL);
				#if defined(FSPACKER_DEBUG)
					printf("Infinity float unpacked\n");
				#endif
				break;
			case VER2_OP_NEG_INF_FLOAT:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking negative infinity float...\n");
				#endif
				ret = PyFloat_FromDouble(-Py_HUGE_VAL);
				#if defined(FSPACKER_DEBUG)
					printf("Negative infinity float unpacked\n");
				#endif
				break;
			case VER2_OP_UNICODE:
				ret = _fspacker_unpacker_ver2_unicode(self);
				break;
			case VER2_OP_ZERO_UNICODE:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking zero unicode...\n");
				#endif
				ret = PyUnicode_New(0, (Py_UCS1)0);
				#if defined(FSPACKER_DEBUG)
					printf("Zero unicode unpacked\n");
				#endif
				break;
			case VER2_OP_BYTES:
				ret = _fspacker_unpacker_ver2_bytes(self);
				break;
			case VER2_OP_ZERO_BYTES:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking zero bytes...\n");
				#endif
				ret = PyBytes_FromStringAndSize(NULL, 0);
				#if defined(FSPACKER_DEBUG)
					printf("Zero unicode unpacked\n");
				#endif
				break;
			case VER2_OP_LIST:
				ret = _fspacker_unpacker_ver2_tuple(self);
				break;
			case VER2_OP_ZERO_LIST:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking zero list...\n");
				#endif
				ret = PyTuple_New(0);
				#if defined(FSPACKER_DEBUG)
					printf("Zero list unpacked\n");
				#endif
				break;
			case VER2_OP_DICT:
				ret = _fspacker_unpacker_ver2_dict(self);
				break;
			case VER2_OP_ZERO_DICT:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking zero dict...\n");
				#endif
				ret = PyDict_New();
				#if defined(FSPACKER_DEBUG)
					printf("Zero dict unpacked\n");
				#endif
				break;
			case VER2_OP_SET:
				ret = _fspacker_unpacker_ver2_set(self);
				break;
			case VER2_OP_ZERO_SET:
				#if defined(FSPACKER_DEBUG)
					printf("Unpacking zero set...\n");
				#endif
				ret = PySet_New(NULL);
				#if defined(FSPACKER_DEBUG)
					printf("Zero set unpacked\n");
				#endif
				break;
			default:
				PyErr_Format(self->module->UnpackingError, "Unknown OP code: %u", op);
		}
	}
	else {
		if ( op == 0x00 ) {
			indexPos = 0;
			self->input_pos++;
		}
		else {
			indexPos = _fspacker_unpacker_ver2_read_indexNr(self);
			if ( indexPos == 0 ) {
				return NULL;
			}
		}
		if (self->memo_length == 0 || indexPos >= self->memo_length) {
			PyErr_Format(self->module->UnpackingError, "Index slot %u missing", indexPos);
			return NULL;
		}
		#if defined(FSPACKER_DEBUG)
			printf("Receiving index: #%ld\n", indexPos);
		#endif
		ret = self->memo[indexPos];
		Py_INCREF(ret);
	}
	#if defined(FSPACKER_DEBUG)
		printf("Parsing processed [%ld]\n", (Py_ssize_t)ret);
	#endif
	if ( ret != NULL ) {
		self->allObject.push_back(ret);
	}
	return ret;
	EOFError:
	PyErr_SetString(self->module->UnpackingError, "End of buffer/Not enough data");
	return NULL;
}
PyObject* _fspacker_unpacker_ver2(const char *input, Py_ssize_t len, Py_ssize_t maxIndexSize, Py_ssize_t recursiveLimit) {
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking version 2 maxIndexSize: %ld recursiveLimit: %ld\n", maxIndexSize, recursiveLimit);
	#endif
	FSPackerState *FSPackerModule = _fspacker_GetGlobalState();
	PyObject *ret = NULL;
	unpackerObject_ver2 unpacker;
	unpacker.input = input;
	unpacker.input_pos = 1;
	unpacker.input_length = len;
	unpacker.memo_size = 16;
	unpacker.memo = PyMem_New(PyObject *, 16);
	if (unpacker.memo == NULL) {
		PyErr_NoMemory();
		return NULL;
	}
	unpacker.stack = 0;
	unpacker.memo_length = 0;
	unpacker.maxIndexSize = maxIndexSize;
	unpacker.recursiveLimit = recursiveLimit;
	unpacker.module = FSPackerModule;
	ret = _fspacker_unpacker_ver2_parser(&unpacker);
	if (ret == NULL) {
		goto error;
	}
	PyMem_Free(unpacker.memo);
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking done\n");
	#endif
	return ret;
	error:
	for ( PyObject* obj : unpacker.allObject ) {
		Py_XDECREF(obj);
	}
	PyMem_Free(unpacker.memo);
	#if defined(FSPACKER_DEBUG)
		printf("Unpacking ERROR\n");
	#endif
	return NULL;
}
