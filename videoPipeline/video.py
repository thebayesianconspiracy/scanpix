import cv2
import re
import os

FRAMES_PATH = "../data/videos/frames"
VIDEOS_PATH = "../data/videos"
MAX_FPS = 10
FRAME_SKIP = 25 // MAX_FPS


class Video:
    def __init__(self, path_to_video):
        self.name = re.search(".*/(.*)\.", path_to_video)[1]
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

        print(f'Finished breaking into {current_frame // FRAME_SKIP - 1} frames!')


def check_if_frames_exist(name):
    if name + '_frame_1.jpg' in os.listdir(FRAMES_PATH):
        return True
    return False


def videos_to_frames():
    print("Starting video to frames conversion!")
    for vid in os.listdir(VIDEOS_PATH):
        video_object = Video(vid)
        if not check_if_frames_exist(video_object.name):
            video_object.break_into_frames()
    print("Completed breaking down all videos!")
