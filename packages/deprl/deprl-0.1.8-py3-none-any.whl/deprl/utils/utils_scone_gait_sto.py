import os

import numpy as np
from matplotlib import pyplot as plt


# precision = 0.5 # slow but accurate
# precision = 0.5 # fast but inaccurate
# 0.1
precision = 0.1 # fast but inaccurate

FORCE_THRESHOLD = 0.01
GRF_LIST = ["leg1_r.grf_norm_y", "leg0_l.grf_norm_y"]
JOINT_LIST = [
    "hip_flexion_r",
    "knee_angle_r",
    "ankle_angle_r",
    "hip_flexion_l",
    "knee_angle_l",
    "ankle_angle_l",
    "time",
]


def deg_2_rad(x):
    return (x / 360) * (2 * np.pi)


def check_force(grf, time):
    if grf[time] > FORCE_THRESHOLD:
        return 1
    else:
        return 0


def extract_normalized(sto, begin, end, time):
    """
    Takes in a list of values <sto> and uses <time> to extend the duration using
    interpolation to a continuous percentage of the gait cycle. This is used
    to avoid small shifts in gait cycle timings from accumulating.
    """
    new_sto = []
    for perc in np.arange(0, 100, precision):
        t = begin + perc * (end - begin) / 100
        new_sto.append(interpolate(sto, time, t))
    return new_sto


def interpolate(sto, time, t):
    """
    Outputs the linear interpolation of <sto> at time <t>, where the discretized
    times are given by <time>.
    """
    lower_index = -1
    upper_index = -1
    for i in range(len(time)):
        if time[i] <= t:
            lower_index = i
        if time[i] > t:
            upper_index = i
            break
    if upper_index == -1:
        upper_index = lower_index
    if upper_index == lower_index and upper_index == len(time) - 1:
        return sto[-1]
    alpha = (t - time[lower_index]) / (time[upper_index] - time[lower_index])
    return sto[lower_index] * (1 - alpha) + sto[upper_index] * alpha


def get_gait_start_times(time, grf):
    """
    Find gait start times from foot contact set-downs.
    """
    grf = np.array(extract_normalized(grf, time[0], time[-1], time))
    time_extended = np.array(extract_normalized(time, time[0], time[-1], time))
    prev_force = 0
    gait_start_times = []
    for tdx in range(grf.shape[0]):
        force = check_force(grf, tdx)
        if not prev_force and force:
            gait_start_times.append(time_extended[tdx])
        prev_force = force
    return gait_start_times[1:]


# TODO find params that work for 2D gait perfectly, then try metrics on this. then either tune coeffs for 3D or tune mpo or dep for 3D.


def extract_gait_cycle(joint, time, grf):
    gait_start_times = get_gait_start_times(time, grf)
    gaits = []
    for idx in range(len(gait_start_times) - 1):
        gaits.append(
            extract_normalized(
                joint, gait_start_times[idx], gait_start_times[idx + 1], time
            )
        )
    return np.array(gaits)


def prepare_hip(arr):
    return arr


def prepare_ankle(arr):
    # offset in experimental data, read out from zml
    arr = [x + 0.349 for x in arr]
    return arr
    # return [x + 0.349 for x in arr]


def prepare_knee(arr):
    """
    prepare knee data. the mirroring around 0 switches the minimum and
    maximum arrays around, but tuples don't allow for item assignment.
    so we cast to list.
    """
    return arr


def normalize(arr, mini=None, maxi=None):
    if mini is None and maxi is None:
        mini = np.min(arr)
        maxi = np.max(arr)
    arr = np.array(arr)
    arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))
    return np.asarray(arr), mini, maxi


def load_exp_data():
    """
    Save data as (mean, min, max) for each gait cycle.
    """
    file1 = open(os.path.join(os.path.dirname(__file__), "resources/exp_gait.zml"), "r")
    lines = file1.readlines()
    maxs = None
    means = None
    mins = None
    for line in lines:
        if "title" in line:
            title = " ".join(line.split()[-2:])
        if "norm_max" in line:
            maxs = line.split()[3:-1]
            maxs = np.array(maxs, dtype=np.float32)
        if "norm_min" in line:
            mins = line.split()[3:-1]
            mins = np.array(mins, dtype=np.float32)
        if "norm_mean" in line:
            means = line.split()[3:-1]
            means = np.array(means, dtype=np.float32)
        if maxs is not None and "Hip" in title:
            hip = (
                deg_2_rad(means.copy()),
                deg_2_rad(mins.copy()),
                deg_2_rad(maxs.copy()),
            )
            maxs = None
            mins = None
            means = None
        if maxs is not None and "Knee" in title:
            knee = (
                deg_2_rad(means.copy()),
                deg_2_rad(mins.copy()),
                deg_2_rad(maxs.copy()),
            )
            maxs = None
            mins = None
            means = None
        if maxs is not None and "Ankle" in title:
            ankle = (
                deg_2_rad(means.copy()),
                deg_2_rad(mins.copy()),
                deg_2_rad(maxs.copy()),
            )
            maxs = None
            means = None
            mins = None
    # return prepare_hip(hip), prepare_knee(knee), prepare_ankle(ankle)
    return prepare_hip(hip), prepare_knee(knee), prepare_ankle(ankle)


def euclid(query, template):
    length = np.minimum(len(query), len(template))
    return np.mean(np.square(np.array(query)[:length] - np.array(template)[:length]))


def get_avg_gait_cycle(joints, grf):
    gaits = []
    for gidx, jdxs in zip(range(2), [range(-6, -3), range(-3, 0)]):
        for joints_query, grf_query in zip(joints, grf):
            gaits_query = extract_gait_cycle(
                [x[jdxs] for x in joints_query],
                [x[0] for x in joints_query],
                remove_small_peaks([x[gidx] for x in grf_query]),
            )
            if gaits_query.shape[0] > 0:
                gaits.append(gaits_query)
            # gaits.append(gaits_template)
    gaits_mean = [np.mean(x, axis=0) for x in gaits]
    return gaits, gaits_mean


def filter_nans_out_of_list(arr):
    return arr[np.where(~np.isnan(np.array(arr)))]


def get_avg_dtwd(joints, grfs, plot=False, convert_fn=None):
    gaits, gaits_mean = get_avg_gait_cycle(joints, grfs)
    if convert_fn is not None:
        gaits, gaits_mean = convert_fn(gaits, gaits_mean)
    if len(gaits) == 0:
        return (0, 0, 0, 0)
    exp_data = load_exp_data()
    exp_data = [list(x) for x in exp_data]
    for i in range(len(exp_data)):
        for j in range(len(exp_data[i])):
            exp_data[i][j] = np.roll(exp_data[i][j], exp_data[i][j].shape[0] // 2, axis=0)
    if plot:
        fig, axs = plt.subplots(3, 1)
        fig, axs = get_plot(fig, axs, gaits, gaits_mean, color="grey")
        get_plot_exp(fig, axs, name="exp", color="grey", plot_mean=False)
        fig.savefig("test.png")
    time_exp = np.linspace(0, 1, 101)
    counter = [[], [], []]
    for gait in gaits_mean:
        time = np.linspace(0, 1, gait.shape[0])
        for g in range(3):
            for tidx, val in enumerate(gait[:, g]):
                if val < interpolate(
                    exp_data[g][2], time_exp, time[tidx]
                ) and val > interpolate(exp_data[g][1], time_exp, time[tidx]):
                    counter[g].append(1)
                else:
                    counter[g].append(0)
    return (
        np.mean(counter[0]) + 1 * np.mean(counter[1]) + 1 * np.mean(counter[2]),
        np.mean(counter[0]),
        np.mean(counter[1]),
        np.mean(counter[2]),
    )

def msd_get_avg_dtwd(joints, grfs, plot=False, convert_fn=None):
    gaits, gaits_mean = get_avg_gait_cycle(joints, grfs)
    exp_data = load_exp_data()
    for sto in gaits_mean:
        dtwds = np.zeros((3,))
        for g in range(3):
            interp_exp_data = []
            for t in np.linspace(0, 1, sto.shape[0]):
                interp_exp_data.append(interpolate(exp_data[g][0], np.linspace(0, 1, 101), t))
            dtwds[g] = np.mean(np.square(interp_exp_data - sto[:, g]))
    return np.sum(dtwds), dtwds[0], dtwds[1], dtwds[2]

def new_get_avg_dtwd(joints, grfs, plot=False, convert_fn=None):
    gaits, gaits_mean = get_avg_gait_cycle(joints, grfs)
    if convert_fn is not None:
        gaits, gaits_mean = convert_fn(gaits, gaits_mean)
    exp_data = load_exp_data()
    exp_data = [list(x) for x in exp_data]
    dtwd_collector = []
    for sto in gaits_mean:
        dtwds = np.zeros((3,))
        for g in range(3):
            interp_exp_data = []
            for t in np.linspace(0, 1, sto.shape[0]):
                interp_exp_data.append([interpolate(exp_data[g][j], np.linspace(0, 1, 101), t) for j in range(3)])
            interp_exp_data = np.array(interp_exp_data)
            arr1 = np.where(interp_exp_data[:, 1] < sto[:, g])[0]
            arr2 = np.where(interp_exp_data[:, 2] > sto[:, g])[0]
            common = np.intersect1d(arr1, arr2)
            dtwds[g] = common.shape[0] / interp_exp_data[:, 0].shape[0]
        dtwd_collector.append(dtwds)
    if plot:
        fignew, axnew = plt.subplots(3, 1)
        axnew[0].plot(np.linspace(0, 1, exp_data[0][0].shape[0]), exp_data[0][0], color='blue')
        axnew[0].plot(np.linspace(0, 1, exp_data[0][1].shape[0]), exp_data[0][1], color='red')
        axnew[0].plot(np.linspace(0, 1, exp_data[0][2].shape[0]), exp_data[0][2], color='green')
        axnew[0].plot(np.linspace(0, 1, gaits_mean[0][:,0].shape[0]), gaits_mean[0][:, 0], color='black')
        plt.savefig('testimage.pdf')
    dtwd_mean = [np.mean([x[i] for x in dtwd_collector]) for i in range(3)]
    return np.sum(dtwd_mean), dtwd_mean[0], dtwd_mean[1], dtwd_mean[2]




def get_plot(fig, axs, gaits, gaits_mean, color="tab:red", name=None, index=0):
    names = ["hip", "knee", "ankle"]
    plot_all = False
    plot_mean = True
    if plot_all:
        for sto in gaits:
            for gait in sto:
                for g in range(3):
                    axs[g].plot(
                        np.linspace(0, 1, gait.shape[0]),
                        gait[:, g],
                        color=color,
                        alpha=0.1,
                    )
                    axs[g, index].set_xlim([0, 1])
                    axs[g, 0].set_ylabel(f"{names[g]} [rad]")
    # if plot_mean:
    #     for gait in gaits_mean:
    #         for g in range(3):
    #             axs[g, index].plot(
    #                 np.linspace(0, 1, gait.shape[0]), gait[:, g], color=color, alpha=0.2
    #             )
    #             axs[g, index].set_xlim([0, 1])
    #             axs[g, 0].set_ylabel(f"{names[g]} [rad]")
    hip = np.mean([x[:, 0] for x in gaits_mean], axis=0)
    knee = np.mean([x[:, 1] for x in gaits_mean], axis=0)
    ankle = np.mean([x[:, 2] for x in gaits_mean], axis=0)
    axs[0, index].plot(np.linspace(0, 1, hip.shape[0]), hip, color="tab:red", linewidth=1)
    axs[1, index].plot(np.linspace(0, 1, knee.shape[0]), knee, color="tab:red", linewidth=1)
    axs[2, index].plot(np.linspace(0, 1, ankle.shape[0]), ankle, color="tab:red", linewidth=1)
    if name is not None:
        plt.savefig(f"{name}.pdf")
        return
    return fig, axs


def get_plot_exp(fig, axs, color="tab:red", name="none", plot_mean=True, index=0):
    exp_data = load_exp_data()
    exp_data = [list(x) for x in exp_data]
    # for i in range(len(joints)):
    #     for j in range(len(joints[i])):
    #         joints[i][j] = np.roll(joints[i][j], joints[i][j].shape[0] // 2, axis=0)
    hip, knee, ankle = exp_data
    if plot_mean:
        axs[0, index].plot(
            np.linspace(0, 1, hip[0].shape[0]), hip[0], color=color, linewidth=3
        )
    axs[0, index].fill_between(
        np.linspace(0, 1, hip[0].shape[0]),
        hip[1],
        hip[2],
        color=color,
        linewidth=3,
        alpha=0.2,
    )
    if plot_mean:
        axs[1, index].plot(
            np.linspace(0, 1, knee[0].shape[0]), knee[0], color=color, linewidth=3
        )
    axs[1, index].fill_between(
        np.linspace(0, 1, knee[0].shape[0]),
        knee[1],
        knee[2],
        color=color,
        linewidth=3,
        alpha=0.2,
    )
    if plot_mean:
        axs[2, index].plot(
            np.linspace(0, 1, ankle[0].shape[0]), ankle[0], color=color, linewidth=3
        )
    axs[2, index].fill_between(
        np.linspace(0, 1, ankle[0].shape[0]),
        ankle[1],
        ankle[2],
        color=color,
        linewidth=3,
        alpha=0.2,
    )
    axs[2, index].set_xlabel("gait cycle [%]")
    names = ["hip", "knee", "ankle"]
    for i in range(axs.shape[0]):
        axs[i, 0].set_ylabel(f"{names[i]} [rad]")
        axs[i, index].set_xlim([0, 1])
    return fig, axs


def list_of_strings_2_string(list_of_strings):
    string = ""
    for s in list_of_strings:
        string += s
    return string


"""
for sto in sto_files:
    path = os.path.join(folder, sto)
    joints_rl, grf_rl = read_joints(name=path, color='tab:red')
    joints_geyer, grf_geyer = read_joints(name='geyer.sto', color='tab:blue')

    ret = 0
    for gidx, jdxs in zip(range(2), [[-6, -5, -4], [-3, -2, -1]]):
        ret += np.mean([get_sample_dtwd(joints_rl, grf_rl[:, gidx], joints_geyer, grf_geyer[:, gidx], jdx) for jdx in jdxs])
    return [ret if not np.isnan(ret) else 200][0]
"""


def readMotionFile(filename):
    """Reads OpenSim .sto files.
    Parameters
    ----------
    filename: absolute path to the .sto file
    Returns
    -------
    header: the header of the .sto
    labels: the labels of the columns
    data: an array of the data
    """
    filename = os.path.join(os.path.abspath(__file__), "resources/", filename)
    if not os.path.exists(filename):
        print("file do not exists")

    file_id = open(filename, "r")

    # read header
    next_line = file_id.readline()
    header = [next_line]
    nc = 0
    nr = 0
    while "endheader" not in next_line:
        if "datacolumns" in next_line:
            nc = int(next_line[next_line.index(" ") + 1 : len(next_line)])
        elif "datarows" in next_line:
            nr = int(next_line[next_line.index(" ") + 1 : len(next_line)])
        elif "nColumns" in next_line:
            nc = int(next_line[next_line.index("=") + 1 : len(next_line)])
        elif "nRows" in next_line:
            nr = int(next_line[next_line.index("=") + 1 : len(next_line)])

        next_line = file_id.readline()
        header.append(next_line)

    # process column labels
    next_line = file_id.readline()
    if next_line.isspace() is True:
        next_line = file_id.readline()

    labels = next_line.split()

    # get data
    data = []
    for i in range(1, nr + 1):
        d = [float(x) for x in file_id.readline().split()]
        data.append(d)

    file_id.close()

    return header, labels, data, nc, nr


def read_joints(name):
    ret = readMotionFile(name)
    joints = []
    grf = []
    for time in ret[2]:
        joint_step = []
        grf_step = []
        for idx, element in enumerate(time):
            if ret[1][idx] in JOINT_LIST:
                joint_step.append(element)
            if ret[1][idx] in GRF_LIST:
                grf_step.append(element)
        joints.append(joint_step)
        grf.append(grf_step)
    joints = np.array(joints)
    grf = np.array(grf)
    return joints, grf

def read_energy(name):
    ret = readMotionFile(name)
    acts = []
    for time in ret[2]:
        act_step = []
        for idx, element in enumerate(time):
            if "activation" in ret[1][idx]:
                act_step.append(element)
        acts.append(act_step)
    acts = np.array(acts)
    return np.mean(np.power(acts, 3))


def remove_small_peaks(arr, sensitivity=FORCE_THRESHOLD, threshold=0.8):
    arr = np.asarray(arr)
    peak_on, prev_peak, pmax = 0, 0, 0
    for i in range(arr.shape[0]):
        peak_on = [1 if arr[i] > sensitivity else 0][0]
        if peak_on and not prev_peak:
            start = i
        if peak_on and prev_peak:
            pmax = max(pmax, arr[i])
        if not peak_on and prev_peak:
            if pmax < threshold:
                arr[start:i] = 0
            pmax = 0
        prev_peak = peak_on
    return arr
