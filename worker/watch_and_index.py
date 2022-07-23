import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import os

from index_image import *
from utils.util import *

''' function to index all exisiting files not included in index.json initially'''
def index_unwatched_files():
    print("indexing unwatched files....")
    indexer = Indexer()
    with open("/worker-app/data/db/index.json") as f:
        raw_data = f.read()
    index_list = json.loads(raw_data)

    for file_name in os.listdir("/worker-app/data/images"):
        if(check_if_image(file_name) and (not check_if_image_in_index(index_list, file_name))):
            json_res = indexer.index(file_name,f"/worker-app/data/images/{file_name}")
            indexer.dump_to_json(json_res)

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
class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        file_name = extract_filename(event.src_path)
        indexer = Indexer()
        print(f"{file_name} created event!")
        if(check_if_image(file_name)):
            json_res = indexer.index(file_name, event.src_path)
            indexer.dump_to_json(json_res)
        else:
            raise Exception("Invalid type of file, cannot be indexed!")

    def on_deleted(self, event):
        file_name = extract_filename(event.src_path)
        indexer = Indexer()
        print(f"{file_name} delete event!")
        if(check_if_image(file_name)):
            indexer.remove_from_json(file_name)
        else:
            raise Exception("Invalid type of file, cannot be deleted from index.json!")

if __name__ == "__main__":
    index_unwatched_files()
    paths  = ["/worker-app/data/images"]
    w = Watcher(paths, MyHandler(), True)
    w.run()
