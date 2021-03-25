from gfx2cuda.gfx2cuda import Gfx2Cuda


def create(buffer_size=60):
    if not isinstance(buffer_size, int) or buffer_size < 1:
        raise AttributeError(f"'buffer_size' should be an int greater than 0")
    return Gfx2Cuda(buffer_size=buffer_size)
