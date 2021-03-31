import gfx2cuda
import torch
import numpy as np

if __name__ == "__main__":
    shape = [2, 2, 4]
    tensor1 = torch.ones(shape).byte().contiguous().cuda()
    tensor2 = torch.zeros(shape).byte().contiguous().cuda()

    #tex = gfx2cuda.texture(tensor1.shape, dtype=tensor1.dtype)

    #with tex as ptr:
    #    tex.copy_from(tensor1.data_ptr())

    tex = gfx2cuda.texture(tensor1)

    with tex as ptr:
        tex.copy_to(tensor2.data_ptr())

    print(tensor2.data)

    assert np.array_equal(tensor2.cpu().numpy(), tensor1.cpu().numpy())
