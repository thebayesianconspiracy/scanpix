import os

from utils.util import is_docker


project_root = os.path.dirname(os.path.dirname(__file__))
BASEURL = "http://scanpix:5001/process_image" if is_docker() else "http://0.0.0.0:5001/process_image"
data_dir = "/worker-app/data" if is_docker() else f"{project_root}/data"
image_directories = [data_dir + "/images", data_dir + "/user-images"]