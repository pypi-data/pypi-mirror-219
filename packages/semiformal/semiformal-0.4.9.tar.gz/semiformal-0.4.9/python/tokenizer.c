#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "scanner.h"


static PyObject *py_tokens(PyObject *self, PyObject *args, PyObject *kwargs) {
    char *text;
    if (!PyArg_ParseTuple(args, "s:text", &text)) {
        return NULL;
    }

    token_array *tokens = tokenize(text);

    if (tokens == NULL) {
        return NULL;
    }

    size_t num_tokens = tokens->n;
    PyObject *result = PyTuple_New(num_tokens);
    if (!result) {
        goto error_free_tokens;
    }

    PyObject *tuple;

    token_t token;
    for (size_t i = 0; i < num_tokens; i++) {
        token = tokens->a[i];
        tuple = Py_BuildValue("III", token.offset, token.len, token.type);
        if (PyTuple_SetItem(result, i, tuple) < 0) {
            goto error_free_tokens;
        }
    }

    token_array_destroy(tokens);

    return result;

error_free_tokens:
    token_array_destroy(tokens);
error_return_null:
    return NULL;
}



static PyObject *py_tokenize(PyObject *self, PyObject *args, PyObject *kwargs) {
    char *text;
    if (!PyArg_ParseTuple(args, "s:text", &text)) {
        return NULL;
    }

    token_array *tokens = tokenize(text);

    if (tokens == NULL) {
        return NULL;
    }

    size_t num_tokens = tokens->n;
    PyObject *result = PyTuple_New(num_tokens);
    if (!result) {
        goto error_free_tokens;
    }

    PyObject *tuple;

    token_t token;
    for (size_t i = 0; i < num_tokens; i++) {
        token = tokens->a[i];
        tuple = Py_BuildValue("s#I", text + token.offset, token.len, token.type);
        if (PyTuple_SetItem(result, i, tuple) < 0) {
            goto error_free_tokens;
        }
    }

    token_array_destroy(tokens);

    return result;

error_free_tokens:
    token_array_destroy(tokens);
error_return_null:
    return NULL;
}


static PyMethodDef tokenizer_methods[] = {
    {"tokens", (PyCFunction)py_tokens, METH_VARARGS | METH_KEYWORDS, "tokens(text)"},
    {"tokenize", (PyCFunction)py_tokenize, METH_VARARGS | METH_KEYWORDS, "tokenize(text)"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef tokenizer_module = {
    PyModuleDef_HEAD_INIT,
    "_tokenizer",
    NULL,
    -1,
    tokenizer_methods
};

PyMODINIT_FUNC PyInit__tokenizer(void) {
    return PyModule_Create(&tokenizer_module);
}

