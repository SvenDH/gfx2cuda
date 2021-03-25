# Gfx2Cuda - Graphics to CUDA interoperability

_Gfx2Cuda_ is a python implementation of cuda's graphics interopability methods for DirectX, OpenGL, etc.
The main usage is for quick transfer of images rendered with for example Godot or Unity to Cuda memory buffers such as pytoch tensors, without needing to transfer the image to cpu and back to gpu.

### Example

**Render to texture and copy to pytorch tensor**

```python
import gfx2cuda
import pytorch

tensor = torch.zeros([480, 640, 4], device=0).byte().contiguous()

instance = gfx2cuda.create()
tex = instance.create_texture(640, 480)

# Now render to the texture

with tex as ptr:
    tex.copy_to(tensor.data_ptr())

print(tensor.data)
# pytorch tensor should now contain your rendered data
```
