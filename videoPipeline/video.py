import cv2
import re
import os
from PIL import Image

FRAMES_PATH = "../data/videos/frames"
VIDEOS_PATH = "../data/videos"
MAX_FPS = 1
FRAME_SKIP = 25 // MAX_FPS


'''function to watermark play button on the thumbnails'''
def watermark_thumbnails():
    FRAMES_PATH = "../data/videos/frames/"
    THUMBNAILS_PATH = "../data/videos/thumbnails/"
    watermark_image_path = f"{THUMBNAILS_PATH}play-button-icon.png"
    for base_image_path in os.listdir(FRAMES_PATH):
        if base_image_path.endswith("_frame_1.jpg"):
            if base_image_path not in [".DS_Store", "play-button-icon.png"] and not base_image_path.startswith("watermarked"):
                base_image = Image.open(f"{FRAMES_PATH}{base_image_path}").convert("RGBA")
                watermark = Image.open(watermark_image_path).convert("RGBA")
                width, height = base_image.size
                width_watermark, height_watermark = (width // 4, height // 4)
                watermark = watermark.resize((width // 4, height // 4))
                transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
                transparent.paste(base_image, (0, 0))
                transparent.paste(watermark, (width // 2 - width_watermark // 2, height // 2 - height_watermark // 2), mask=watermark)
                transparent.show()
                transparent.save(f"{THUMBNAILS_PATH}watermarked_" + base_image_path)

class Video:
    def __init__(self, path_to_video):
        self.name = re.search(".*/(.*)", path_to_video)[1]
        self.path = str(path_to_video)

    def break_into_frames(self):
        print(f"Breaking {self.name} into frames!")

        capture = cv2.VideoCapture(self.path)
        path_to_save = os.path.abspath(FRAMES_PATH)
        current_frame = 1

        if not capture.isOpened():
            print('Capture is not open')

        while capture.isOpened():
            ret, frame = capture.read()
            if ret:
                if current_frame % FRAME_SKIP == 0:
                    name = self.name + '_frame_' + str(current_frame // FRAME_SKIP) + '.jpg'
                    print(f'Creating: {name}')
                    cv2.imwrite(os.path.join(path_to_save, name), frame)
                current_frame += 1
            else:
                break
        capture.release()
        cv2.destroyAllWindows()

        print(f'Finished breaking into {current_frame // FRAME_SKIP - 1} frames!')


def check_if_frames_exist(name):
    if name + '_frame_1.jpg' in os.listdir(FRAMES_PATH):
        return True
    return False


def videos_to_frames():
    print("Starting video to frames conversion!")
    for vid in os.listdir(VIDEOS_PATH):
        if os.path.isfile("../data/videos/"+vid) and vid != ".DS_Store":
            video_object = Video("../data/videos/" + vid)
            if not check_if_frames_exist(video_object.name):
                video_object.break_into_frames()
    print("Completed breaking down all videos!")
    watermark_thumbnails()


videos_to_frames()
