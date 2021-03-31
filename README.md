# Gfx2Cuda - Graphics to CUDA interoperability

_Gfx2Cuda_ is a python implementation of CUDA's graphics interopability methods for DirectX, OpenGL, etc.
The main usage is for quick transfer of images rendered with for example Godot or Unity to CUDA memory buffers such as 
pytoch tensors, without needing to transfer the image to cpu and back to gpu.

For now only DirectX 11 is supported. This can be useful for implementing CUDA ipc (interprocess-communication) for 
Windows, since that functionality is not available in vanilla CUDA for Windows. 
You would use a DirectX texture as buffer that can be seen by multiple processes without having to download any gpu data
to cpu and back.

### Example

**Render to texture and copy to pytorch tensor**

```python
import gfx2cuda
import torch

# Shape: [height, width, channels]
shape = [480, 640, 4]
tensor1 = torch.ones(shape).contiguous().cuda()
tensor2 = torch.zeros(shape).contiguous().cuda()

# Create copy of a tensor but as a texture
tex = gfx2cuda.texture(tensor1)

with tex as ptr:
    tex.copy_to(tensor2.data_ptr())

print(tensor2.data)
# pytorch tensor should now contain a copy of the texture data
```

**Share texture between process, write on one process and see results in the other**

```python
from multiprocessing import Process

import gfx2cuda
import torch

shape = [4, 4, 4]

def f(handle):
    tex = gfx2cuda.open_ipc_texture(handle)
    # Received and opened the texture
    print(tex)
    # >> Texture with format TextureFormat.RGBA32FLOAT (4 x 4)
    tensor1 = torch.ones(shape).contiguous().cuda()
    with tex:
        tex.copy_from(tensor1.data_ptr())

    tensor2 = torch.zeros(shape).contiguous().cuda()
    with tex:
        tex.copy_to(tensor2.data_ptr())

    print(tensor2.data)
    # See all ones

if __name__ == "__main__":
    tensor = torch.zeros(shape).contiguous().cuda()
    # Initialize as all zeros
    tex = gfx2cuda.texture(tensor)

    p = Process(target=f, args=(tex.ipc_handle,))
    p.start()
    p.join()

    with tex:
        tex.copy_to(tensor.data_ptr())

    print(tensor.data)
    # See all ones
```
