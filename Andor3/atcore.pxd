from libc.stddef cimport wchar_t

cdef extern from 'atcore.h':
    cdef enum:
        AT_HANDLE_UNINITIALISED
        AT_HANDLE_SYSTEM

    
    int AT_InitialiseLibrary()
    int AT_FinaliseLibrary()

    int AT_Open(int CameraIndex, int *Hndl)
    int AT_OpenDevice(const wchar_t* Device, int *Hndl)
    int AT_Close(int Hndl)

    ctypedef int (*FeatureCallback)(int Hndl, const wchar_t* Feature, void* Context)
    int AT_RegisterFeatureCallback(int Hndl, const wchar_t* Feature, FeatureCallback EvCallback, void* Context)
    int AT_UnregisterFeatureCallback(int Hndl, const wchar_t* Feature, FeatureCallback EvCallback, void* Context)

    int AT_IsImplemented(int Hndl, const wchar_t* Feature, int* Implemented)
    int AT_IsReadable(int Hndl, const wchar_t* Feature, int* Readable)
    int AT_IsWritable(int Hndl, const wchar_t* Feature, int* Writable)
    int AT_IsReadOnly(int Hndl, const wchar_t* Feature, int* ReadOnly)

    int AT_SetInt(int Hndl, const wchar_t* Feature, long long Value)
    int AT_GetInt(int Hndl, const wchar_t* Feature, long long* Value)
    int AT_GetIntMax(int Hndl, const wchar_t* Feature, long long* MaxValue)
    int AT_GetIntMin(int Hndl, const wchar_t* Feature, long long* MinValue)

    int AT_SetFloat(int Hndl, const wchar_t* Feature, double Value)
    int AT_GetFloat(int Hndl, const wchar_t* Feature, double* Value)
    int AT_GetFloatMax(int Hndl, const wchar_t* Feature, double* MaxValue)
    int AT_GetFloatMin(int Hndl, const wchar_t* Feature, double* MinValue)

    int AT_SetBool(int Hndl, const wchar_t* Feature, int Value)
    int AT_GetBool(int Hndl, const wchar_t* Feature, int* Value)

    int AT_SetEnumerated(int Hndl, const wchar_t* Feature, int Value)
    int AT_SetEnumeratedString(int Hndl, const wchar_t* Feature, const wchar_t* String)
    int AT_GetEnumerated(int Hndl, const wchar_t* Feature, int* Value)
    int AT_GetEnumeratedCount(int Hndl,const  wchar_t* Feature, int* Count)
    int AT_IsEnumeratedIndexAvailable(int Hndl, const wchar_t* Feature, int Index, int* Available)
    int AT_IsEnumeratedIndexImplemented(int Hndl, const wchar_t* Feature, int Index, int* Implemented)
    int AT_GetEnumeratedString(int Hndl, const wchar_t* Feature, int Index, wchar_t* String, int StringLength)

    int AT_SetEnumIndex(int Hndl, const wchar_t* Feature, int Value)
    int AT_SetEnumString(int Hndl, const wchar_t* Feature, const wchar_t* String)
    int AT_GetEnumIndex(int Hndl, const wchar_t* Feature, int* Value)
    int AT_GetEnumCount(int Hndl,const  wchar_t* Feature, int* Count)
    int AT_IsEnumIndexAvailable(int Hndl, const wchar_t* Feature, int Index, int* Available)
    int AT_IsEnumIndexImplemented(int Hndl, const wchar_t* Feature, int Index, int* Implemented)
    int AT_GetEnumStringByIndex(int Hndl, const wchar_t* Feature, int Index, wchar_t* String, int StringLength)

    int AT_Command(int Hndl, const wchar_t* Feature)

    int AT_SetString(int Hndl, const wchar_t* Feature, const wchar_t* String)
    int AT_GetString(int Hndl, const wchar_t* Feature, wchar_t* String, int StringLength)
    int AT_GetStringMaxLength(int Hndl, const wchar_t* Feature, int* MaxStringLength)

    int AT_QueueBuffer(int Hndl, unsigned char* Ptr, int PtrSize)
    int AT_WaitBuffer(int Hndl, unsigned char** Ptr, int* PtrSize, unsigned int Timeout)
    int AT_Flush(int Hndl)