import re
import os


def check_if_image(file_name):
    pat = ".*\.(.*)"
    m = re.search(pat, file_name)
    extensions = set(["jpg", "jpeg", "png"])
    if (m.group(1) in extensions):
        return True
    return False


'''function to extract filename from path'''


def extract_filename(path):
    m = re.search(".*/(.*)", path)
    return m.group(1)


def check_if_image_in_index(index_list, file_name):
    for index in index_list:
        if (index["file_name"] == file_name):
            return True
    return False


def get_video_name_from_frame(name, video_path):
    if "_frame_" in name:
        video_name = re.search("(.*)_frame_.*", name)[1]
        if video_name:
            return video_name
    return name


def get_frame_number(name, video_path):
    if "_frame_" in name:
        frame_number = re.search(".*_frame_(.*)\.", name)[1]
        video_name = re.search("(.*)_frame_.*", name)[1]
        if video_name:
            return frame_number
    return -1


# FPS calculated approximately by tallying total duration of a video with the number of frames generated
APPROX_FPS = 1.2


def get_timestamp(frame_number, fps):
    from math import floor
    seconds = floor(int(frame_number) * 25 // 30)
    return seconds
