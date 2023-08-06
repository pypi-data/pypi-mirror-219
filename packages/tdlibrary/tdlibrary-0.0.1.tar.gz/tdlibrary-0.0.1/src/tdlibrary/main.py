import sleaputils as su
import tdtools as tdt
from tkinter import filedialog
import numpy as np


def main():
    slp_files = filedialog.askopenfilenames(title="Open a SLEAP File",
                                            filetypes=(("SLEAP file", "*.slp"), ("H5 file", "*.h5"),
                                                       ("CSV", "*.csv"), ("All types", "*.*")))
    rot_dict = {'RNI': 0,
                'IRN': 120,
                'NIR': 240}
    for ind, f in enumerate(slp_files):
        file_type = f.split('.')[-1]
        if file_type == "slp":
            file_name = su.clean_sleap_file(f, 1)
        if file_type == "h5":
            file_name = f
        if file_type == "csv":
            data = np.loadtxt(f, delimiter=",", dtype=str).astype(float)
            cent_x = data[:, 0]
            cent_y = data[:, 1]
        else:
            orient = input('Arena orientation for file: ' + f + '?')
            cent_x, cent_y, head_angles, dist_vec, _ = tdt.get_territory_data(file_name, rot_offset=rot_dict[orient])
            data = (cent_x, cent_y, head_angles, dist_vec)
            data2 = np.vstack(data).T
            np.savetxt(file_name + '.csv', data2, delimiter=',')
        xy = np.vstack((cent_x, cent_y)).T
        prefs = tdt.compute_preferences(xy)
        print(prefs[0], ',', prefs[1], ',', prefs[2])


if __name__ == "__main__":
    main()
