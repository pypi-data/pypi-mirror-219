import numpy as np
import h5py
import matplotlib.pyplot as plt
import sleap


def get_territory_data(file_name, rot_offset=0, num_f=0):
    in_rad = np.radians(rot_offset)
    rad_cm = 30.48  # radius of arena in cm (12in)
    px_per_cm = 350 / rad_cm
    ref_point = [650, 500]
    c, s = np.cos(in_rad), np.sin(in_rad)
    rot_mat = [[c, -s], [s, c]]
    sleap_data = h5py.File(file_name, 'r')
    # labels = sleap.load_file(file_name)
    mouse_data = sleap_data['tracks']
    if num_f == 0:
        num_f = np.shape(mouse_data)[3]
    mouse_data = mouse_data[:, :, :, :num_f]
    sleap_pts = np.nanmean(mouse_data, axis=0)
    head_angles = get_head_direction(sleap_pts)
    mouse_cent = np.nanmean(sleap_pts, axis=1).T
    rel_xy = mouse_cent - ref_point
    rel_xy[:, 1] = -rel_xy[:, 1]
    x = rel_xy[:, 0]
    y = rel_xy[:, 1]
    xy = rot_mat @ np.vstack((x, y))
    cent_x = xy[0, :] / px_per_cm
    cent_y = xy[1, :] / px_per_cm
    dist_vec = np.linalg.norm(rel_xy[1:, :] - rel_xy[:-1, :], axis=1) / px_per_cm
    dist_vec = np.hstack(([0], dist_vec))
    return cent_x, cent_y, head_angles, dist_vec, sleap_pts


def compute_preferences(xy, walls=None):
    if walls is None:
        walls = [-np.pi / 2, 5 * np.pi / 6, np.pi / 6]
    x = xy[:, 0]
    y = xy[:, 1]
    t = np.arctan2(y, x)
    ter_a = np.logical_or(t < walls[0], t > walls[1])
    ter_b = np.logical_and(t > walls[0], t < walls[2])
    ter_c = np.logical_and(t > walls[2], t < walls[1])
    prefs = np.zeros(len(walls))
    for i, ter in enumerate((ter_a, ter_b, ter_c)):
        prefs[i] = np.sum(ter) / len(t)
    return prefs


def get_head_direction(mouse_data, in_deg=False):
    md_copy = np.copy(mouse_data)
    md_copy[1, :, :] = -md_copy[1, :, :]
    xy_nose = md_copy[:, 0, :] - md_copy[:, 1, :]
    angs = np.arctan2(xy_nose[1, :], xy_nose[0, :])
    if in_deg:
        angs = np.degrees(angs)
    return angs


def avg_angs(angs):
    avg_s = np.nanmean(np.sin(angs))
    avg_c = np.nanmean(np.cos(angs))
    return np.arctan2(avg_s, avg_c)


def compute_over_spatial_bin(xpos, ypos, data, func, bins=20, range=None):
    if range is None:
        range = [[-400, 400], [-400, 400]]
    _, xedges, yedges = np.histogram2d(xpos, ypos, bins=bins, range=range)
    out_hist = np.zeros((len(xedges) - 1, len(yedges) - 1))
    for i, xe in enumerate(xedges[:-1]):
        in_x = np.logical_and(xpos > xe, xpos < xedges[i + 1])
        for j, ye in enumerate(yedges[:-1]):
            in_y = np.logical_and(ypos > ye, ypos < yedges[j + 1])
            in_bin = np.logical_and(in_x, in_y)
            out_hist[i, j] = func(data[in_bin])
    return out_hist, xedges, yedges


def plot_territory(ax, t, r):
    walls = [-np.pi / 2, 5 * np.pi / 6, np.pi / 6]
    num_f = len(t)
    ter_a = np.logical_or(t < walls[0], t > walls[1])
    ter_b = np.logical_and(t > walls[0], t < walls[2])
    ter_c = np.logical_and(t > walls[2], t < walls[1])
    cmap = np.tile([0.6, 0.6, 0.6], (num_f, 1))
    ax.set_xticks([])
    ax.set_yticks([])
    cmap[ter_b, :] = [0, 0.6, 0]
    cmap[ter_a, :] = [0.7, 0.6, 0.3]
    # ax.scatter(t, r, c=cmap, s=3)
    h, te, re, _ = ax.hist2d(t, r, bins=50, range=[[np.nanmin(t), np.nanmax(t)], [np.nanmin(r), np.nanmax(r)]],
                             density=True)
    return h, te, re


def add_territory_circle(ax, walls=None, is_polar=False, arena_width_cm=28):
    if walls is None:
        walls = [-np.pi / 2, 5 * np.pi / 6, np.pi / 6]


def xy_func(x):
    return np.vstack(([x[0]], [x[1]])).T


def heatmap_group(g, list_xy, info):
    x_acc = np.array([])
    y_acc = np.array([])
    plt.figure()
    for xy in list_xy:
        x_acc = np.hstack((x_acc, xy[:, 0]))
        y_acc = np.hstack((y_acc, xy[:, 1]))

    plt.hist2d(x_acc, y_acc, bins=25,
               range=[[np.nanmin(x_acc), np.nanmax(x_acc)], [np.nanmin(y_acc), np.nanmax(y_acc)]],
               density=True)


def scatter_groups(g, list_pref, info):
    sub_col = {'KinA1': [0.8, 0, 0],
               'KinA2': [0.7, 0.1, 0],
               'KinA3': [0.6, 0.2, 0],
               'KinA4': [0.5, 0.3, 0],
               'KinB1': [0, 0.3, 0.5],
               'KinB2': [0, 0.2, 0.6],
               'KinB3': [0, 0.1, 0.7],
               'KinB4': [0, 0, 0.8]}
    f = plt.figure()
    for p, this_i in zip(list_pref, info):
        c = sub_col[this_i['Subject']]
        x = np.arange(3)
        plt.plot(x, p, color=c)


def get_t(x):
    t = np.arctan2(x[1], x[0])
    return t


def plot_bias(g, prefs, info):
    thetas = np.array([7 * np.pi / 6, 11 * np.pi / 6, np.pi / 2])
    xs = []
    ys = []
    for p in prefs:
        r = p[0]
        x = r @ np.cos(thetas)
        y = r @ np.sin(thetas)
        xs.append(x)
        ys.append(y)
    if g is "Day0":
        plt.plot(xs, ys, 'x-b')
    else:
        plt.plot(xs, ys, 'x-b')

def hist_t(g, ts, info):
    group_t = np.array([])
    for t in ts:
        group_t = np.hstack((group_t, t))
    ax = plt.subplot(projection='polar')
    vals, bin_edges = np.histogram(np.degrees(group_t), bins=20, range=[np.nanmin(group_t), np.nanmax(group_t)])
    ax.plot(bin_edges[:-1], vals)
    plt.show()
    print('y')
