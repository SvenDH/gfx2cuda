import sys

from gfx2cuda.gfx2cuda import *
from gfx2cuda.backends import Texture
from gfx2cuda.format import TextureFormat
from gfx2cuda.exception import Gfx2CudaError

_instance = None


def _default_backend():
    if sys.platform == 'win32':
        return Backends.D3D11
    else:
        return Backends.OPENGL


def _lazy_init(backend=None, **kwargs):
    global _instance
    if _instance is None:
        _instance = Gfx2Cuda(backend=backend or _default_backend())
    if backend is not None and backend is not _instance.get_backend():
        raise Gfx2CudaError("Backend does not match initialized backend")


def texture(*args, **kwargs):
    _lazy_init(**kwargs)
    fmt = None
    needs_copy = None
    if len(args) == 1:
        if isinstance(args[0], list) or isinstance(args[0], tuple):
            dims = args[0]
        elif isinstance(args[0], int):
            return _instance.lookup_shared_handle(args[0])
        else:
            dims = args[0].shape
            needs_copy = args[0]
            if hasattr(needs_copy, '__cuda_array_interface__'):
                dtype = needs_copy.__cuda_array_interface__['typestr']
                fmt = TextureFormat.from_channels_and_dtype(dims[2], dtype)
            else:
                fmt = TextureFormat.from_channels_and_dtype(dims[2], args[0].dtype)

    elif len(args) == 2:
        if isinstance(args[0], list) or isinstance(args[0], tuple):
            dims = args[0]
            fmt = args[1]
        else:
            fmt = kwargs.get('format', TextureFormat.R32FLOAT)
            dims = args + (fmt.channels,)
    elif len(args) == 3:
        dims = args
    else:
        raise ValueError("Too many arguments")

    device = kwargs.get('device', 0)
    if fmt is None:
        dtype = kwargs.get('dtype', 'float')
        normalized = kwargs.get('normalized', False)
        fmt = TextureFormat.from_channels_and_dtype(dims[2], dtype, normalized)
    tex = _instance.create_texture(dims[1], dims[0], fmt, device=device)
    if needs_copy is not None:
        with tex:
            if hasattr(needs_copy, '__cuda_array_interface__'):
                ptr = needs_copy.__cuda_array_interface__['data'][0]
            else:
                # Just try something here
                ptr = needs_copy.data_ptr()
            tex.copy_from(ptr)

    return tex


def open_ipc_texture(handle, **kwargs):
    _lazy_init(**kwargs)
    tex = _instance.lookup_shared_handle(handle)
    if tex is None:
        tex = _instance.open_ipc_handle(handle)
    return tex


def synchronize(**kwargs):
    _lazy_init(**kwargs)
    _instance.device.synchronize()
