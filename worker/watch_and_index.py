import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from singleton_decorator import singleton
from utils.util import *
from index_image import *
import socketio

''' indexer metadata class'''


@singleton
class Indexer_Metadata:
    def __init__(self):
        self.images_indexed = 0
        self.images_total = 0

    def add_images_indexed_count(self, count):
        self.images_indexed += count

    def add_images_total_count(self, count):
        self.images_total += count


'''initializing Indexer related classes'''
indexer_metadata = Indexer_Metadata()
indexer = Indexer()


def write_to_progress_bar():
    payload = str(indexer_metadata.images_indexed) + '_' + str(indexer_metadata.images_total)
    send_payload(payload)


def update_index_json(image_root_path, image_name, index_list):
    if check_if_image(image_name) and (not check_if_image_in_index(index_list, image_name)):
        json_res = indexer.index(image_name, f"{image_root_path}/{image_name}")
        indexer.dump_to_json(json_res)
        indexer_metadata.add_images_indexed_count(1)
        write_to_progress_bar()


''' function to index all existing files not included in index.json initially'''


def index_unwatched_files():
    print("indexing unwatched files....")
    with open("/worker-app/data/db/index.json") as f:
        raw_data = f.read()
    index_list = json.loads(raw_data)

    image_directory_iterator = os.listdir("/worker-app/data/images")
    video_frames_directory_iterator = os.listdir("/worker-app/data/videos/frames")
    indexer_metadata.add_images_total_count(len(image_directory_iterator) + len(video_frames_directory_iterator))
    indexer_metadata.add_images_indexed_count(len(index_list))
    write_to_progress_bar()

    images_root_path = "/worker-app/data/images"
    frames_root_path = "/worker-app/data/videos/frames"

    # indexing images
    for image_name in image_directory_iterator:
        update_index_json(images_root_path, image_name, index_list)

    # indexing frames
    for frame_name in video_frames_directory_iterator:
        update_index_json(frames_root_path, frame_name, index_list)


''' watcher class to monitor directories '''


class Watcher:

    def __init__(self, directories=None, handler=FileSystemEventHandler(), recursive=False):
        if directories is None:
            directories = ["."]
        self.observer = Observer()
        self.handler = handler
        self.directories = directories
        self.recursive = recursive

    # watcher starts monitoring the directory
    def run(self):
        print("directories => ", self.directories)
        self.observer.schedule(self.handler, self.directories[0], self.recursive)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directories[0]))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


'''Custom Handler class to handle events returned by the watcher'''


class WatchHandler(FileSystemEventHandler):

    def on_created(self, event):
        file_name = extract_filename(event.src_path)
        print(f"{file_name} created event!")
        indexer_metadata.add_images_total_count(1)
        write_to_progress_bar()
        if check_if_image(file_name):
            json_res = indexer.index(file_name, event.src_path)
            indexer.dump_to_json(json_res)
            indexer_metadata.add_images_indexed_count(1)
            write_to_progress_bar()
        else:
            raise Exception("Invalid type of file, cannot be indexed!")

    def on_deleted(self, event):
        file_name = extract_filename(event.src_path)
        print(f"{file_name} delete event!")
        if check_if_image(file_name):
            indexer.remove_from_json(file_name)
            indexer_metadata.add_images_total_count(-1)
            indexer_metadata.add_images_indexed_count(-1)
            write_to_progress_bar()
        else:
            raise Exception("Invalid type of file, cannot be deleted from index.json!")


'''SocketIO Client related functions'''
socket_io = socketio.Client()


@socket_io.event
def connect():
    print('connection established')


@socket_io.event
def send_payload(data):
    print(f"emitting data => {data} to server...")
    socket_io.emit('indexer_progress_event', data)


@socket_io.event
def disconnect():
    print('disconnected from server')


if __name__ == "__main__":
    socket_io.connect("http://scanpix-server:5001")
    index_unwatched_files()
    paths = ["/worker-app/data/images"]
    w = Watcher(paths, WatchHandler(), True)
    w.run()
