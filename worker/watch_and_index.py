import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

from index_image import *

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

'''function to extract filename from path'''
def extract_filename(path):
    m = re.search(".*/(.*)", path)
    return m.group(1)


'''Custom Handler class to handle events retured by the watcher'''
class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        file_name = extract_filename(event.src_path)
        image_file = file_name.endswith(".jpg") or file_name.endswith(".png")
        indexer = Indexer()
        print(f"{file_name} created event.....")
        json_res = indexer.index(file_name, event.src_path)
        indexer.dump_to_json(json_res)
        print(f"Dumping json of {file_name} to index.json....")

    def on_deleted(self, event):
        file_name = extract_filename(event.src_path)
        image_file = file_name.endswith(".jpg") or file_name.endswith(".png")
        indexer = Indexer()
        print(f"{file_name} delete event.....")
        indexer.remove_from_json(file_name)
        print(f"deleted {file_name} index from index.json")

if __name__ == "__main__":
    import re
    paths  = ["/worker-app/data/images"]
    w = Watcher(paths, MyHandler(), True)
    w.run()
