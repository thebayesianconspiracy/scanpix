import requests
import json
import tqdm
import os

BASEURL = "http://0.0.0.0:5001/process_image"
IMG_PATH = "../data/images/"
imgs = [x for x in os.listdir(IMG_PATH) if x.split('.')[-1] in ['jpg', 'png', 'jpeg']]
img_index = []
for img in tqdm(imgs):
    res = requests.get(url=f"{BASEURL}", params={'url': f"{IMG_PATH}/{img}"}).json()
    res['file_name'] = img
    img_index.append(res)

OUTPUT_PATH = "../data/"
with open(f'{OUTPUT_PATH}/index.json', 'w', encoding='utf-8') as f:
    json.dump(img_index, f, indent=4)
