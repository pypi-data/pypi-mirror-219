"""
#TODO: VS CODE CHECK 
#* - import check if used (it works highly and click remove all)

- auto fill the read me of a function when hitting ''' 
- fix color to pycharm color

"""

"""
#! belongs in image tools 

def expand_single_frame_to_3_color_h5(f, f2):
    h5c = image_tools.h5_iterative_creator(f2, overwrite_if_file_exists=True)
    with h5py.File(f, 'r') as h:
        x = h['frame_nums'][:]
        for ii, (k1, k2) in enumerate(tqdm(loop_segments(x), total=len(x))):
            new_imgs = h['images'][k1:k2]
            new_imgs = np.tile(new_imgs[:, :, :, None], 3)
            h5c.add_to_h5(new_imgs, np.ones(new_imgs.shape[0]) * -1)


"""
import shutil

import numpy as np
import os
import glob
from natsort import natsorted, ns
import scipy.io as spio
import h5py
import matplotlib.pyplot as plt
import pandas as pd

import copy
import nillip
import platform
import subprocess
from scipy.signal import medfilt, medfilt2d
import pickle
from tqdm.autonotebook import tqdm

from datetime import datetime
import pytz
import cv2

from pathlib import Path

"""
Arrow Symbol	Arrow Type	Alt Code
↑	Upwards Arrow	24
↓	Downwards Arrow	25
→	Rightwards Arrow 26
←	Leftwards Arrow	27


plt.imshow(tmp2, interpolation='nearest', aspect='auto')

color codes 
https://www.webucator.com/article/python-color-constants-module/


https://stackoverflow.com/questions/18596410/importerror-no-module-named-mpl-toolkits-with-maptlotlib-1-3-0-and-py2exe
import importlib
importlib.import_module('mpl_toolkits').__path__

import mpl_toolkits


# if tqdm_import_helper():
#     from tqdm.notebook import tqdm
# else:
#     from tqdm import tqdm

"""


def remove_vid_from_batch_processing_file(full_file_name, remove_files_list):
    remove_files_list = make_list(remove_files_list, True)
    batch_f = load_obj(full_file_name)

    save_old_file = (get_time_string() + '_batch_processing_old_auto_save').join(
        full_file_name.split('file_list_for_batch_processing'))

    save_obj(batch_f, save_old_file)
    out, inds = lister_it(batch_f['mp4_names'], keep_strings='', remove_string=remove_files_list,
                          return_bool_index=True)

    batch_f['mp4_names'] = list(np.asarray(batch_f['mp4_names'])[inds])
    batch_f['FPS_check_bad_vid_inds'] = list(np.asarray(batch_f['FPS_check_bad_vid_inds'])[inds])
    batch_f['is_processed'] = batch_f['is_processed'][inds]
    os.remove(full_file_name)
    save_obj(batch_f, full_file_name)


def get_bins_from_ax(ax=None):
    if ax is None:
        ax = plt.gca()
    bins_form_patches = np.unique([ax.patches[0].get_x()] + [bar.get_x() + bar.get_width() for bar in ax.patches])
    return bins_form_patches


def zorder(ax, zorder):
    plt.setp(ax.lines, zorder=zorder)
    plt.setp(ax.collections, zorder=zorder)


def NANify_data(tvt_x, tvt_y, tvt_fn, numpy_seed=42):
    nan_array_border_inds = load_nan_border_index()
    tvt_x_naned = []
    for data in tqdm(tvt_x):
        data = copy.deepcopy(data)
        np.random.seed(numpy_seed)
        inds = np.random.choice(nan_array_border_inds.shape[0], data.shape[0])
        replace_with_nans = nan_array_border_inds[inds]
        data[replace_with_nans] = np.nan
        tvt_x_naned.append(data)
    del data

    for i, nan_data in enumerate(tqdm(tvt_x_naned)):
        tvt_x[i] = np.vstack([tvt_x[i], tvt_x_naned[i]])
        tvt_y[i] = np.concatenate([tvt_y[i], tvt_y[i]])
        tvt_fn[i] = np.concatenate([tvt_fn[i], tvt_fn[i]])
    return tvt_x, tvt_y, tvt_fn


def quick_spliter(split_nums, len_array):
    l_nums = np.sum(split_nums)
    count = 1 + (len_array // l_nums)

    inds = np.ones(l_nums)
    for ii, (i1, i2) in enumerate(loop_segments(split_nums)):
        inds[i1:i2] = ii
    inds = np.asarray(list(inds) * count)
    inds = inds[:len_array]

    bool_inds_arrays = []
    for k in range(len(split_nums)):
        bool_inds_arrays.append(np.asarray(k == inds))
    bool_inds_arrays = np.asarray(bool_inds_arrays)

    frame_nums = []
    for b in bool_inds_arrays:
        b2 = group_consecutives(b, 0)[0]
        frame_nums.append([len(k) for k in b2 if np.all(k)])

    return bool_inds_arrays, frame_nums



def _single_to_list_input_checker(in_, len_list):
    in_ = make_list(in_, suppress_warning=True)

    if len(in_) == 1:
        in_ = in_ * len_list
    else:
        assert len(
            in_) == len_list, """'_single_to_list_input_checker' length of input list and the set rquirment dont match"""
    return in_




def _top_percentile_mean(data, p):
    # Compute the cutoff for top p percentile
    cutoff = np.percentile(data, 100 - p)

    # Use boolean indexing to get the top p percent of the data
    top_p_data = data[data >= cutoff]

    # Compute and return the mean of the top p percent
    return np.mean(top_p_data)


def check_vids_for_issues_based_on_FPS_as_an_int(video_files):
    bad_inds = [check_video_fps(video_file) for video_file in tqdm(video_files)]
    return bad_inds


def check_video_fps(video_file):
    video = cv2.VideoCapture(video_file)
    if video.isOpened() == True:
        frame_numbers = int(video.get(7))
        fps = video.get(5)
        if not fps == int(fps):
            print("for file " + os.path.basename(video_file) +
                  " FPS is not an integer, this usually indicates a problem with the video. TOTAL FRAMES = "
                  + str(frame_numbers))
            return True
        else:
            return False
    else:
        print("for file " + os.path.basename(video_file) + " could not open video file")
        return True


def unique_keep_order(x):
    indexes = np.unique(x, return_index=True)[1]
    out = np.asarray([x[index] for index in sorted(indexes)]).astype(int)
    return out


def hex_to_rgb(h):
    h = ''.join(h.split('#'))
    return list(int(h[i:i + 2], 16) for i in (0, 2, 4))


def intersect_data_with_nans(src_data_inds, data_to_match_inds, data=None):
    """

    Parameters
    ----------
    src_data_inds :  come from the data you want to use; inds, trial nums or frame nums, or raw inds; must be unique
    data_to_match_inds : 'src_data_inds' will be forced to match 'data_to_match_inds' index, length and order, inds, trial nums or frame nums, or raw inds; must be unique
    data : matches 'data_to_match_inds' but is the actaul

    Returns
    -------
    index data from data array 'data' that matches the length of 'data_to_match_inds'

    Examples
    ________
    data_inds =      np.asarray([12, 11, 13, 14, 15,      17])
    match_set_inds = np.asarray([11, 12,     14, 15, 16,  17,  18,  19,  20])
    data = np.asarray([9,8,2,3,4,7,5,6,4,5,6,7,8,9,92,1,1,56,33,44,55,66,77])

    out = utils.intersect_data_with_nans(data_inds, match_set_inds, data=None)
    print(np.vstack((out, match_set_inds)))

    out = utils.intersect_data_with_nans(match_set_inds, data_inds, data=None)
    print(np.vstack((out, data_inds)))

    data_inds_data = data[data_inds]
    match_set_inds_data = data[match_set_inds]
    out = utils.intersect_data_with_nans(data_inds, match_set_inds, data=data_inds_data)
    print(np.vstack((out, match_set_inds_data)))

    data_inds_data = data[data_inds]
    match_set_inds_data = data[match_set_inds]
    out = utils.intersect_data_with_nans(match_set_inds, data_inds, data=match_set_inds_data)
    print(np.vstack((out, data_inds_data)))

    """
    assert len(src_data_inds) == len(set(src_data_inds)), 'data_inds contains duplicates, this is not allowed'
    assert len(data_to_match_inds) == len(
        set(data_to_match_inds)), 'match_set_inds contains duplicates, this is not allowed'
    if data is None:
        data = src_data_inds
    match_inds = []
    for k in data_to_match_inds:
        if k in src_data_inds and not np.isnan(k):
            x = k == src_data_inds
            match_inds.append(np.where(x)[0][0].astype(float))
        else:
            match_inds.append(np.nan)
    out = index_with_nans(data, match_inds)
    return out


def index_with_nans(x, inds):
    return [np.nan if np.isnan(k) else x[int(k)] for k in inds]


def intersect_with_nans(arr1, arr2):
    a, b, c = np.intersect1d(arr1, arr2, return_indices=True)
    b2 = np.ones_like(arr1) * np.nan
    b2[b] = b
    c2 = np.ones_like(arr2) * np.nan
    c2[c] = c
    return b2, c2


def find_step_onset(x):
    x = np.asarray(x).astype(float)
    x -= np.average(x)
    step = np.hstack((np.ones(len(x)), -1 * np.ones(len(x))))
    dary_step = np.convolve(x, step, mode='valid')
    step_indx = np.argmax(dary_step)
    return step_indx


def getkey(h5_list, key_name=None):
    """
    Parameters
    ----------
    h5_list : list
        list of full paths to H5 file(s).
    key_name : str
        default 'labels', the key to get the data from the H5 file
    """

    h5_list = make_list(h5_list, suppress_warning=True)
    if key_name is None:
        print_h5_keys(h5_list[0])
        return None
    for i, k in enumerate(h5_list):
        with h5py.File(k, 'r') as h:
            try:
                x = h[key_name][:]
            except:
                x = h[key_name]

            if i == 0:
                out = np.asarray(x)
            else:
                out = np.concatenate((out, x))
    return out


def loop_segment_chunks(len_array, chunk_size):
    return loop_segments(chunk_segments(len_array, chunk_size))


def chunk_segments(len_array, chunk_size):
    out = [chunk_size] * (len_array // chunk_size)
    if len_array % chunk_size > 0:
        out.append(len_array % chunk_size)
    return out


def num_chunks(len_array, chunk_size):
    return len_array // chunk_size + 1 * (len_array % chunk_size > 0)


def cut_with_nans(x, inds, start_pad, end_pad=None):
    inds = np.asarray(make_list(inds, True)) + start_pad
    if end_pad is None:
        end_pad = start_pad
    x = np.concatenate((np.ones(start_pad) * np.nan, x, np.ones(end_pad) * np.nan))
    x_out = []
    for k in inds:
        i1 = np.max([0, k - start_pad])
        i2 = k + end_pad + 1
        x_out.append(x[i1:i2])
    return np.asarray(x_out)


def h5_string_switcher(list_in):
    list_in = make_list(list_in)
    print(type(list_in[0]))
    if 'bytes' in str(type(list_in[0])).lower():
        print('DECODE switching from bytes to string')
        out = [k.decode("ascii", "ignore") for k in list_in]
    elif type(list_in[0]) == str:
        print('ENCODE switching from string to bytes')
        out = [k.encode("ascii", "ignore") for k in list_in]
    else:
        print('not bytes or string format, returning input')
        return list_in
    return out


def clear_dir(dir_in):
    rmtree(dir_in)
    make_path(dir_in)


def rmtree(dir_in):
    if os.path.isdir(dir_in):
        shutil.rmtree(dir_in)


def norm_path(path_in, sep=None):
    add_start = ''
    if sep == None:
        sep = os.sep
    if path_in[0] == '/' or path_in[0] == '\\':
        add_start = sep
    tmp_list = '\\'.join([k for k in path_in.split('/') if len(k) > 0])
    final_list = [k for k in tmp_list.split('\\') if len(k) > 0]
    return add_start + sep.join(final_list)


def h5_to_dict(h5_in, exclude_keys=['final_features_2105', 'images', 'FD__original', 'CNN_pred']):
    """

    Parameters
    ----------
    h5_in :
    exclude_keys : by default excludes all the alrge data in the H5 file, set to "[]" to get the entire H5

    Returns
    -------

    """
    d = dict()
    if exclude_keys is None:
        exclude_keys = []
    with h5py.File(h5_in, 'r') as h:
        for k in h.keys():
            if k not in exclude_keys:
                d[k] = h[k][:]
    return d


def smooth(y, window, mode='same'):  # $%
    if window == 1:
        return y
    box = np.ones(window) / window
    y_smooth = np.convolve(y, box, mode=mode)
    return y_smooth


def make_path(name_in):
    Path(name_in).mkdir(parents=True, exist_ok=True)


def sort(x):
    return natsorted(x, alg=ns.FLOAT | ns.UNSIGNED)
    # return natsorted(x, alg=ns.REAL)


def split_list_inds(x, split_ratio):
    split_ratio = split_ratio / np.sum(split_ratio)
    L = len(x)
    mixed_inds = np.random.choice(L, L, replace=False)
    out = np.split(mixed_inds, np.ceil(L * np.cumsum(split_ratio[:-1])).astype('int'))
    return out


def split_list(x, split_ratio):
    inds = split_list_inds(x, split_ratio)
    out = []
    for k in inds:
        tmp1 = []
        for k2 in k:
            tmp1.append(x[k2])
        out.append(tmp1)
    return out


def h5_batch_generator(h5_path, key, batch_size):
    with h5py.File(h5_path, 'r') as hf:
        data_len = hf[key].shape[0]
        for i in range(0, data_len, batch_size):
            yield hf[key][i: i + batch_size]


def predict_on_large_data(h5_path, key, model, batch_size=1000):
    # Create the generator
    gen = h5_batch_generator(h5_path, key, batch_size)

    predictions = []
    for batch in gen:
        pred = model.predict(batch)
        predictions.append(pred)

    return np.concatenate(predictions)

def info(x):
    if isinstance(x, dict):
        print('type is dict')
        get_dict_info(x)
    elif isinstance(x, list):
        try:
            x = copy.deepcopy(np.asarray(x))
            print('type is list, converting a copy to numpy array to print this info')
            np_stats(x)
        except:
            print(
                "type is a list that can't be converted to a numpy array for printing info or maybe data format is not compatible")

    elif type(x).__module__ == np.__name__:
        print('type is np array')
        np_stats(x)
    else:
        try:
            print('type is ' + str(type(x)) + ' will try printing using "get_class_info2" ')
            get_class_info2(x)
        except:
            print('cant find out what to do with input of type')
            print(type(x))


def get_time_string(time_zone_string='America/Los_Angeles'):
    tz = pytz.timezone(time_zone_string)
    loc_dt = pytz.utc.localize(datetime.utcnow())
    current_time = loc_dt.astimezone(tz)
    todays_version = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    return todays_version



def _check_pkl(name):
    if name[-4:] != '.pkl':
        return name + '.pkl'
    return name


def save_obj(obj, name, protocol=4):
    with open(_check_pkl(name), 'wb') as f:
        # pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(obj, f, protocol=protocol)


def load_obj(name):
    with open(_check_pkl(name), 'rb') as f:
        return pickle.load(f)

def get_nillip_path():
    path = os.path.dirname(nillip.__file__)
    return path

def isnotebook():
    try:
        c = str(get_ipython().__class__)
        shell = get_ipython().__class__.__name__
        if 'colab' in c:
            return True
        elif shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def four_class_labels_from_binary(x):
    '''
    for time series onset off set with lag images
    '''
    a = np.asarray(x)
    b = np.asarray([0] + list(np.diff(a)))
    c = a + b
    c[c == -1] = 3
    return c


def print_h5_keys(h5file, return_list=False, do_print=True):
    with h5py.File(h5file, 'r') as h:
        x = copy.deepcopy(list(h.keys()))
        if do_print:
            print_list_with_inds(x)
        if return_list:
            return x

#! change name here to simply be copy data etc etc... change out the label naming 
def copy_h5_key_to_another_h5(h5_to_copy_from, h5_to_copy_to, label_string_to_copy_from, label_string_to_copy_to=None):
    """
    copy data to another h5, optionally 

    """
    if label_string_to_copy_to is None:
        label_string_to_copy_to = label_string_to_copy_from
    with h5py.File(h5_to_copy_from, 'r') as h:
        with h5py.File(h5_to_copy_to, 'r+') as h2:
            try:
                h2[label_string_to_copy_to][:] = h[label_string_to_copy_from][:]
            except:
                h2.create_dataset(label_string_to_copy_to, shape=np.shape(h[label_string_to_copy_from][:]),
                                  data=h[label_string_to_copy_from][:])


def lister_it(in_list, keep_strings='', remove_string=None, return_bool_index=False) -> object:
    if len(in_list) == 0:
        print("in_list was empty, returning in_list")
        return in_list

    def index_list_of_strings(in_list2, cmp_string):
        return np.asarray([cmp_string in string for string in in_list2])

    if isinstance(keep_strings, str): keep_strings = [keep_strings]
    if isinstance(remove_string, str): remove_string = [remove_string]

    keep_i = np.asarray([False] * len(in_list))
    for k in keep_strings:
        keep_i = np.vstack((keep_i, index_list_of_strings(in_list, k)))
    keep_i = np.sum(keep_i, axis=0) > 0

    remove_i = np.asarray([True] * len(in_list))
    if remove_string is not None:
        for k in remove_string:
            remove_i = np.vstack((remove_i, np.invert(index_list_of_strings(in_list, k))))
        remove_i = np.product(remove_i, axis=0) > 0

    inds = keep_i * remove_i  # np.invert(remove_i)
    if inds.size <= 0:
        return []
    else:
        out = np.asarray(in_list)[inds]
        if return_bool_index:
            return out, inds
    return out


def get_class_info2(c, sort_by=None, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
    def get_len_or_shape(x_in):
        which_one = None
        try:
            len_or_shape_out = str(len(x_in))
            which_one = 'length'
            if type(x_in).__module__ == np.__name__:
                len_or_shape_out = str(x_in.shape)
                which_one = 'shape '
        except:
            if which_one is None:
                len_or_shape_out = 'None'
                which_one = 'None  '
        return len_or_shape_out, which_one

    names = []
    len_or_shape = []
    len_or_shape_which_one = []
    type_to_print = []

    for k in dir(c):
        if include_underscore_vars is False and k[0] != '_':

            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
        elif include_underscore_vars:
            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    len_space_shape = ' ' * max(len(k) for k in len_or_shape)
    if sort_by is None:
        ind_array = np.arange(len(names))
    elif 'type' in sort_by.lower():
        ind_array = np.argsort(type_to_print)
    elif 'len' in sort_by.lower() or 'shape' in sort_by.lower():
        np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
        tmp1 = np.asarray([eval(k) for k in len_or_shape])
        tmp1[tmp1 == None] = np.nan
        tmp1 = [np.max(iii) for iii in tmp1]
        ind_array = np.argsort(tmp1)
    elif 'name' in sort_by.lower():
        ind_array = np.argsort(names)
    else:
        ind_array = np.arange(len(names))

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        k5 = len_or_shape[i]
        x = eval('c.' + names[i])
        k3 = str(x)
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]
        k5 = (k5 + len_space_shape)[:len(len_space_shape)]
        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]
        print(k1 + ' type->   ' + k2 + '  ' + len_or_shape_which_one[i] + '->   ' + k5 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print


def get_class_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
    def get_len_or_shape(x_in):
        which_one = None
        try:
            len_or_shape_out = str(len(x_in))
            which_one = 'length'
            if type(x_in).__module__ == np.__name__:
                len_or_shape_out = str(x_in.shape)
                which_one = 'shape '
        except:
            if which_one is None:
                len_or_shape_out = 'None'
                which_one = 'None  '
        return len_or_shape_out, which_one

    names = []
    len_or_shape = []
    len_or_shape_which_one = []
    type_to_print = []

    for k in dir(c):
        if include_underscore_vars is False and k[0] != '_':

            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
        elif include_underscore_vars:
            tmp1 = str(type(eval('c.' + k)))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(k)
            a, b = get_len_or_shape(eval('c.' + names[-1]))
            len_or_shape.append(a)
            len_or_shape_which_one.append(b)
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    len_space_shape = ' ' * max(len(k) for k in len_or_shape)
    if sort_by_type:
        ind_array = np.argsort(type_to_print)
    else:
        ind_array = np.argsort(names)

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        k5 = len_or_shape[i]
        x = eval('c.' + names[i])
        k3 = str(x)
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]
        k5 = (k5 + len_space_shape)[:len(len_space_shape)]
        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]
        print(k1 + ' type->   ' + k2 + '  ' + len_or_shape_which_one[i] + '->   ' + k5 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print


def get_dict_info(c, sort_by_type=True, include_underscore_vars=False, return_name_and_type=False, end_prev_len=40):
    names = []
    type_to_print = []
    for k in c.keys():
        if include_underscore_vars is False and str(k)[0] != '_':
            tmp1 = str(type(c[k]))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(str(k))
        elif include_underscore_vars:
            tmp1 = str(type(c[k]))
            type_to_print.append(tmp1.split("""'""")[-2])
            names.append(str(k))
    len_space = ' ' * max(len(k) for k in names)
    len_space_type = ' ' * max(len(k) for k in type_to_print)
    if sort_by_type:
        ind_array = np.argsort(type_to_print)
    else:
        ind_array = np.argsort(names)

    for i in ind_array:
        k1 = names[i]
        k2 = type_to_print[i]
        try:
            k3 = str(c[names[i]])
        except:
            k3 = str(c[float(names[i])])
        k1 = (k1 + len_space)[:len(len_space)]
        k2 = (k2 + len_space_type)[:len(len_space_type)]

        if len(k3) > end_prev_len:
            k3 = '...' + k3[-end_prev_len:]
        else:
            k3 = '> ' + k3[-end_prev_len:]

        if 'numpy.ndarray' in k2:
            k4 = str(c[names[i]].shape)
            k4_str = '   shape-> '
        else:
            try:
                k4 = str(len(c[names[i]]))
                k4_str = '   len-> '
            except:
                k4_str = '   None->'
                k4 = 'None'

        print(k1 + ' type->   ' + k2 + k4_str + k4 + '  ' + k3)
    if return_name_and_type:
        return names, type_to_print



def group_consecutives(vals, step=1):  # row # find_in_a_row # putting this here for searching
    """

    Parameters
    ----------
    vals :
        
    step :
         (Default value = 1)

    Returns
    -------

    """
    run = []
    run_ind = []
    result = run
    result_ind = run_ind
    expect = None
    for k, v in enumerate(vals):
        if v == expect:
            if not (np.isnan(v)):
                # print(v)
                # print(expect)
                run.append(v)
                run_ind.append(k)
        else:
            if not (np.isnan(v)):
                run = [v]
                run_ind = [k]
                result.append(run)
                result_ind.append(run_ind)
        expect = v + step
    # print(result)
    if result == []:
        pass
    elif result[0] == []:
        result = result[1:]
        result_ind = result_ind[1:]
    return result, result_ind


# def get_h5s(base_dir, print_h5_list=True):
#     """

#     Parameters
#     ----------
#     base_dir :
        

#     Returns
#     -------

#     """
#     H5_file_list = []
#     for path in Path(base_dir + os.path.sep).rglob('*.h5'):
#         H5_file_list.append(str(path.parent) + os.path.sep + path.name)
#     H5_file_list.sort()
#     if print_h5_list:
#         print_list_with_inds(H5_file_list)
#     return H5_file_list


def check_if_file_lists_match(H5_list_LAB, H5_list_IMG):
    """

    Parameters
    ----------
    H5_list_LAB :
        
    H5_list_IMG :
        

    Returns
    -------

    """
    for h5_LAB, h5_IMG in zip(H5_list_LAB, H5_list_IMG):
        try:
            assert h5_IMG.split(os.path.sep)[-1] in h5_LAB
        except:
            print('DO NOT CONTINUE --- some files do not match on your lists try again')
            assert (1 == 0)
    print('yay they all match!')


def print_list_with_inds(list_in):
    """

    Parameters
    ----------
    list_in :
        

    Returns
    -------

    """
    _ = [print(str(i) + ' ' + k.split(os.path.sep)[-1]) for i, k in enumerate(list_in)]


def get_model_list(model_save_dir):
    """

    Parameters
    ----------
    model_save_dir :
        

    Returns
    -------

    """
    print('These are all the models to choose from...')
    model_2_load_all = glob.glob(model_save_dir + '/*.ckpt')
    print_list_with_inds(model_2_load_all)
    return model_2_load_all


def recursive_dir_finder(base_path, search_term):
    """enter base directory and search term to find all the directories in base directory
      with files matching the search_term. output a sorted list of directories.
      e.g. -> recursive_dir_finder('/content/mydropbox/', '*.mp4')

    Parameters
    ----------
    base_path :
        
    search_term :
        

    Returns
    -------

    """
    matching_folders = []
    for root, dirs, files in os.walk(base_path):
        if glob.glob(root + '/' + search_term):
            matching_folders.append(root)
    try:
        matching_folders = natsorted(matching_folders)
    except:
        matching_folders = sorted(matching_folders)
    return matching_folders




def get_files(base_dir, search_term=''):
    """
base_dir = '/content/gdrive/My Drive/LIGHT_GBM/FEATURE_DATA/'
num_folders_deep = 1
file_list = []
for i, path in enumerate(Path(base_dir + os.sep).rglob('')):
  x = str(path.parent) + os.path.sep + path.name
  if i ==0:
    file_list.append(x)
    cnt = len(x.split(os.sep))
  if (len(x.split(os.sep))-cnt)<=num_folders_deep:
    file_list.append(x)
list(set(file_list))

    Parameters
    ----------
    base_dir :
        
    search_term :

    Returns
    -------

    """
    file_list = []
    for path in Path(base_dir + os.sep).rglob(search_term):
        ##### can I edit this with default depth of one and only look x num folders deep to prevent long searchs in main folders?
        file_list.append(str(path.parent) + os.path.sep + path.name)
    file_list.sort()
    return file_list


'''
these below 3 function used to load mat files into dict easily was found and copied directly from 
https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries
and contributed by user -mergen 

to the best of my knowledge code found on stackoverflow is under the creative commons license and as such is legal to 
use in my package. contact phillip.maire@gmail.com if you have any questions. 
'''


def loadmat(filename):
    """this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects

    if this doesnt work try this
    import mat73
    from nillip import utils
    mat_file = '/Users/phil/Dropbox/U_191028_1154.mat'
    data_dict = mat73.loadmat(mat_file)

    Parameters
    ----------
    filename :
        

    Returns
    -------

    """
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


def _check_keys(dict):
    """checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries

    Parameters
    ----------
    dict :
        

    Returns
    -------

    """
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict


def _todict(matobj):
    """A recursive function which constructs from matobjects nested dictionaries

    Parameters
    ----------
    matobj :
        

    Returns
    -------

    """
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


def get_inds_of_inds(a, return_unique_list=False):
    a2 = []
    for k in a:
        a2.append(list(np.where([k == kk for kk in a])[0]))
    try:
        inds_of_inds = list(np.unique(a2, axis=0))
        for i, k in enumerate(inds_of_inds):
            inds_of_inds[i] = list(k)
    except:
        inds_of_inds = list(np.unique(a2))
    if return_unique_list:
        return inds_of_inds, pd.unique(a)
    else:
        return inds_of_inds

#! better naming
def inds_around_inds(x, N):
    """

    Parameters
    ----------
    x : array
    N : window size

    Returns
    -------
    returns indices of arrays where array >0 with borders of ((N - 1) / 2), so x = [0, 0, 0, 1, 0, 0, 0] and N = 3
    returns [2, 3, 4]
    """
    assert N / 2 != round(N / 2), 'N must be an odd number so that there are equal number of points on each side'
    cumsum = np.cumsum(np.insert(x, 0, 0))
    a = (cumsum[N:] - cumsum[:-N]) / float(N)
    a = np.where(a > 0)[0] + ((N - 1) / 2)
    return a.astype('int')


def loop_segments(frame_num_array, returnaslist=False):
    """

    Parameters
    ----------
    frame_num_array :
    num of frames in each trial in a list
    Returns
    -------
    2 lists with the proper index for pulling those trials out one by one in a for loop
    Examples
    ________
    a3 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    frame_num_array = [4, 5]
    for i1, i2 in loop_segments(frame_num_array):
        print(a3[i1:i2])

    # >>>[0, 1, 2, 3]
    # >>>[4, 5, 6, 7, 8]
    """
    frame_num_array = list(frame_num_array)
    frame_num_array = [0] + frame_num_array
    frame_num_array = np.cumsum(frame_num_array)
    frame_num_array = frame_num_array.astype(int)
    if returnaslist:
        return [list(frame_num_array[:-1]), list(frame_num_array[1:])]
    else:
        return zip(list(frame_num_array[:-1]), list(frame_num_array[1:]))

def get_time_it(txt):
    """
  Example
  -------
  import re
  import matplotlib.pyplot as plt
  for k in range(8):
    S = 'test '*10**k
    s2 = 'test'
    %time [m.start() for m in re.finditer(S2, S)]

  # then copy it into a string like below

  txt = '''
  CPU times: user 0 ns, sys: 9.05 ms, total: 9.05 ms
  Wall time: 9.01 ms
  CPU times: user 12 µs, sys: 1 µs, total: 13 µs
  Wall time: 15.7 µs
  CPU times: user 48 µs, sys: 3 µs, total: 51 µs
  Wall time: 56.3 µs
  CPU times: user 281 µs, sys: 0 ns, total: 281 µs
  Wall time: 287 µs
  CPU times: user 2.42 ms, sys: 0 ns, total: 2.42 ms
  Wall time: 2.43 ms
  CPU times: user 21.8 ms, sys: 22 µs, total: 21.8 ms
  Wall time: 21.2 ms
  CPU times: user 198 ms, sys: 21.5 ms, total: 219 ms
  Wall time: 214 ms
  CPU times: user 1.83 s, sys: 191 ms, total: 2.02 s
  Wall time: 2.02 s
  '''
  data = get_time_it(txt)
  ax = plt.plot(data[1:])
  plt.yscale('log')
  """
    vars = [k.split('\n')[0] for k in txt.split('Wall time: ')[1:]]
    a = dict()
    a['s'] = 10 ** 0
    a['ms'] = 10 ** -3
    a['µs'] = 10 ** -6
    data = []
    for k in vars:
        units = k.split(' ')[-1]
        data.append(float(k.split(' ')[0]) * a[units])
    return data



def diff_lag_h5_maker(f3):
    """
    need to use the stack_lag_h5_maker first and then send a copy of that into this one again these program are only a temp
    solution, if we use these methods for the main model then I will make using them more fluid and not depend on one another
    Parameters
    ----------
    f3 : the file from stack_lag_h5_maker output

    Returns
    -------
    """
    # change color channel 0 and 1 to diff images from color channel 3 so color channels 0, 1, and 2 are 0-2, 1-2, and 2
    with h5py.File(f3, 'r+') as h:
        for i in tqdm(range(h['images'].shape[0])):
            k = copy.deepcopy(h['images'][i])
            for img_i in range(2):
                k = k.astype(float)
                a = k[:, :, img_i] - k[:, :, -1]
                a = ((a + 255) / 2).astype(np.uint8)
                h['images'][i, :, :, img_i] = a




    # copy over the other info from the OG h5 file
    copy_over_all_non_image_keys(f, f2)
    # copy_h5_key_to_another_h5(f, f2, 'labels', 'labels')
    # copy_h5_key_to_another_h5(f, f2, 'frame_nums', 'frame_nums')


def force_write_to_h5(h5_file, data, data_name):
    with h5py.File(h5_file, 'r+') as h:
        try:
            h.create_dataset(data_name, data=data)
        except:
            del h[data_name]
            h.create_dataset(data_name, data=data)

def intersect_lists(d):
    return list(set(d[0]).intersection(*d))



def add_to_h5(h5_file, key, values, overwrite_if_exists=False):
    all_keys = print_h5_keys(h5_file, return_list=True, do_print=False)
    with h5py.File(h5_file, 'r+') as h:
        if key in all_keys and overwrite_if_exists:
            print('key already exists, overwriting value...')
            del h[key]
            h.create_dataset(key, data=values)
        elif key in all_keys and not overwrite_if_exists:
            print("""key already exists, NOT overwriting value..., \nset 'overwrite_if_exists' to True to overwrite""")
        else:
            h.create_dataset(key, data=values)



def update_nillip():
    # filename = get_nillip_path() + os.sep + '/nillip_data/final_model/final_resnet50V2_full_model.zip'
    # dst = filename[:-4]
    # if os.path.isdir(dst):
    #     shutil.rmtree(dst)
    #     print('waiting 10 seconds to allow model to delete')
    # time.sleep(10)

    x = '''python3 "/Users/phil/Dropbox/UPDATE_nillip_PYPI.py"'''
    out = os.popen(x).read()
    print(out)
    # print(
    #     'please refer to the open terminal window for further details\nrerun utils.download_resnet_model() to put the model file back')


def make_list(x, suppress_warning=False):
    if not isinstance(x, list):
        if not suppress_warning:
            print("""input is supposed to be a list, converting it but user should do this to suppress this warning""")
        if type(x) is np.str_:
            x2 = [x]
        # elif type(x) is np.str_:
        #     pass
        elif 'array' in str(type(x)).lower():
            x2 = list(x)
        elif type(x).__module__ == np.__name__:
            print(type(x))
            assert False, '''see module nillip.utils.make_list, we have not official protocol for this input type ''' + str(
                type(x))
        elif isinstance(x, str):
            x2 = [x]
        else:
            x2 = [x]
        return x2
    else:
        return x


def search_sequence_numpy(arr, seq, return_type='indices'):
    Na, Nseq = arr.size, seq.size
    r_seq = np.arange(Nseq)
    M = (arr[np.arange(Na - Nseq + 1)[:, None] + r_seq] == seq).all(1)

    if return_type == 'indices':
        return np.where(M)[0]
    elif return_type == 'bool':
        return M




def assert_path(str_in):
    if os.path.isfile(str_in):
        str_in = os.path.dirname(str_in)
    elif os.path.isdir(str_in):
        pass
    else:
        assert False, 'this is not a path or a file'
    return str_in


def open_folder(path):
    path = assert_path(path)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def medfilt_confidence_scores(pred_bool_in, kernel_size_in):
    if pred_bool_in.shape[1] == 1:
        pred_bool_out = medfilt(copy.deepcopy(pred_bool_in), kernel_size=kernel_size_in)
    else:
        pred_bool_out = medfilt2d(copy.deepcopy(pred_bool_in), kernel_size=[kernel_size_in, 1])
    return pred_bool_out



def copy_folder_structure(src, dst):
    src = os.path.abspath(src)
    src_prefix = len(src) + len(os.path.sep)
    Path(dst).mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(src):
        for dirname in dirs:
            dirpath = os.path.join(dst, root[src_prefix:], dirname)
            Path(dirpath).mkdir(parents=True, exist_ok=True)


def copy_file_filter(src, dst, keep_strings='', remove_string=None, overwrite=False,
                     just_print_what_will_be_copied=False, disable_tqdm=False, return_list_of_files=False):
    """

    Parameters
    ----------
    return_list_of_files :
    src : source folder
    dst : destination folder
    keep_strings : see utils.lister_it, list of strings to match in order to copy
    remove_string : see utils.lister_it, list of strings to match in order to not copy
    overwrite : will overwrite files if true
    just_print_what_will_be_copied : can just print what will be copied to be sure it is correct
    disable_tqdm : if True it will prevent the TQDM loading bar

    Examples
    ________
    copy_file_filter('/Users/phil/Desktop/FAKE_full_data', '/Users/phil/Desktop/aaaaaaaaaa', keep_strings='/3lag/',
                 remove_string=None, overwrite=True, just_print_what_will_be_copied=False)
    Returns
    -------

    """
    src = src.rstrip(os.sep) + os.sep
    dst = dst.rstrip(os.sep) + os.sep

    all_files_and_dirs = get_files(src, search_term='*')
    to_copy = lister_it(all_files_and_dirs, keep_strings=keep_strings, remove_string=remove_string)

    if just_print_what_will_be_copied:
        _ = [print(str(i) + ' ' + k) for i, k in enumerate(to_copy)]
        if return_list_of_files:
            return to_copy, None
        else:
            return

    to_copy2 = []  # this is so I can tqdm the files and not the folders which would screw with the average copy time.
    for k in to_copy:
        k2 = dst.join(k.split(src))
        if os.path.isdir(k):
            Path(k2).mkdir(parents=True, exist_ok=True)
        else:
            to_copy2.append(k)
    final_copied = []
    for k in tqdm(to_copy2, disable=disable_tqdm):
        k2 = dst.join(k.split(src))
        final_copied.append(k2)
        if overwrite or not os.path.isfile(k2):
            if os.path.isfile(k2):
                os.remove(k2)
            Path(os.path.dirname(k2)).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(k, k2)
        elif not overwrite:
            print('overwrite = False: file exists, skipping--> ' + k2)
    if return_list_of_files:
        return to_copy2, final_copied


def np_stats(in_arr):
    print('\nmin', np.min(in_arr))
    print('max', np.max(in_arr))
    print('mean', np.mean(in_arr))
    print('shape', in_arr.shape)
    print('len of unique', len(np.unique(in_arr)))
    print('type', type(in_arr))
    try:
        print('Dtype ', in_arr.dtype)
    except:
        pass


def h5_key_exists(h5_in, key_in):
    return key_in in print_h5_keys(h5_in, return_list=True, do_print=False)


def del_h5_key(h5_in, key_in):
    if h5_key_exists(h5_in, key_in):
        with h5py.File(h5_in, 'r+') as h:
            del h[key_in]


def overwrite_h5_key(h5_in, key_in, new_data=None):
    exist_test = h5_key_exists(h5_in, key_in)
    with h5py.File(h5_in, 'r+') as h:
        if exist_test:
            del h[key_in]
        if new_data is not None:
            h[key_in] = new_data


def convert_list_of_strings_for_h5(list_in):
    return [n.encode("ascii", "ignore") for n in list_in]


def intersect_all(arr1, arr2):
    """retun inndex of length len(arr1) instead of numpys length min([len(arr1), len(arr2)])"""
    return [{v: i for i, v in enumerate(arr2)}[v] for v in arr1]


def assert_min_hd_space(path, min_gb=2):
    assert shutil.disk_usage(
        path).free / 10 ** 9 > min_gb, """assert_min_hd_space function: GB limit reached, ending function"""

