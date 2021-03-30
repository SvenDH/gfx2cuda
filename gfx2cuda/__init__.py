from gfx2cuda.gfx2cuda import *

_instance = None


def _lazy_init(backend=None):
    global _instance
    if _instance is None:
        _instance = Gfx2Cuda(backend=backend or Backends.D3D11)
    if backend is not _instance.get_backend():
        raise Gfx2CudaError("Backend does not match initialized backend")


def texture(width, height, fmt=TexureFormat.RGBA8UNORM, backend=None):
    _lazy_init(backend)
    tex = _instance.create_texture(width, height, fmt)
    return tex
