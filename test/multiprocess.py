from multiprocessing import Process, Queue

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


if __name__ == "__main__":
    tensor = torch.zeros(shape).byte().contiguous().cuda()

    tex = gfx2cuda.texture(tensor)

    p = Process(target=f, args=(tex.ipc_handle,))

    p.start()
    p.join()

    with tex as ptr:
        tex.copy_to(tensor.data_ptr())

    print(tensor.data)

    assert np.array_equal(tensor.cpu().numpy(), np.ones(shape, dtype=np.uint8))
