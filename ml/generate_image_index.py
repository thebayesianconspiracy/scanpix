import re

import requests
import json
from tqdm import tqdm
import os

BASEURL = "http://0.0.0.0:5001/process_image"
IMG_PATH = "../data/images"
FRAMES_PATH = "../data/videos/frames"
imgs = [x for x in os.listdir(IMG_PATH) if x.split('.')[-1] in ['jpg', 'png', 'jpeg']]
frames = [x for x in os.listdir(FRAMES_PATH) if x.split('.')[-1] in ['jpg', 'png', 'jpeg']]

img_index = []
for img in tqdm(imgs):
    res = requests.get(url=f"{BASEURL}", params={'url': f"/scanpix/data/images/{img}"}).json()
    res['file_name'] = img
    res['type'] = "image"
    img_index.append(res)

for img in tqdm(frames):
    res = requests.get(url=f"{BASEURL}", params={'url': f"/scanpix/data/videos/frames/{img}"}).json()
    video_name = re.search("(.*)_frame_.*", img)[1]
    res['file_name'] = video_name
    res['type'] = "video"
    frame_number = re.search(".*_frame_(.*)\.", img)[1]
    if frame_number:
        res["frame_number"] = frame_number
    img_index.append(res)

OUTPUT_PATH = "../data/db/"
with open(f'{OUTPUT_PATH}/index.json', 'w', encoding='utf-8') as f:
    json.dump(img_index, f, indent=4)

# with open("../data/db/index.json", "r") as f:
#     raw_data = f.read()
# IMAGE_INDEX = json.loads(raw_data)
#
# for i in range(len(IMAGE_INDEX)):
#     IMAGE_INDEX[i]["type"] = "image"
#
# with open("../data/db/index.json", "w", encoding="utf-8") as f:
#     json.dump(IMAGE_INDEX, f, indent=4)
