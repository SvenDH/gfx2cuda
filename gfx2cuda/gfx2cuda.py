from gfx2cuda.backends import Backends, Device, TexureFormat, Texture


class Gfx2CudaError(BaseException):
    pass


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
        self.shared_handle_map = dict()

    def get_backend(self):
        return self.backend

    def detect_devices(self):
        self._reset_devices()
        self.devices = Device.discover_devices(self.backend)

    def _reset_devices(self):
        self.devices = []

    def create_texture(self, width, height, fmt):
        if self.device is not None:
            tex = self.device.create_texture(width, height, fmt)
            self.shared_handle_map[tex.shared_handle] = tex
            return tex
        return None

    def lookup_shared_handle(self, handle):
        if handle in self.shared_handle_map:
            return self.shared_handle_map[handle]
        return None
