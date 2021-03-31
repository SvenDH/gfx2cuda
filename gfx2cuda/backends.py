import enum
from abc import ABCMeta, abstractmethod

import gfx2cuda
import gfx2cuda.dll.dxgi
import gfx2cuda.dll.d3d
import gfx2cuda.dll.cuda
from gfx2cuda.format import TextureFormat
from gfx2cuda.exception import Gfx2CudaError


class Texture:
    def __init__(self, width, height, format, device, cpu_access=False, ptr=None):
        self.width = width
        self.height = height
        self.device = device
        self.format = format
        self.cpu_access = cpu_access
        self.nbytes = width * height * format.get_pixel_size()
        self._ptr = None
        self._ipc_handle = None
        self._tex = ptr

    @property
    def ipc_handle(self):
        if self._ipc_handle is None:
            self._ipc_handle = self.create_ipc_handle()
        return self._ipc_handle

    @classmethod
    @abstractmethod
    def create_from_ptr(cls, ptr, device):
        pass

    @abstractmethod
    def create_ipc_handle(self):
        pass

    @abstractmethod
    def register(self):
        pass

    def __str__(self):
        return f"Texture with format {self.format} ({self.width} x {self.height})"

    def __enter__(self):
        self.map()
        return self.data_ptr()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unmap()

    def map(self):
        gfx2cuda.dll.cuda.cuda_map_resource(self._ptr)

    def unmap(self):
        gfx2cuda.dll.cuda.cuda_unmap_resource(self._ptr)

    def unregister(self):
        gfx2cuda.dll.cuda.cuda_unregister_resource(self._ptr)

    def data_ptr(self):
        return gfx2cuda.dll.cuda.cuda_get_mapped_array(self._ptr)

    def copy_to(self, dst):
        wbytes = self.nbytes // self.height
        gfx2cuda.dll.cuda.cuda_memcpy2d_atod(dst, self.data_ptr(), wbytes, self.height)

    def copy_from(self, src):
        wbytes = self.nbytes // self.height
        gfx2cuda.dll.cuda.cuda_memcpy2d_dtoa(self.data_ptr(), src, wbytes, self.height)

    def __del__(self):
        self.unregister()


class D3D11Texture(Texture):
    def __init__(self, width, height, format, device, cpu_access=False, ptr=None):
        super().__init__(width, height, format, device, cpu_access, ptr)
        if self._tex is None:
            dxgi_fmt = format.get_dxgi_format()
            self._tex = gfx2cuda.dll.d3d.d3d11_create_texture_2d(width, height, device.handle, dxgi_fmt, cpu_access)

    @classmethod
    def create_from_ptr(cls, ptr, device):
        width, height, dxgi_fmt = gfx2cuda.dll.d3d.d3d11_texture_desc(ptr)
        fmt = TextureFormat.from_dxgi_format(dxgi_fmt)
        return cls(width, height, fmt, device, ptr=ptr)

    def create_ipc_handle(self):
        dxgi_ptr = gfx2cuda.dll.dxgi.get_dxgi_resource(self._tex)
        handle = gfx2cuda.dll.dxgi.get_shared_handle(dxgi_ptr)
        gfx2cuda.dll.dxgi.dxgi_resource_release(dxgi_ptr)
        return handle.value

    def register(self):
        self._ptr = gfx2cuda.dll.cuda.cuda_register_d3d_resource(self._tex)


class OpenGLTexture(Texture):
    def __init__(self, width, height, format, device, cpu_access=False, ptr=None):
        super().__init__(width, height, format, device, cpu_access, ptr)
        if self._tex is None:
            raise NotImplementedError

    @classmethod
    def create_from_ptr(cls, ptr, device):
        raise NotImplementedError

    def create_ipc_handle(self):
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

    def create_texture(self, width, height, format):
        if self.backend == Backends.D3D11:
            tex = D3D11Texture(width, height, format, self)
        elif self.backend == Backends.OPENGL:
            tex = OpenGLTexture(width, height, format, self)
        else:
            raise Gfx2CudaError("The specified backend is invalid!")
        tex.register()
        return tex

    @abstractmethod
    def init_context(self):
        pass

    @abstractmethod
    def synchronize(self):
        pass

    @abstractmethod
    def open_ipc_handle(self, handle):
        pass

    def has_cuda(self):
        if self.dev == -1:
            try:
                self.init_context()
            except:
                return False
        return self.dev != -1

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

    def synchronize(self):
        gfx2cuda.dll.d3d.d3d11_flush(self.context)

    def open_ipc_handle(self, handle):
        ptr = gfx2cuda.dll.d3d.d3d11_open_shared_handle(handle, self.handle)
        tex = D3D11Texture.create_from_ptr(ptr, self)
        tex.register()
        return tex

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
    def __init__(self, name=None, adapter=None, backend=None):
        super().__init__(name, adapter, backend)

    def init_context(self):
        raise NotImplementedError

    def synchronize(self):
        raise NotImplementedError

    def open_ipc_handle(self, handle):
        raise NotImplementedError

    @classmethod
    def discover_devices(cls):
        raise NotImplementedError
