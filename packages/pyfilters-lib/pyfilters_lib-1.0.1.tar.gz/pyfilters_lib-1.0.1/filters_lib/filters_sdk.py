import ctypes
import math
import pathlib
import platform
import sys

from typing import List

import filter_types

_libname = None
if sys.platform == "win32":
    arc = platform.architecture()
    if arc[0].__contains__("64"):
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "windows-x64" / "filters.dll"
    else:
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "windows-x86" / "filters.dll"
elif sys.platform.startswith("linux"):
    print('Add linux lib')
elif sys.platform == "darwin":
    print('Add macos lib')
else:
    raise FileNotFoundError("This platform (%s) is currently not supported by pyfilters-sdk." % sys.platform)

_filters_lib = ctypes.WinDLL(str(_libname))

error_type = ctypes.POINTER(ctypes.c_uint8)


class _FilterParam(ctypes.Structure):
    _fields_ = [('type', ctypes.c_uint8), ('samplingFreq', ctypes.c_int), ('cutoffFreq', ctypes.c_double)]


_get_preinstalled_filter_count = _filters_lib.get_preinstalled_filter_count
_get_preinstalled_filter_count.restype = None
_get_preinstalled_filter_count.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_uint8))

_get_preinstalled_filter_list = _filters_lib.get_preinstalled_filter_list
_get_preinstalled_filter_list.restype = None
_get_preinstalled_filter_list.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8))


def preinstalled_filters_list() -> List[filter_types.FilterParam]:
    _count_preinstalled = -1
    has_error = error_type(ctypes.c_uint8(0))
    _count_preinstalled_cint = ctypes.c_int(_count_preinstalled)
    _get_preinstalled_filter_count(ctypes.byref(_count_preinstalled_cint), has_error)
    raise_exception_if(has_error)

    _filters = (_FilterParam * _count_preinstalled_cint.value)()
    _get_preinstalled_filter_list(_filters, has_error)
    raise_exception_if(has_error)

    return [filter_types.FilterParam(current_filter.type, current_filter.samplingFreq, current_filter.cutoffFreq) for
            current_filter in _filters]


class Filter:
    def __init__(self):
        tfilter = ctypes.POINTER(ctypes.c_void_p)

        self._native_ptr = None

        self._create_tfilter_by_param = _filters_lib.create_TFilter_by_param
        self._create_tfilter_by_param.restype = ctypes.POINTER(tfilter)
        self._create_tfilter_by_param.argtypes = (_FilterParam, ctypes.POINTER(ctypes.c_uint8))

        self._create_custom_tfilter = _filters_lib.create_custom_TFilter
        self._create_custom_tfilter.restype = ctypes.POINTER(tfilter)
        self._create_custom_tfilter.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8))

        self._reset = _filters_lib.TFilter_Reset
        self._reset.restype = None
        self._reset.argtypes = (ctypes.POINTER(tfilter), ctypes.POINTER(ctypes.c_uint8))

        self._clear_params = _filters_lib.TFilter_ClearParams
        self._clear_params.restype = None
        self._clear_params.argtypes = (ctypes.POINTER(tfilter), ctypes.POINTER(ctypes.c_uint8))

        self._set_params = _filters_lib.TFilter_SetParams
        self._set_params.restype = None
        self._set_params.argtypes = (ctypes.POINTER(tfilter), ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint8))

        self._filter = _filters_lib.TFilter_Filter
        self._filter.restype = ctypes.c_double
        self._filter.argtypes = (ctypes.POINTER(tfilter), ctypes.c_double, ctypes.POINTER(ctypes.c_uint8))

        self._filter_array = _filters_lib.TFilter_Filter_array
        self._filter_array.restype = None
        self._filter_array.argtypes = (ctypes.POINTER(tfilter), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_uint8))

        self._get_id_filter = _filters_lib.getID_TFilter
        self._get_id_filter.restype = ctypes.c_int
        self._get_id_filter.argtypes = (ctypes.POINTER(tfilter), ctypes.POINTER(ctypes.c_uint8))

        self._delete_tfilter = _filters_lib.delete_TFilter
        self._delete_tfilter.restype = None
        self._delete_tfilter.argtypes = (ctypes.POINTER(tfilter), ctypes.POINTER(ctypes.c_uint8))

    def init_by_param(self, filter_params: filter_types.FilterParam):
        if self._native_ptr is not None:
            return

        has_error = error_type(ctypes.c_uint8(0))
        self._native_ptr = self._create_tfilter_by_param(_FilterParam(filter_params.type.value,
                                                                      filter_params.sampling_freq,
                                                                      filter_params.cutoff_freq),
                                                         has_error)
        raise_exception_if(has_error)

    def init_by_str(self, filter_str: str):
        if self._native_ptr is not None:
            return

        has_error = error_type(ctypes.c_uint8(0))
        self._native_ptr = self._create_custom_tfilter(filter_str, has_error)
        raise_exception_if(has_error)

    def get_native_ptr(self):
        return self._native_ptr

    def reset(self):
        if self._native_ptr is None:
            return

        has_error = error_type(ctypes.c_uint8(0))
        self._reset(self._native_ptr, has_error)
        raise_exception_if(has_error)

    def clear_params(self):
        if self._native_ptr is None:
            return

        has_error = error_type(ctypes.c_uint8(0))
        self._clear_params(self._native_ptr, has_error)
        raise_exception_if(has_error)

    def set_params(self, params: str):
        if self._native_ptr is None:
            return

        has_error = error_type(ctypes.c_uint8(0))
        self._set_params(self._native_ptr, params, has_error)
        raise_exception_if(has_error)

    def filter(self, value: float) -> float:
        if self._native_ptr is None:
            return math.nan

        has_error = error_type(ctypes.c_uint8(0))
        res = self._filter(self._native_ptr, value, has_error)
        raise_exception_if(has_error)
        return res

    def filter_array(self, values: List[float]) -> List[float]:
        if self._native_ptr is None:
            return []

        native_array = (ctypes.c_double * len(values))(*values)

        has_error = error_type(ctypes.c_uint8(0))
        self._filter_array(self._native_ptr, native_array, len(values), has_error)
        raise_exception_if(has_error)

        return [x for x in native_array]

    def get_id_filter(self) -> int:
        if self._native_ptr is None:
            return -1

        has_error = error_type(ctypes.c_uint8(0))
        res = self._get_id_filter(self._native_ptr, has_error)
        raise_exception_if(has_error)
        return res

    def __del__(self):
        if self._native_ptr is not None:
            has_error = error_type(ctypes.c_uint8(0))
            self._delete_tfilter(self._native_ptr, has_error)
            raise_exception_if(has_error)
            self._native_ptr = None


class FilterList:
    def __init__(self):
        tfilter_list = ctypes.POINTER(ctypes.c_void_p)
        tfilter = ctypes.POINTER(ctypes.c_void_p)

        self._native_ptr = None

        self._create_tfilter_list = _filters_lib.create_TFilterList
        self._create_tfilter_list.restype = ctypes.POINTER(tfilter_list)
        self._create_tfilter_list.argtypes = ()

        self._add_filter = _filters_lib.TFilterList_AddFilter
        self._add_filter.restype = None
        self._add_filter.argtypes = (
        ctypes.POINTER(tfilter_list), ctypes.POINTER(tfilter), ctypes.POINTER(ctypes.c_uint8))

        self._filter = _filters_lib.TFilterList_Filter
        self._filter.restype = ctypes.c_double
        self._filter.argtypes = (ctypes.POINTER(tfilter_list), ctypes.c_double, ctypes.POINTER(ctypes.c_uint8))

        self._filter_array = _filters_lib.TFilterList_Filter_array
        self._filter_array.restype = None
        self._filter_array.argtypes = (
        ctypes.POINTER(tfilter_list), ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint8))

        self._clear_filters = _filters_lib.TFilter_List_ClearFilters
        self._clear_filters.restype = None
        self._clear_filters.argtypes = (ctypes.POINTER(tfilter_list), ctypes.POINTER(ctypes.c_uint8))

        self._reset = _filters_lib.TFilterList_Reset
        self._reset.restype = None
        self._reset.argtypes = (ctypes.POINTER(tfilter_list), ctypes.POINTER(ctypes.c_uint8))

        self._delete_tfilter = _filters_lib.TFilterList_Delete_TFilter
        self._delete_tfilter.restype = None
        self._delete_tfilter.argtypes = (ctypes.POINTER(tfilter_list), ctypes.c_int, ctypes.POINTER(ctypes.c_uint8))

        self._delete_tfilter_list = _filters_lib.delete_TFilterList
        self._delete_tfilter_list.restype = None
        self._delete_tfilter_list.argtypes = (ctypes.POINTER(tfilter_list), ctypes.POINTER(ctypes.c_uint8))

        self._native_ptr = self._create_tfilter_list()

    def add_filter(self, filter_to_add: Filter):
        has_error = error_type(ctypes.c_uint8(0))
        self._add_filter(self._native_ptr, filter_to_add.get_native_ptr(), has_error)
        raise_exception_if(has_error)

    def filter(self, value: float) -> float:
        has_error = error_type(ctypes.c_uint8(0))
        res = self._filter(self._native_ptr, value, has_error)
        raise_exception_if(has_error)
        return res

    def filter_array(self, values: List[float]) -> List[float]:
        native_array = (ctypes.c_double * len(values))(*values)
        has_error = error_type(ctypes.c_uint8(0))
        self._filter_array(self._native_ptr, native_array, len(values), has_error)

        raise_exception_if(has_error)
        return [x for x in native_array]

    def clear_filters(self):
        has_error = error_type(ctypes.c_uint8(0))
        self._clear_filters(self._native_ptr, has_error)
        raise_exception_if(has_error)

    def reset(self):
        has_error = error_type(ctypes.c_uint8(0))
        self._reset(self._native_ptr, has_error)
        raise_exception_if(has_error)

    def delete_filter(self, filter_id: int):
        has_error = error_type(ctypes.c_uint8(0))
        self._delete_tfilter(self._native_ptr, filter_id, has_error)
        raise_exception_if(has_error)

    def __del__(self):
        if self._native_ptr is not None:
            has_error = error_type(ctypes.c_uint8(0))
            self._delete_tfilter_list(self._native_ptr, has_error)
            raise_exception_if(has_error)

            self._native_ptr = None


def raise_exception_if(status):
    if status.contents.value == 1:
        raise Exception('Something went wrong!')
