from gfx2cuda.gfx2cuda import *

instance = None


def texture(width, height, fmt=TexureFormat.RGBA8UNORM, backend=None):
    global instance
    if instance is None:
        instance = Gfx2Cuda(backend=backend or Backends.D3D11)

    tex = instance.create_texture(width, height, fmt)
    return tex
