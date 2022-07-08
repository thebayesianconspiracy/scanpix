import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

from index_image import *

''' watcher class to monitor directories '''
class Watcher:

    def __init__(self, directories=".", handler=FileSystemEventHandler(), recursive=False):
        self.observer = Observer()
        self.handler = handler
        self.directories = directories
        self.recursive = recursive

    # watcher starts monitoring the directory
    def run(self):
        print("directories => ", self.directories)
        for directory in self.directories:
            self.observer.schedule(self.handler, directory, self.recursive)
        self.observer.start()
        print("Observers started...")

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()

'''function to extract filename from path'''
def extract_filename(path):
    m = re.search(".*/(.*)", path)
    return m.group(1)


'''Custom Handler class to handle events retured by the watcher'''
class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        file_name = extract_filename(event.src_path)
        if event.event_type == "created" and file_name.endswith(".jpg"):
            print(f"New image file: {file_name} created.....")
            indexer = Indexer()
            json_res = indexer.index(file_name, event.src_path)
            indexer.dump_to_json(json_res)
            print(f"Dumping json of {file_name} to index.json....")


if __name__ == "__main__":
    import re
    paths  = ["/worker-app/data/images"]
    print("paths => ", paths)
    w = Watcher(paths, MyHandler(), True)
    w.run()
