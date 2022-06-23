import requests
import json


BASEURL = "http://0.0.0.0:5001/process_image"
IMAGE_PATH = "../data/images"


class Indexer:

    def index(self, img_name):
        res = requests.get(url=BASEURL, params={'url': f"{IMAGE_PATH}/{img_name}"})
        print(f"response: {res}")
        #res['file_name'] = img_name
        #res['file_location'] = f"{IMAGE_PATH}/{img_name}"
        return res

    def dump_to_json(self, json_index):
        with open("../data/index.json", "a", encoding='utf-8') as f:
            json.dump(json_index, f, indent=4)
