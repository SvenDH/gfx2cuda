import gfx2cuda
import torch

if __name__ == "__main__":
    tensor = torch.zeros([480, 640, 4], device=0).byte().contiguous()

    tex = gfx2cuda.texture(640, 480)

    with tex as ptr:
        tex.copy_to(tensor.data_ptr())

    print(tensor.data)

    print(tex.shared_handle)

    print(gfx2cuda.Texture.from_handle(tex.shared_handle))
