#!/usr/bin/env python
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
        self.instructionQueue = [("","") for i in range(1)]

        print(self.instructionQueue)

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
        name, ext = filename, file_extension = os.path.splitext(path)

        # Checks to see which classifier the extension is in
        for classification in self.outPaths:
            if (ext in [x.replace("*", "") for x in self.outPaths[classification]["pattern"]]):
                # Return classification if found
                return (classification)

        # If no classification is found return
        return None


    def classifyDir(self):
        # Classify every file in dir
        for file in os.listdir(self.path):
            curPath = self.path + file
            self.moveFile(curPath)


    def moveFile(self, srcPath):
        # Gets the classification for the file type of the path moved
        classification = self.classifyFile(srcPath)

        if classification:
            # Gets the output path given the file type
            newPath = self.outPaths[classification]["outPath"] + srcPath.split("/")[-1]

            # Execute instruction
            os.replace(srcPath, newPath)


            # curInstruction = self.instructionQueue.pop(0)
            # try:
            #     print("Moving file", curInstruction[1], "to", curInstruction[0])
            #     os.replace(curInstruction[0], curInstruction[1])
            #     self.instructionQueue.append(("", ""))
            #
            # except:
            #     print("Unable to move file")

            # Add isntruction to instructionQueue
            # self.instructionQueue.append((srcPath, newPath))


    def on_moved(self, event):
        print("Moved")
        self.moveFile(event.dest_path)

    def on_created(self, event):
        print("Created")
        self.moveFile(event.src_path)

    def on_deleted(self, event):
        event.src_path
        print(f"what the f**k! Someone deleted {event.src_path}!")


    def on_modified(self, event):
        event.src_path
        print(f"hey buddy, {event.src_path} has been modified")




def main():
    mainPath = "/Users/matthewjordan/Code/DownloadOrganizer/Testfolder/"
    outPaths = {
        "Video":{
            "outPath":mainPath + "Video/",
            "pattern":["*.mp4", "*.mov"]
        },
        "Audio":{
            "outPath":mainPath + "Audio/",
            "pattern":["*.mp3", "*.m4a", "*.mid", "*.wav", "*.aif", "*.aiff"]
        },
        "Image":{
            "outPath":mainPath + "Image/",
            "pattern":["*.png", "*.jpg", "*.pdf"]
        },
    }
    # Initalize and run the Sorter classe
    dirSorter = DirSorter(mainPath, outPaths)
    dirSorter.classifyDir()
    dirSorter.run()


if __name__ == '__main__':
    main()
