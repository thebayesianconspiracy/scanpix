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


'''initializing Indexer releated classes'''
indexer_metadata = Indexer_Metadata()
indexer = Indexer()


def write_to_progress_bar():
    payload = str(indexer_metadata.images_indexed) + '_' + str(indexer_metadata.images_total)
    send_payload(payload)


''' function to index all exisiting files not included in index.json initially'''


def index_unwatched_files():
    print("indexing unwatched files....")
    indexer = Indexer()
    with open("/worker-app/data/db/index.json") as f:
        raw_data = f.read()
    index_list = json.loads(raw_data)

    directory_iterator = os.listdir("/worker-app/data/images")
    indexer_metadata.add_images_total_count(len(directory_iterator))
    indexer_metadata.add_images_indexed_count(len(index_list))
    write_to_progress_bar()

    for file_name in directory_iterator:
        if (check_if_image(file_name) and (not check_if_image_in_index(index_list, file_name))):
            json_res = indexer.index(file_name, f"/worker-app/data/images/{file_name}")
            indexer.dump_to_json(json_res)
            indexer_metadata.add_images_indexed_count(1)
            write_to_progress_bar()


''' watcher class to monitor directories '''


class Watcher:

    def __init__(self, directories=["."], handler=FileSystemEventHandler(), recursive=False):
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


'''Custom Handler class to handle events retured by the watcher'''


class WatchHandler(FileSystemEventHandler):

    def on_created(self, event):
        file_name = extract_filename(event.src_path)
        print(f"{file_name} created event!")
        indexer_metadata.add_images_total_count(1)
        write_to_progress_bar()
        if (check_if_image(file_name)):
            json_res = indexer.index(file_name, event.src_path)
            indexer.dump_to_json(json_res)
            indexer_metadata.add_images_indexed_count(1)
            write_to_progress_bar()
        else:
            raise Exception("Invalid type of file, cannot be indexed!")

    def on_deleted(self, event):
        file_name = extract_filename(event.src_path)
        print(f"{file_name} delete event!")
        if (check_if_image(file_name)):
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
    socket_io.connect("http://scanpix:5001")
    index_unwatched_files()
    paths = ["/worker-app/data/images"]
    w = Watcher(paths, WatchHandler(), True)
    w.run()
