import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import h5py

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 18


def plot_with_slider_1D(data, time, tf_data, gripper_data):
    cur_idx = 0
    time = time % 10000
    time = time - time[0]
    fig, ax = plt.subplots(figsize=(9, 7))
    plt.subplots_adjust(bottom=0.27, left=0.08, right=0.7, top=0.75, hspace=0.4)
    
    labels = ['x', 'y', 'z']
    colors = ["red", "blue", "green"]

    for d in range(len(data)):
        ax.plot(range(len(data[d])), data[d], label=f'{labels[d]}', color=colors[d], alpha=0.5, linewidth=2)
        ax.tick_params(axis='both', which='both', left=False, bottom=False, top=False, length=0, labelleft=False, labelbottom=False) # labels along the bottom edge are off

    ax.grid(True, linestyle='-', color='white', alpha=0.5)
    
    x1_positions = [0, 1125, 2591, 3986, 5666]
    colors = ["purple", "teal", "navy", "orange", "brown"]
    labels = ["plate", "napkin", "cup", "fork", "spoon"]
    
    plot_with_images(ax, folder="4", x_positions=x1_positions, colors=colors, labels=labels)
    
    zero_indices = np.where(gripper_data[1] <= 0.0499)[0]
    for i in zero_indices:
        ax.axvline(i, color="gray", linestyle="-", alpha=0.01)
        ax.tick_params(axis='both', which='both', left=False, bottom=False, top=False, length=0, labelleft=False, labelbottom=False, labeltop=False) # labels along the bottom edge are off
        ax.tick_params(axis='both', which='both', left=False, bottom=False, top=False, length=0, labelleft=False, labelbottom=False, labeltop=False) # labels along the bottom edge are off

    #darker_line = Line2D([], [], color='gray', linestyle='-', alpha=1, label='gripper closed')
    gray_patch = mpatches.Patch(color='gray', alpha = 0.5, label='gripper closed')
    handles, labels = ax.get_legend_handles_labels()
    handles.append(gray_patch)
    ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=1)
    ax.set_facecolor("#E5E5E5")
    
    ax2 = ax.twiny()
    for d in range(3):
        ax2.plot(time, tf_data[1][:, d], color=colors[d], alpha=0)
        ax2.tick_params(axis='both', which='both', left=False, bottom=False, top=False, length=0, labelleft=False, labelbottom=False, labeltop=False) # labels along the bottom edge are off

    plt.savefig("gt_plot.png", dpi=300)
    plt.show()

def plot_with_images(ax, folder, x_positions, colors, labels, zoom=0.07):
    base_path = "/Users/wendy/Desktop/school/uml/robotics/auto_correlation/raw data/fetch_table_demos/long tasks/screenshots/1/"
    
    for i, (x_pos, color, label) in enumerate(zip(x_positions, colors, labels)):
        ax.axvline(x_pos, color=color, alpha=1, linestyle="--", label=label, linewidth=3)
        
        img_path = f"{base_path}/{label}.png"
        img = plt.imread(img_path)
        image_box = OffsetImage(img, zoom=zoom)
        
        box_offset = -.55 if i % 2 == 0 else 2.75
        ab = AnnotationBbox(image_box, (x_pos, 1), frameon=False, box_alignment=(0.5, box_offset))
        ax.add_artist(ab)
        ax.tick_params(axis='both', which='both', left=False, bottom=False, top=False, length=0, labelleft=False, labelbottom=False) # labels along the bottom edge are off

def read_data(fname):
    hf = h5py.File(fname, 'r')
    js = hf.get('joint_state_info')
    joint_time = np.array(js.get('joint_time'))
    joint_pos = np.array(js.get('joint_positions'))
    joint_vel = np.array(js.get('joint_velocities'))
    joint_eff = np.array(js.get('joint_effort'))
    joint_data = [joint_time, joint_pos, joint_vel, joint_eff]

    tf = hf.get('transform_info')
    tf_time = np.array(tf.get('transform_time'))
    tf_pos = np.array(tf.get('transform_positions'))
    tf_rot = np.array(tf.get('transform_orientations'))
    tf_data = [tf_time, tf_pos, tf_rot]

    gp = hf.get('gripper_info')
    gripper_time = np.array(gp.get('gripper_time'))
    gripper_pos = np.array(gp.get('gripper_position'))
    gripper_data = [gripper_time, gripper_pos]

    hf.close()

    return joint_data, tf_data, gripper_data

if __name__ == '__main__':
    path = "../table task/xyz data/full_tasks/fetch_recorded_demo_1730997119.txt"
    h5_path = "../table task/h5 files/fetch_recorded_demo_1730997119.h5"
    data = np.loadtxt(path)  # load the file into an array

    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]

    joint_data, tf_data, gripper_data = read_data(h5_path)
    time = tf_data[0][:, 0] + tf_data[0][:, 1] * (10.0 ** -9)

    traj_list = [x, y, z]
    traj = data
    plot_with_slider_1D(traj_list, time, tf_data, gripper_data)
