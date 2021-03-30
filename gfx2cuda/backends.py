import enum
from abc import ABCMeta, abstractmethod

import gfx2cuda
from gfx2cuda import Gfx2CudaError
import gfx2cuda.dll.dxgi
import gfx2cuda.dll.d3d
import gfx2cuda.dll.cuda


class TexureFormat(enum.Enum):
    RGBA8UNORM = 0
    RGBA16FLOAT = 1
    RGBA32FLOAT = 2

    def get_pixel_size(self):
        if self == TexureFormat.RGBA8UNORM:
            return 4
        elif self == TexureFormat.RGBA16FLOAT:
            return 8
        elif self == TexureFormat.RGBA32FLOAT:
            return 16

    def get_dxgi_format(self):
        if self == TexureFormat.RGBA8UNORM:
            return 28  # DXGI_FORMAT_R8G8B8A8_UNORM
        elif self == TexureFormat.RGBA16FLOAT:
            return 10  # DXGI_FORMAT_R16G16B16A16_FLOAT
        elif self == TexureFormat.RGBA32FLOAT:
            return 2  # DXGI_FORMAT_R32G32B32A32_FLOAT


class Texture:
    def __init__(self, width, height, fmt, device):
        self.width = width
        self.height = height
        self.device = device
        self.format = fmt
        self.nbytes = width * height * fmt.get_pixel_size()
        self.ptr = None
        self._shared_handle = None

    @classmethod
    def from_handle(cls, handle):
        return gfx2cuda.Gfx2Cuda().lookup_shared_handle(handle)

    @property
    def shared_handle(self):
        if self._shared_handle is None:
            self._shared_handle = self.create_shared_handle()
        return self._shared_handle

    @abstractmethod
    def create_shared_handle(self):
        pass

    @abstractmethod
    def register(self):
        pass

    def __str__(self):
        return str(self.ptr)

    def __enter__(self):
        self.map()
        return self.data_ptr()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unmap()

    def map(self):
        gfx2cuda.dll.cuda.cuda_map_resource(self.ptr)

    def unmap(self):
        gfx2cuda.dll.cuda.cuda_unmap_resource(self.ptr)

    def unregister(self):
        gfx2cuda.dll.cuda.cuda_unregister_resource(self.ptr)

    def data_ptr(self):
        return gfx2cuda.dll.cuda.cuda_get_mapped_array(self.ptr)

    def copy_to(self, dst):
        wbytes = self.nbytes // self.height
        gfx2cuda.dll.cuda.cuda_memcpy2d_atod(dst, self.data_ptr(), wbytes, self.height)

    def __del__(self):
        self.unregister()


class D3D11Texture(Texture):
    def __init__(self, width, height, fmt, device):
        super().__init__(width, height, fmt, device)
        dxgi_fmt = fmt.get_dxgi_format()
        self.tex = gfx2cuda.dll.d3d.d3d11_create_texture_2d(width, height, device.handle, dxgi_fmt)

    def create_shared_handle(self):
        dxgi_ptr = gfx2cuda.dll.dxgi.get_dxgi_resource(self.tex)
        handle = gfx2cuda.dll.dxgi.get_shared_handle(dxgi_ptr)
        return handle.value

    def register(self):
        self.ptr = gfx2cuda.dll.cuda.cuda_register_d3d_resource(self.tex)


class OpenGLTexture(Texture):
    def __init__(self, width, height, fmt, device):
        super().__init__(width, height, fmt, device)

    def create_shared_handle(self):
        raise NotImplementedError

    def register(self):
        raise NotImplementedError


class Backends(enum.Enum):
    D3D11 = 0
    OPENGL = 1


class Device(metaclass=ABCMeta):
    def __init__(self, name=None, adapter=None, backend=None):
        self.name = name or "Unknown Adapter"
        self.backend = backend
        self.adapter = adapter
        self.handle = None
        self.dev = -1

    def create_texture(self, width, height, fmt):
        if self.backend == Backends.D3D11:
            tex = D3D11Texture(width, height, fmt, self)
        elif self.backend == Backends.OPENGL:
            tex = OpenGLTexture(width, height, fmt, self)
        else:
            raise Gfx2CudaError("The specified backend is invalid!")
        tex.register()
        return tex

    @abstractmethod
    def init_context(self):
        pass

    @classmethod
    def discover_devices(cls, backend):
        if backend == Backends.D3D11:
            return D3D11Device.discover_devices()
        elif backend == Backends.OPENGL:
            return OpenGLDevice.discover_devices()
        else:
            raise Gfx2CudaError("The specified backend is invalid!")


class D3D11Device(Device):
    def __init__(self, name=None, adapter=None, backend=None):
        super().__init__(name, adapter, backend)
        self.handle, self.context = gfx2cuda.dll.d3d.d3d_initialize_device(adapter)

    def init_context(self):
        self.dev = gfx2cuda.dll.cuda.cuda_device_d3d_adapter(self.adapter)

    @classmethod
    def discover_devices(cls):
        dxgi_factory = gfx2cuda.dll.dxgi.new_dxgi_factory()
        dxgi_adapters = gfx2cuda.dll.dxgi.get_dxgi_adapters(dxgi_factory)

        devices = []
        for dxgi_adapter in dxgi_adapters:
            dxgi_adapter_desc = gfx2cuda.dll.dxgi.dxgi_adapter_description(dxgi_adapter)
            devices += [cls(name=dxgi_adapter_desc, adapter=dxgi_adapter, backend=Backends.D3D11)]

        return devices


class OpenGLDevice(Device):
    def __init__(self, name=None, adapter=None):
        super().__init__(name, adapter)

    def init_context(self):
        raise NotImplementedError

    @classmethod
    def discover_devices(cls):
        raise NotImplementedError
