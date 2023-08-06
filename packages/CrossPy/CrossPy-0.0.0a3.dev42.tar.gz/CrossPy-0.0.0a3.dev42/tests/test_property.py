import numpy as np
from crosspy import cupy as cp
import crosspy as xp

def test_tobuffer():
    components = []
    components.append(cp.arange(3))
    components.append(np.arange(2))

    a = xp.array(components, axis=0)
    with cp.cuda.Device(1):
        buf = cp.empty(5, dtype=np.int64)
    a.tobuffer(buf)
    print("buf", buf)

if __name__ == '__main__':
    test_tobuffer()