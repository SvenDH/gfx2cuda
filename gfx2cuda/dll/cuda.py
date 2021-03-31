import os
from ctypes import *
import glob

CUDA_PATH = os.getenv('CUDA_PATH')
if sizeof(c_void_p) == 8:
    _cu_re = '/bin/cudart64_*'
else:  # == 4
    _cu_re = '/bin/cudart32_*'

cu_path = glob.glob(CUDA_PATH + _cu_re)[0]
cu = cdll.LoadLibrary(cu_path)


def cuda_device_d3d_adapter(adapter):
    dev = c_int()
    ret = cu.cudaD3D11GetDevice(byref(dev), cast(adapter, c_void_p))
    assert ret == 0, ret
    return dev.value


def cuda_map_resource(resource):
    ret = cu.cudaGraphicsMapResources(1, byref(resource), 0)
    assert ret == 0, ret


def cuda_unmap_resource(resource):
    ret = cu.cudaGraphicsUnmapResources(1, byref(resource), 0)
    assert ret == 0, ret


def cuda_unregister_resource(resource):
    ret = cu.cudaGraphicsUnregisterResource(resource)
    assert ret == 0, ret


def cuda_memcpy2d_atod(dst, src, width_in_bytes, height):
    ret = cu.cudaMemcpy2DFromArray(c_void_p(dst), width_in_bytes, c_void_p(src), 0, 0, width_in_bytes, height, 3)
    assert ret == 0, ret


def cuda_memcpy2d_dtoa(dst, src, width_in_bytes, height):
    ret = cu.cudaMemcpy2DToArray(c_void_p(dst), 0, 0, c_void_p(src), width_in_bytes, width_in_bytes, height, 3)
    assert ret == 0, ret


def cuda_get_mapped_array(resource):
    array = c_void_p()
    ret = cu.cudaGraphicsSubResourceGetMappedArray(byref(array), resource, 0, 0)
    assert ret == 0, ret
    return array.value


def cuda_register_d3d_resource(d3d_resource):
    resource = c_void_p()
    ret = cu.cudaGraphicsD3D11RegisterResource(byref(resource), cast(d3d_resource, c_void_p), 0)
    assert ret == 0, ret
    ret = cu.cudaGraphicsResourceSetMapFlags(resource, 1)
    assert ret == 0, ret
    return resource
