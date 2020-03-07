import matplotlib.pyplot as plt
import numpy as np

def render(voxels):
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    n = len(voxels)
    facecolors = np.ndarray((n, n, n, 3))
    filled = np.ndarray((n, n, n), dtype='b')
    for i, a in enumerate(voxels):
        for j, b in enumerate(a):
            for k, c in enumerate(b):
                if c:
                    filled[i][j][j] = True
                    for l in range(3):
                        facecolors[i][j][k][l] = c[l] / 255.
                else:
                    filled[i][j][k] = False
    ax.voxels(filled, facecolors=facecolors)
    fig.show()
    plt.show()
