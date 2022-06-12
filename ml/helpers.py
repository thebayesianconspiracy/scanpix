import requests
from PIL import Image


def get_image_from_url(url):
    return Image.open(requests.get(url, stream=True).raw) if 'http' in url else Image.open(url)
