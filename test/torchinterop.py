import gfx2cuda
import torch

if __name__ == "__main__":
    tensor = torch.zeros([480, 640, 4], device=0).byte().contiguous()

    instance = gfx2cuda.create()
    tex = instance.create_texture(640, 480)

    with tex as ptr:
        tex.copy_to(tensor.data_ptr())

    print(tensor.data)
