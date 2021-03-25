import collections
from gfx2cuda.backends import Devices, Device


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            print(f"Only 1 instance of {cls.__name__} is allowed per process! Returning the existing instance...")
        return cls._instances[cls]


class Gfx2Cuda(metaclass=Singleton):
    def __init__(self, backend=Devices.D3D11, buffer_size=60):
        self.backend = backend
        self.devices = []
        self.detect_devices()
        self.device = self.devices[0] if len(self.devices) > 0 else None
        self.device.init_context()
        self.buffer_size = buffer_size
        self.buffer = collections.deque(list(), self.buffer_size)

    def detect_devices(self):
        self._reset_devices()
        self.devices = Device.discover_devices(self.backend)

    def _reset_devices(self):
        self.devices = []

    def create_shared_texture(self, width, height):
        if self.device is not None:
            return self.device.create_texture(width, height)
        return None
