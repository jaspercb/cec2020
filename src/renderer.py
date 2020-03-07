from matplotlib import pyplot as plt, animation as animation
import numpy as np

class Renderer(object):
  def __init__(self):
      self.fig = plt.figure(figsize=[8, 8])
      widths = [1, 3, 1]
      heights = [1, 1, 1]
      spec = self.fig.add_gridspec(ncols=3, nrows=3, width_ratios=[1, 3, 1],
                                height_ratios=[1, 1, 1])
      self.axs = [self.fig.add_subplot(spec[0, 0], projection='3d'),
                  self.fig.add_subplot(spec[0:, 1], projection='3d')]
      self.fig.tight_layout()

  def animate(self, frames):
      animation.FuncAnimation(self.fig, self.render, frames, blit=True, interval=20, repeat=False)
      plt.show()

  def singleFrame(self, frame):
      self.render(frame)
      plt.show()

  def render(self, voxels):
      filled = np.empty_like(voxels, dtype='b')
      facecolors = np.ndarray(filled.shape + (3,))

      for i, a in enumerate(voxels):
          for j, b in enumerate(a):
              for k, c in enumerate(b):
                  if c:
                      filled[i][j][k] = True
                      for l in range(3):
                          facecolors[i][j][k][l] = c[l] / 256.
                  else:
                      facecolors[i][j][k] = [0,0,0]
                      filled[i][j][k] = False
      for ax in self.axs:
        ax.cla()
        ax.voxels(filled, facecolors=facecolors)
        ax.set_axis_off()

      self.axs[0].view_init(azim=127, elev=-45)

      return self.axs
