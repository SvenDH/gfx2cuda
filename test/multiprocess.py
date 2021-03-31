from multiprocessing import Process

import gfx2cuda
import numpy as np
import torch


shape = [4, 4, 4]


def f(handle):
    tex = gfx2cuda.open_ipc_texture(handle)

    print(tex)

    tensor1 = torch.ones(shape).byte().contiguous().cuda()

    with tex as ptr:
        tex.copy_from(tensor1.data_ptr())

    tensor2 = torch.zeros(shape).byte().contiguous().cuda()

    with tex as ptr:
        tex.copy_to(tensor2.data_ptr())

    print(tensor2.data)

    torch.cuda.synchronize()
    gfx2cuda.synchronize()


if __name__ == "__main__":
    tensor = torch.zeros(shape).byte().contiguous().cuda()

    tex = gfx2cuda.texture(tensor)

    gfx2cuda.synchronize()

    p = Process(target=f, args=(tex.ipc_handle,))

    p.start()
    p.join()

    with tex as ptr:
        tex.copy_to(tensor.data_ptr())

    print(tensor.data)
