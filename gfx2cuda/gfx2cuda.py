from gfx2cuda.backends import Backends, Device
from gfx2cuda.exception import Gfx2CudaError


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            print(f"Only 1 instance of {cls.__name__} is allowed per process! Returning the existing instance...")
        return cls._instances[cls]


class Gfx2Cuda(metaclass=Singleton):
    def __init__(self, backend=Backends.D3D11):
        self.backend = backend
        self.devices = []
        self.detect_devices()
        self.device = self.devices[0] if len(self.devices) > 0 else None
        self.device.init_context()
        self._ipc_handle_map = dict()

    def get_backend(self):
        return self.backend

    def detect_devices(self):
        self._reset_devices()
        self.devices = Device.discover_devices(self.backend)

    def _reset_devices(self):
        self.devices = []

    def create_texture(self, width, height, format, device=None):
        if device >= len(self.devices):
            raise Gfx2CudaError("Out of bound CUDA device")
        if self.device is not None and device is None:
            tex = self.device.create_texture(width, height, format)
        else:
            if self.devices[device].has_cuda():
                assert device == self.devices[device].dev
                tex = self.devices[device].create_texture(width, height, format)
            else:
                raise Gfx2CudaError("Device has no CUDA capabilities.")
        self._ipc_handle_map[tex.ipc_handle] = tex
        return tex

    def lookup_ipc_handle(self, handle):
        if handle in self._ipc_handle_map:
            return self._ipc_handle_map[handle]
        return None

    def open_ipc_handle(self, handle):
        tex = self.device.open_ipc_handle(handle)
        self._ipc_handle_map[handle] = tex
        return tex
