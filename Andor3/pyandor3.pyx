import os
import sys
import warnings
cimport cython
cimport atcore as at
import numpy as np
cimport numpy as np
from copy import deepcopy
from libc.stdlib cimport malloc, free
from libc.stddef cimport wchar_t
from cpython.mem cimport PyMem_Free
from .errorcodes import AndorError

np.import_array()

cdef extern from "Python.h":
    wchar_t* PyUnicode_AsWideCharString(object, Py_ssize_t *)
    object PyUnicode_FromWideChar(const wchar_t *w, Py_ssize_t size)

__all__ = ['AT_InitialiseLibrary',
'AT_FinaliseLibrary',
'AT_Open',
'AT_OpenDevice',
'AT_Close',
'AT_GetInt',
'AT_GetString',
'AT_GetBool'
]

def chkerr(code):
    if code == 0:
        # print(ERROR_CODE[0])
        pass
    else:
        raise AndorError(code)

def AT_InitialiseLibrary():
    chkerr(at.AT_InitialiseLibrary())

def AT_FinaliseLibrary():
    chkerr(at.AT_FinaliseLibrary())

def AT_Open(idx):
    cdef int handle
    chkerr(at.AT_Open(idx, &handle))
    return handle

def AT_OpenDevice(dev, idx):
    cdef Py_ssize_t length
    cdef wchar_t *chars = PyUnicode_AsWideCharString(f"Library:{dev}, Index:{idx}", &length)
    cdef int handle
    chkerr(at.AT_OpenDevice(chars, &handle))
    PyMem_Free(chars)
    return handle

def AT_Close(handle):
    chkerr(at.AT_Close(handle))

def AT_GetInt(handle, feature):
    cdef Py_ssize_t length
    cdef wchar_t *chars = PyUnicode_AsWideCharString(feature, &length)
    cdef long long value
    chkerr(at.AT_GetInt(handle, chars, &value))
    PyMem_Free(chars)
    return value

def AT_GetString(handle, feature):
    cdef Py_ssize_t length
    cdef wchar_t *chars = PyUnicode_AsWideCharString(feature, &length)
    cdef wchar_t value[64]
    chkerr(at.AT_GetString(handle, chars, value, 64))
    PyMem_Free(chars)
    return PyUnicode_FromWideChar(value, -1)

def AT_GetBool(handle, feature):
    cdef Py_ssize_t length
    cdef wchar_t *chars = PyUnicode_AsWideCharString(feature, &length)
    cdef int value
    chkerr(at.AT_GetBool(handle, chars, &value))
    PyMem_Free(chars)
    return bool(value)

def test():
    cdef int i = 0
    at.AT_InitialiseLibrary()
    cdef long long iNumberDevices = 0
    cdef Py_ssize_t length
    cdef wchar_t *chars = PyUnicode_AsWideCharString("Device Count", &length)
    i = at.AT_GetInt(1, chars, &iNumberDevices)
    PyMem_Free(chars)
    print(f"error code {i}")
    print(f"found {iNumberDevices} cameras")
    at.AT_FinaliseLibrary()