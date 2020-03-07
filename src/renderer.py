from matplotlib import pyplot as plt, animation as animation
import numpy as np

class Renderer(object):
  def __init__(self):
      self.fig = plt.figure(figsize=[8, 8])
      widths = [1, 3, 1]
      heights = [1, 1, 1]
      spec = self.fig.add_gridspec(ncols=3, nrows=3, width_ratios=[1, 3, 1],
                                height_ratios=[1, 1, 1])
      self.axs = dict()
      for row in range(3):
          for col in [0, 2]:
              ax = self.fig.add_subplot(spec[row, col])
              ax.set_aspect('equal')
              ax.set_axis_off()
              self.axs[(row, col)] = ax

      self.main_ax = self.fig.add_subplot(spec[0:, 1], projection='3d')
      self.fig.tight_layout()

  def animate(self, frames):
      animation.FuncAnimation(self.fig, self.render, frames, blit=True, interval=20, repeat=False)
      plt.show()

  def singleFrame(self, frame):
      self.render(frame)
      plt.show()

  def render(self, voxels):
      self.main_ax.cla()
      filled = np.empty_like(voxels, dtype='b')
      facecolors = np.ndarray(filled.shape + (3,))

      # alphafacecolors = np.ndarray((n, n, n, 4))
      for i, a in enumerate(voxels):
          for j, b in enumerate(a):
              for k, c in enumerate(b):
                  if c:
                      filled[i][j][k] = True
                      for l in range(3):
                          facecolors[i][j][k][l] = c[l] / 256.
                          # alphafacecolors[i][j][k][l] = c[l] / 256.
                      # alphafacecolors[i][j][k][3] = 1
                  else:
                      facecolors[i][j][k] = [0,0,0]
                      # alphafacecolors[i][j][k] = [0,0,0,0]
                      filled[i][j][k] = False
      self.main_ax.voxels(filled, facecolors=facecolors)
      self.main_ax.set_axis_off()

      return [self.main_ax]
