import requests
import json
import os
from singleton_decorator import singleton
from utils.util import get_video_name_from_frame, get_frame_number, check_if_image

BASEURL = "http://scanpix-server:5001/process_image"


def append_to_json(filepath, data):
    # if file is empty dump to empty file and return
    if (os.stat(filepath).st_size == 0):
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump([data], f)
        return

    # construct JSON fragment as new file ending
    new_ending = ", " + json.dumps(data)[0:-1] + "}]"

    # edit the file in situ - first open it in read/write mode
    with open(filepath, 'r+') as f:

        f.seek(0, 2)  # move to end of file
        index = f.tell()  # find index of last byte

        # walking back from the end of file, find the index
        # of the original JSON List's closing ']'
        while not f.read().startswith(']'):
            index -= 1
            if index == 0:
                raise ValueError("can't find JSON object in {!r}".format(filepath))
            f.seek(index)

        # starting at the original ending ] position, write out
        # the new ending
        f.seek(index)
        f.write(new_ending)


@singleton
class Indexer:

    def index(self, img_name, img_path):
        import re
        img_path = re.sub("worker-app", "scanpix", img_path)
        res = requests.get(url=BASEURL, params={'url': img_path}).json()
        res['file_name'] = get_video_name_from_frame(img_name, "/scanpix/data/videos")
        res['frame_number'] = get_frame_number(img_name, "/scanpix/data/videos")
        res['type'] = "image" if check_if_image(res["file_name"]) else "video"
        print(f"indexed {img_name}!")
        return res

    def dump_to_json(self, json_index):
        append_to_json("/worker-app/data/db/index.json", json_index)
        print("Dumped to index.json!")

    def remove_from_json(self, file_name):
        with open("/worker-app/data/db/index.json", "r") as f:
            raw_data = f.read()
        index_list = json.loads(raw_data)

        index_list = list(filter(lambda x: x["file_name"] != file_name, index_list))
        with open("/worker-app/data/db/index.json", "w", encoding="utf-8") as f:
            json.dump(index_list, f, indent=4)
        print(f"removed {file_name} from json")
