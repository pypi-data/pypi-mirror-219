from matplotlib.axes import Axes
import matplotlib.projections as proj
from matplotlib.transforms import Affine2D, BboxTransformTo, Transform
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 10})

class NickleGraph(Axes):
    name = 'nickleback'

    # def get_xaxis_transform(self, which='grid'):
    #     af = Affine2D()
    #     af.rotate_deg(15)
    #     af.skew(0.125,0.05)
    #     return af


    def _set_lim_and_transforms(self):
        super()._set_lim_and_transforms()
        af = Affine2D()
        af.rotate_deg(12)
        # #af.skew(-0.125,0.2)
        self.transAxes = af + self.transAxes
        self.transData = self.transScale + self.transLimits +  self.transAxes
        self._xaxis_transform = self.transData
        self._yaxis_transform = self.transData

    def draw(self, *args):
        f = self.figure
        num_c = self.get_gridspec().ncols
        num_r = self.get_gridspec().nrows
        s_pts = self.bbox.get_points()
        f_pts = f.bbox.get_points()
        x_val = s_pts[0,0] + s_pts[1,0] * 0.15
        y_val = s_pts[0,1] + s_pts[1,1] * 0.15
        x_dist = f_pts[1,0] / (num_c+1)
        y_dist = f_pts[1, 1] / (num_r + 1)
        xs = []
        ys = []
        for c in range(num_c):
            xs.append(x_dist * (c+1))
        for r in range(num_r):
            ys.append(y_dist * (r+1))
        i = 0
        j = 0
        min_diff = max(f_pts[1,:])
        for ind, x in enumerate(xs):
            if abs(x-x_val) < min_diff:
                i = ind
                min_diff = abs(x-x_val)
        min_diff = max(f_pts[1,:])
        for ind, y in enumerate(ys):
            if abs(y-y_val) < min_diff:
                j = ind
                min_diff = abs(y-y_val)
        w = 1/num_c
        h = 1/num_r
        vals = [w*i, h*j, w, h]
        nick_ax = f.add_axes(vals)
        nick_ax.axis('off')
        nick_ax.set_zorder(0)
        im = plt.imread('graph.png')
        nick_ax.imshow(im, aspect='auto')
        vals = [vals[0]+w/2.6, vals[1]+h/5, w/3, h/2.5]
        self.set_position(vals)
        super().draw(*args)
        nick_ax.draw(*args)


proj.register_projection(NickleGraph)
fig, axes = plt.subplots(3, 30, subplot_kw=dict(projection='nickleback'), figsize=(30,30))


for i in range(np.shape(axes)[0]):
    for j in range(np.shape(axes)[1]):
        x = np.radians(np.arange(360))
        #axes[i,j].scatter(x, np.sin(x))
        im = plt.imread('graph.png')
        axes[i, j].imshow(im, aspect='auto')
# axes[0,0].set_xlim(0, 500)
# axes[0,0].set_ylim(0, 0.5)

plt.show()
