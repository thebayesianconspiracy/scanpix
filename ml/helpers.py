import requests
import os
from PIL import Image


def get_image_from_url(url):
    return Image.open(requests.get(url, stream=True).raw) if 'http' in url else Image.open(url)


'''function to watermark play button on the thumbnails'''


def watermark_thumbnails():
    THUMBNAILS_PATH = "/scanpix/data/videos/thumbnails/"
    watermark_image_path = f"{THUMBNAILS_PATH}play-button-icon.png"
    for base_image_path in os.listdir(THUMBNAILS_PATH):
        if base_image_path not in [".DS_Store", "play-button-icon.png"] and not base_image_path.startswith("watermarked"):
            base_image = Image.open(f"{THUMBNAILS_PATH}{base_image_path}").convert("RGBA")
            watermark = Image.open(watermark_image_path).convert("RGBA")
            width, height = base_image.size
            width_watermark, height_watermark = (width // 4, height // 4)
            watermark = watermark.resize((width // 4, height // 4))
            transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            transparent.paste(base_image, (0, 0))
            transparent.paste(watermark, (width // 2 - width_watermark // 2, height // 2 - height_watermark // 2), mask=watermark)
            transparent.show()
            transparent.save(f"{THUMBNAILS_PATH}watermarked_" + base_image_path)
