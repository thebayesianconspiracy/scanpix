import os
import re


def check_if_image(file_name):
    pat = ".*\.(.*)"
    m = re.search(pat, file_name)
    extensions = set(["jpg", "jpeg", "png"])
    if m.group(1) in extensions:
        return True
    return False


'''function to extract filename from path'''


def extract_filename(path):
    m = re.search(".*/(.*)", path)
    return m.group(1)


def check_if_image_in_index(index_list, file_name):
    for index in index_list:
        if index["file_name"] == file_name:
            return True
    return False


def is_docker():
    path = '/proc/self/cgroup'
    return (
            os.path.exists('/.dockerenv') or
            os.path.isfile(path) and any('docker' in line for line in open(path))
    )
