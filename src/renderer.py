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

      self.anax = self.fig.add_subplot(spec[0, 2])
      self.hopperax = self.fig.add_subplot(spec[1:, 2])

      self.fig.tight_layout()

  # a frame is a tuple of (ticks, voxels, hopper_contents, capacity)
  def animate(self, frames):
      animation.FuncAnimation(self.fig, self.render, frames, blit=True,
                              interval=20, repeat=False)
      plt.show()

  def singleFrame(self, voxels):
      self.render((0, voxels, [], 1))
      plt.show()

  def render(self, frame):
      time, voxels, hopper, capacity = frame
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

      self.axs[0].view_init(azim=135, elev=-45)
      self.axs[1].view_init(azim=135, elev=45)

      self.anax.cla()
      self.hopperax.cla()

      hopper_plot = np.zeros((capacity, 1, 4))
      for i, a in enumerate(hopper):
        for j, channel in enumerate(a):
          hopper_plot[-(i+1)][0][j] = channel / 256
        hopper_plot[-(i+1)][0][3] = 1
      try:
        self.hopperax.set_data(hopper_plot)
      except AttributeError:
        self.hopperax.imshow(hopper_plot)
      self.hopperax.patch.set_edgecolor('gray')
      self.hopperax.patch.set_linewidth('2')

      anno_opts = dict(xy=(0.5, 0.5), xycoords='axes fraction',
                       va='center', ha='center')
      self.anax.annotate(f'{time} ticks, hopper {len(hopper)}/{capacity}', **anno_opts)
      self.anax.set_axis_off()

      return self.axs + [self.anax, self.hopperax]
