import enum
import numpy as np

from gfx2cuda.exception import Gfx2CudaFormatError


class TextureFormat(enum.Enum):
    R8UNORM = (1, 1, True)
    R8UINT = (1, 1, False)
    R16UNORM = (2, 1, True)
    R16UINT = (2, 1, False)
    R32UINT = (4, 1, False)
    R32FLOAT = (4, 1, False)

    RG8UNORM = (1, 2, True)
    RG8UINT = (1, 2, False)
    RG16FLOAT = (2, 2, False)
    RG16UNORM = (2, 2, True)
    RG16UINT = (2, 2, False)
    RG32FLOAT = (4, 2, False)
    RG32UINT = (4, 2, False)

    RGB32FLOAT = (4, 3, False)
    RGB32UINT = (4, 3, False)

    RGBA8UNORM = (1, 4, True)
    RGBA8UINT = (1, 4, False)
    RGBA16FLOAT = (2, 4, False)
    RGBA16UNORM = (2, 4, True)
    RGBA16UINT = (2, 4, False)
    RGBA32FLOAT = (4, 4, False)
    RGBA32UINT = (4, 4, False)

    @staticmethod
    def from_channels_and_dtype(channels, dtype, normalized=False):
        try:
            dtype = np.dtype(dtype)
        except TypeError:
            # try to remove prefix (eg. torch.uint32, or tf.uint32)
            name = str(dtype).split('.')
            dtype = np.dtype(name[1])

        if normalized:
            if channels == 1:
                if dtype == np.uint8:
                    return TextureFormat.R8UNORM
                elif dtype == np.uint16:
                    return TextureFormat.R8UNORM
            if channels == 2:
                if dtype == np.uint8:
                    return TextureFormat.RG8UNORM
                elif dtype == np.uint16:
                    return TextureFormat.RG16UNORM
            elif channels == 4:
                if dtype == np.uint8:
                    return TextureFormat.RGBA8UNORM
                elif dtype == np.uint16:
                    return TextureFormat.RGBA16UNORM
        else:
            if channels == 1:
                if dtype == np.uint8:
                    return TextureFormat.R8UINT
                elif dtype == np.uint16:
                    return TextureFormat.R16UINT
                elif dtype == np.float32:
                    return TextureFormat.R32FLOAT
                elif dtype == np.uint32:
                    return TextureFormat.R32UINT
            if channels == 2:
                if dtype == np.float16:
                    return TextureFormat.RG16FLOAT
                elif dtype == np.uint16:
                    return TextureFormat.RG16UINT
                elif dtype == np.float32:
                    return TextureFormat.RG32FLOAT
                elif dtype == np.uint32:
                    return TextureFormat.RG32UINT
            elif channels == 3:
                if dtype == np.float32:
                    return TextureFormat.RGB32FLOAT
                elif dtype == np.uint32:
                    return TextureFormat.RGB32UINT
            elif channels == 4:
                if dtype == np.uint8:
                    return TextureFormat.RGBA8UINT
                elif dtype == np.float16:
                    return TextureFormat.RGBA16FLOAT
                elif dtype == np.uint16:
                    return TextureFormat.RGBA16UINT
                elif dtype == np.float32:
                    return TextureFormat.RGBA32FLOAT
                elif dtype == np.uint32:
                    return TextureFormat.RGBA32UINT
        raise Gfx2CudaFormatError(f"Unsupported texture format for {channels} channels and {dtype}")

    @property
    def size(self):
        return self.value[0]

    @property
    def channels(self):
        return self.value[1]

    @property
    def normalized(self):
        return self.value[2]

    def get_pixel_size(self):
        return self.channels * self.size

    def get_dxgi_format(self):
        if self in _dxgi_format_map:
            return _dxgi_format_map[self]
        raise Gfx2CudaFormatError(f"Unsupported texture format {self}")

    @classmethod
    def from_dxgi_format(cls, format):
        return _dxgi_forma_inv[format]



_dxgi_format_map = {
    TextureFormat.R8UNORM: 61,      # DXGI_FORMAT_R8_UNORM
    TextureFormat.R8UINT: 62,       # DXGI_FORMAT_R8_UINT
    TextureFormat.R16UNORM: 56,     # DXGI_FORMAT_R16_UNORM
    TextureFormat.R16UINT: 57,      # DXGI_FORMAT_R16_UINT
    TextureFormat.R32FLOAT: 41,     # DXGI_FORMAT_R32_FLOAT
    TextureFormat.R32UINT: 42,      # DXGI_FORMAT_R32_UINT
    TextureFormat.RG8UNORM: 49,     # DXGI_FORMAT_R8G8_UNORM
    TextureFormat.RG8UINT: 50,      # DXGI_FORMAT_R8G8_UINT
    TextureFormat.RG16FLOAT: 34,    # DXGI_FORMAT_R16G16_FLOAT
    TextureFormat.RG16UNORM: 35,    # DXGI_FORMAT_R16G16_UNORM
    TextureFormat.RG16UINT: 36,     # DXGI_FORMAT_R16G16_UINT
    TextureFormat.RG32FLOAT: 16,    # DXGI_FORMAT_R32G32_FLOAT
    TextureFormat.RG32UINT: 17,     # DXGI_FORMAT_R32G32_UINT
    TextureFormat.RGB32FLOAT: 6,    # DXGI_FORMAT_R32G32B32_FLOAT
    TextureFormat.RGB32UINT: 7,     # DXGI_FORMAT_R32G32B32_UINT
    TextureFormat.RGBA8UNORM: 28,   # DXGI_FORMAT_R8G8B8A8_UNORM
    TextureFormat.RGBA8UINT: 30,    # DXGI_FORMAT_R8G8B8A8_UINT
    TextureFormat.RGBA16FLOAT: 10,  # DXGI_FORMAT_R16G16B16A16_FLOAT
    TextureFormat.RGBA16UNORM: 11,  # DXGI_FORMAT_R16G16B16A16_UNORM
    TextureFormat.RGBA16UINT: 12,   # DXGI_FORMAT_R16G16B16A16_UINT
    TextureFormat.RGBA32FLOAT: 2,   # DXGI_FORMAT_R32G32B32A32_FLOAT
    TextureFormat.RGBA32UINT: 3     # DXGI_FORMAT_R32G32B32A32_UINT
}

_dxgi_forma_inv = {v: k for k, v in _dxgi_format_map.items()}
