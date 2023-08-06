import cv2
import sleap as slp
import h5py
from matplotlib.gridspec import GridSpec
import tdtools
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate, correlation_lags


class Peetector:
    def __init__(self, file_prefix, h_thresh=100, s_kern=5, di_kern=51, t_thresh=20, dead_zones=[], rot_ang=0):
        self.thermal_vid = cv2.VideoCapture(file_prefix + '.avi')
        self.fill_pts = self.sleap_to_fill_pts(file_prefix + '.h5')
        self.h_thresh = h_thresh
        self.s_kern = s_kern
        self.di_kern = di_kern
        self.t_thresh = t_thresh
        self.set_dz(dead_zones)

    def sleap_to_fill_pts(self, sleap_h5):
        with h5py.File(sleap_h5, "r") as f:
            locations = f["tracks"][:].T
        t, d1, d2, d3 = np.shape(locations)
        fill_pts = []
        for i in range(t):
            t_pts = locations[i, :, :, :]
            t_pts = np.moveaxis(t_pts, 0, 1)
            t_pts = np.reshape(t_pts, (d2, d1 * d3))
            keep = ~np.all(np.isnan(t_pts), axis=0)
            k_pts = t_pts[:, keep]
            fill_pts.append(k_pts.T)
        return fill_pts

    def set_dz(self, dead_zones):
        if dead_zones == "Block0":
            w1 = np.array([[316, 210], [330, 210], [330, 480], [316, 480]])
            w2 = np.array([[311, 212], [111, 111], [129, 85], [306, 197]])
            w3 = np.array([[340, 205], [577, 104], [540, 80], [337, 195]])
            self.dead_zones = (w1, w2, w3)
        else:
            self.dead_zones = dead_zones

    def peetect_frame(self, frame_num):
        vid_obj = self.thermal_vid
        kern = np.ones((self.s_kern, self.s_kern), np.float32) / (self.s_kern * self.s_kern)
        kern2 = np.ones((self.di_kern, self.di_kern), np.uint8)
        urine_evts_times = []
        urine_evts_xys = []
        self.thermal_vid.set(cv2.CAP_PROP_POS_FRAMES, frame_num - 1)
        is_read, frame_i = vid_obj.read()
        if is_read:
            im_w = np.shape(frame_i)[1]
            im_h = np.shape(frame_i)[0]
            f1 = cv2.cvtColor(frame_i, cv2.COLOR_BGR2GRAY)
            frameg = cv2.filter2D(src=f1, ddepth=-1, kernel=kern)
            cv2.circle(frameg, (320, 208), 50, 255, -1)
            mask_frame = np.zeros_like(frameg)
            cv2.circle(mask_frame, (325, 230), 200, 255, -1)
            frame = cv2.bitwise_and(frameg, frameg, mask=mask_frame)
            mask = np.uint8(255 * (frame > self.h_thresh))
            for dz in self.dead_zones:
                cv2.fillPoly(mask, pts=[dz], color=(255, 255, 255))
            cv2.dilate(mask, kern2, iterations=1)
            cv2.floodFill(mask, None, (320, 208), 0)
            pts = self.fill_pts[frame_num]
            for p in pts:
                px = int(p[0])
                py = int(p[1])
                if 0 < px < im_w and 0 < py < im_h:
                    if mask[py, px] > 0:
                        cv2.floodFill(mask, None, (int(p[0]), int(p[1])), 0)
            if np.sum(mask) > 0:
                urine_xys = np.argwhere(mask > 0)
                if np.shape(urine_xys)[0] > 1:
                    urine_evts_xys.append(frame_num)
                    urine_evts_xys.append(urine_xys)
        return urine_evts_xys


def clean_urine_by_time(times_file, evts_file):
    true_events = []
    c = 0
    for i, (t, xys) in enumerate(zip(u_times[1:num], u_xys[1:num])):
        check_for_frames = np.arange(t + 1, t + frame_win + 1)
        frames_have_events = np.all(np.isin(check_for_frames, u_times))
        keep_inds = []
        if frames_have_events:
            evt_inds = np.argwhere(np.isin(u_times, check_for_frames))
            next_n_evts = u_xys[evt_inds]
            bool_acc = np.ones(np.shape(xys)[0])
            for e in next_n_evts:
                e_xys = e[0]
                str_xys = np.char.add(xys.astype(str)[:, 0], xys.astype(str)[:, 1])
                str_exys = np.char.add(e_xys.astype(str)[:, 0], e_xys.astype(str)[:, 1])
                all_next = np.isin(str_xys, str_exys)
                bool_acc = np.logical_and(bool_acc, all_next)
            keep_inds = bool_acc
        if np.any(keep_inds):
            xys = xys[keep_inds]
            xys = np.fliplr(xys)
            in_rad = np.radians(rot_ang)
            c, s = np.cos(in_rad), np.sin(in_rad)
            rot_mat = [[c, -s], [s, c]]
            rad_cm = 30.48
            px_per_cm = 215 / rad_cm
            ref_point = [315, 216]
            rel_xy = xys - ref_point
            rel_xy[:, 1] = -rel_xy[:, 1]
            x = rel_xy[:, 0]
            y = rel_xy[:, 1]
            xy = rot_mat @ np.vstack((x, y))
            cent_x = xy[0, :] / px_per_cm
            cent_y = xy[1, :] / px_per_cm
            xys = np.vstack((cent_x, cent_y)).T
            true_events.append(xys)
            true_times.append(t)
        if i % 5000 == 0:
            print(i)
    out_tf = times_file + '_cleanRot.npy'
    out_ef = evts_file + '_cleanRot.npy'
    np.save(out_tf, true_times)
    np.save(out_ef, true_events)
    return out_tf, out_ef


def plot_urine_data(time_file, evt_file):
    times = np.load(time_file)
    evt_xys = np.load(evt_file, allow_pickle=True)
    mask = np.zeros((480, 640))
    c = 0
    f, axs = plt.subplots(3, 1)
    total_marks_left = []
    total_marks_right = []
    for t, e in zip(times, evt_xys):
        for pt in e:
            mask[pt[0], pt[1]] += 1
        total_marks_left.append((t, np.sum(e[:, 1] < 323)))
        total_marks_right.append((t, np.sum(e[:, 1] > 323)))
        print(c)
        # total_marks.append(np.shape(e)[0])
        c += 1
    total_marks_left = np.array(total_marks_left)
    total_marks_right = np.array(total_marks_right)
    axs[0].stem(total_marks_left[:, 0], total_marks_left[:, 1])
    axs[1].stem(total_marks_right[:, 0], total_marks_right[:, 1])
    axs[2].pcolor(mask)
    axs[2].set_ylim(480, 0)
    plt.show()


def get_mask(run_data, thresh=80, block=1):
    evt_xys = run_data[1]
    rad_cm = 30.48
    mask = np.zeros((610, 610))
    for e in evt_xys:
        for pt in e:
            x_ind = round(10 * (pt[1] + rad_cm))
            y_ind = round(10 * (pt[0] + rad_cm))
            mask[x_ind, y_ind] += 1
    out_m = mask > thresh
    out_m = out_m.astype(int)
    if block == 0:
        mask_l = np.copy(out_m)
        mask_r = np.copy(out_m)
        mask_h, mask_w = np.shape(out_m)
        mask_l[:, int(mask_w / 2):] = 0
        mask_r[:, :int(mask_w / 2)] = 0
        return mask_l, mask_r
    else:
        return out_m


def plot_block0(run_data):
    times, evt_xys = run_data[:]
    fig = plt.figure(constrained_layout=True, figsize=(20, 10))
    gs = GridSpec(2, 4, figure=fig)
    total_marks_left, total_marks_right = urine_area_over_time(run_data)
    times = np.arange(len(total_marks_left)) / (40 * 60)
    y1 = max(np.max(total_marks_left), np.max(total_marks_right))
    y1 = y1 + 0.2*y1
    y1 = 1200
    ax0 = fig.add_subplot(gs[1, 2:])
    ax0.plot(times, total_marks_right, c=[1, 0.5, 0])
    ax0.set_ylim(0, y1)
    ax0.set_xlabel('Time (min)')
    ax0.set_ylabel('Urine Area (px)')
    ax1 = fig.add_subplot(gs[0, 2:])
    ax1.plot(times, total_marks_left, c=[0, 0.8, 0])
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Urine Area (px)')
    ax1.set_ylim(0, y1)
    mask_l, mask_r = get_mask(run_data, block=0)
    mask_h, mask_w = np.shape(mask_l)
    rgb = np.zeros((mask_h, mask_w, 3))
    rgb[:, :, 1] += mask_l
    rgb[:, :, 0] += mask_r
    rgb[:, :, 1] += mask_r/2
    ax2 = fig.add_subplot(gs[:, :2])
    ax2.imshow(np.flipud(rgb))
    plt.show()


def get_total_sides(run_data):
    mask_l, mask_r = get_mask(run_data, block=0)
    left_tot = np.sum(mask_l)
    right_tot = np.sum(mask_r)
    return left_tot, right_tot


def urine_area_over_time(run_data, block=0):
    total_marks_left = np.zeros(90000)
    total_marks_right = np.zeros(90000)
    for t, e in zip(run_data[0], run_data[1]):
        total_marks_left[t] = np.sum(e[:, 0] <= 0)
        total_marks_right[t] = np.sum(e[:, 0] > 0)
    total_marks_left = total_marks_left[:72000]
    total_marks_right = total_marks_right[:72000]
    if block == 0:
        return total_marks_left, total_marks_right
    else:
        return total_marks_left + total_marks_right


def plot_all_series_and_mean(g_id, g_data, g_info):
    f, axs = plt.subplots(2, 1, figsize=(20,10))
    m0 = g_data[0]
    num_f = len(m0[0])
    temp = np.zeros((num_f,len(g_data)*2))
    c = -1
    for m in g_data:
        c += 1
        t = np.arange(num_f) / (40*60)
        axs[0].plot(t, m[0], c=[0.5, 0.5, 0.5])
        axs[0].plot(t, m[1], c=[0.5, 0.5, 0.5])
        temp[:,c] = m[0]
        temp[:,c+1] = m[1]
    #     axs[2*c].plot(m[0], c='b')
    #     axs[2*c+1].plot(m[1], c='r')
        # axs[c].set_ylim(0,1000)
    axs[1].plot(t, np.mean(temp, axis=1), c='r')
    plt.show()
    print('yes')


def plot_all_masks(g_id, g_data, g_info):
    f, axs = plt.subplots(1, 1, figsize=(10,10))
    m0 = g_data[0]
    mask = np.zeros_like(m0)
    for g in g_data:
        mask += g
    axs.pcolor(mask)
    plt.show()


def plot_sides(g_id, g_data, g_info):
    data = np.array(g_data)
    plt.figure()
    plt.scatter(data[:,0], data[:,1])
    print(data)


def marks_per_loc(g_id, g_data, g_info):
    for g, g_i in zip(g_data, g_info):
        mask = ut.get_mask(g)
        plt.figure()
        plt.pcolor(mask)
        plt.title(g_i)
        plt.show()
        xy = np.argwhere(mask > 0)/10 - 30.48
        prefs = tdtools.compute_preferences(np.fliplr(xy))
        print(prefs)


def run_cc(g_id, g_data, g_info):
    for g, g_i in zip(g_data, g_info):
        u_r, u_i = ut.urine_area_over_time(g)
        corr = correlate(u_r, u_i)
        lags = correlation_lags(len(u_r), len(u_i))
        corr /= np.max(corr)
        plt.figure()
        plt.plot(lags/(40*60),corr)
        f_name = g_i['Resident'] + ' vs ' + g_i['Intruder'] +  ' Day ' + g_i['Day']
        plt.title(f_name)
        plt.show()