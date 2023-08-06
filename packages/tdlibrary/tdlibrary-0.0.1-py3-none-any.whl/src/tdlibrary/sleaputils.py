import sleap
import numpy as np


def clean_sleap_file(slp_file, num_animals, dist_thresh=100):
    labels = sleap.load_file(slp_file)
    out_slp_file = slp_file.split('.')[0] + '_fixed.h5'
    og_track_list = []
    track_cents = []
    for n in range(num_animals):
        og_track_list.append(labels.tracks[n])
        if len(labels[0].instances) == 0:
            track_cents.append(np.array([0,0]))
        else:
            track_cents.append(labels[0].instances[n].centroid)
    c = 1
    for l in labels.labeled_frames:
        if c % 1000 == 0:
            print('Cleaning slp file, on frame: ', c)
        out_ins = []
        num_i = len(l.instances)
        if num_i > 0:
            insts = l.instances
            track_dists = np.zeros((num_animals, num_i))
            for ind, z in enumerate(zip(og_track_list, track_cents)):
                t, tc = z[:]
                for ind2, i in enumerate(insts):
                    d = np.linalg.norm(tc - i.centroid)
                    track_dists[ind, ind2] = d
            closest_i = np.argmin(track_dists, axis=1)
            for c_i in closest_i:
                min_t = np.argmin(track_dists[:, c_i])
                insts[c_i].track = og_track_list[min_t]
                out_ins.append(insts[c_i])
            l.instances = out_ins
        c += 1
    labels.export(out_slp_file)
    return out_slp_file