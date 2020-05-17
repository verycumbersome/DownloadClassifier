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

        # Create Sorter classification patterns
        for path in outPaths:
            self.patterns += outPaths[path]["pattern"]
            self.createPath(outPaths[path]["outPath"])


    def run(self):
        """
        Runs a continuous while loop to maintain the running state of the program
        """
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = PatternMatchingEventHandler(
            self.patterns,
            self.ignore_patterns,
            self.ignore_directories,
            self.case_sensitive
        )

        # event_handler.on_deleted = self.on_deleted
        # event_handler.on_modified = self.on_modified
        event_handler.on_moved = self.on_moved
        event_handler.on_created = self.on_created

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
        """
        Initalizes the path to create the folder when ran
        """
        # Create new directory for output path
        try:
            os.mkdir(outPath)
        except OSError:
            print ("Creation of the directory %s failed" % outPath)
        else:
            print ("Successfully created the directory %s " % outPath)


    def classifyFile(self, path):
        """
        Returns the value of the classification type as provided to the class via self.outPaths
        """
        # Gets extension of file from path
        name, ext = filename, file_extension = os.path.splitext(path)
        fileName = os.path.basename(path)

        # Look for all keywords in path
        for classification in self.outPaths:
            keywords = self.outPaths[classification]["keywords"]
            if [ele for ele in keywords if(ele in fileName)]:
                return (classification)
#

        # Look for all extension patterns in path
        for classification in self.outPaths:
            if (ext in [x.replace("*", "") for x in self.outPaths[classification]["pattern"]]):
                # Return classification if found
                return (classification)

        # If no classification is found return
        return None


    def organizeDir(self):
        """
        Classifies and moves each recognizable file in the directory to its corresponding classification path
        """
        # Classify every file in dir
        for file in os.listdir(self.path):
            curPath = self.path + file
            self.moveFile(curPath)


    def moveFile(self, srcPath):
        """
        Moves the file from srcPath to the relative path given the classification value
        """
        # Gets the classification for the file type of the path moved
        classification = self.classifyFile(srcPath)

        if classification:
            # Gets the output path given the file type
            newPath = self.outPaths[classification]["outPath"] + srcPath.split("/")[-1]

            # Execute instruction
            os.replace(srcPath, newPath)


    def on_moved(self, event):
        """
        Event handler for when a file is moved in the directory
        """
        print("Moved")
        time.sleep(5)
        self.moveFile(event.dest_path)

    def on_created(self, event):
        """
        Event handler for when a file is created in the directory
        """
        print("Created")
        time.sleep(5)
        self.moveFile(event.src_path)

    # def on_deleted(self, event):
    #     event.src_path
    #     print(f"what the f**k! Someone deleted {event.src_path}!")
    #
    # def on_modified(self, event):
    #     event.src_path
    #     print(f"hey buddy, {event.src_path} has been modified")




def main():
    mainPath = "/Users/matthewjordan/Downloads/"
    outPaths = {
        "Video":{
            "outPath":mainPath + "Video/",
            "keywords":[],
            "pattern":["*.mp4", "*.mov"]
        },
        "Audio":{
            "outPath":mainPath + "Audio/",
            "keywords":[],
            "pattern":["*.mp3", "*.m4a", "*.mid", "*.wav", "*.aif", "*.aiff"]
        },
        "Image":{
            "outPath":mainPath + "Image/",
            "keywords":[],
            "pattern":["*.png", "*.jpg", "*.jpeg", "*.gif", "*.pdf"]
        },
        "Acapella":{
            "outPath":mainPath + "Acapella/",
            "keywords":["acapella", "Acapella"],
            "pattern":[]
        },
    }
    # Initalize and run the Sorter classe
    dirSorter = DirSorter(mainPath, outPaths)
    # dirSorter.organizeDir()
    # dirSorter.run()
    tempPath = mainPath + "(Acapella) Pop Out - Polo G Feat. Lil Tjay.mp3"
    print(dirSorter.classifyFile(tempPath))


if __name__ == '__main__':
    main()
