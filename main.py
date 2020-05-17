import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class DirSorter():
    """docstring for Sorter object"""

    def __init__(self, path, outPaths):
        self.path = path
        self.outPaths = outPaths
        self.patterns = []
        self.ignore_patterns = ""
        self.ignore_directories = False
        self.case_sensitive = True

        outPaths["Misc"] = {
            "outPath":"/Users/matthewjordan/Downloads/Misc",
            "pattern":[]
        }

        # Create Sorter classification patterns
        for path in outPaths:
            self.patterns += outPaths[path]["pattern"]
            self.createPath(outPaths[path]["outPath"])


    def run(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = PatternMatchingEventHandler(
            self.patterns,
            self.ignore_patterns,
            self.ignore_directories,
            self.case_sensitive
        )

        event_handler.on_created = self.on_created
        event_handler.on_deleted = self.on_deleted
        event_handler.on_modified = self.on_modified
        event_handler.on_moved = self.on_moved

        go_recursively = True

        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=go_recursively)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()


    def createPath(self, outPath):
        # Create new directory for output path
        try:
            os.mkdir(outPath)
        except OSError:
            print ("Creation of the directory %s failed" % outPath)
        else:
            print ("Successfully created the directory %s " % outPath)


    def classifyFile(self, path):
        # Gets extension of file from path
        ext = path.split(".")[-1]

        # Checks to see which classifier the extension is in
        for classification in self.outPaths:
            if (ext in [x.replace("*.", "") for x in self.outPaths[classification]["pattern"]]):
                # Return classification if found
                return (classification)

        # If no classification is found return Misc
        return ("Misc")

    def on_created(self, event):
        event.src_path
        print("CREATED")


    def on_deleted(self, event):
        event.src_path
        print(f"what the f**k! Someone deleted {event.src_path}!")


    def on_modified(self, event):
        event.src_path
        print(f"hey buddy, {event.src_path} has been modified")


    def on_moved(self, event):
        classification = self.classifyFile(event.dest_path)
        newPath = self.outPaths[classification]["outPath"] + event.dest_path.split("/")[-1]
        print(newPath)
        os.replace(event.dest_path, newPath)
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


def main():
    outPaths = {
        "Video":{
            "outPath":"/Users/matthewjordan/Downloads/Video/",
            "pattern":["*.mp4", "*.mov"]
        },
        "Audio":{
            "outPath":"/Users/matthewjordan/Downloads/Audio/",
            "pattern":["*.mp3", "*.wav", "*.aif"]
        }
    }
    # Initalize and run the Sorter classe
    dirSorter = DirSorter("/Users/matthewjordan/Downloads/", outPaths)
    dirSorter.run()


if __name__ == '__main__':
    main()
