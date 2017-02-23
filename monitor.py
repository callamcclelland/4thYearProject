import time
import glob
import guiProject
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from urllib.request import FileHandler
from PyQt5 import QtCore, QtGui, QtWidgets



class Watcher:

    def __init__(self, dirInput, dirStore, dirDisplay,ui):
        self.dirInput = dirInput
        self.observer = Observer()
        self.dirStore = dirStore
        self.dirDisplay = dirDisplay
        self.ui = ui

    def run(self):
        """
        Creates an event_handler and waits for a signal.
        
        Creates an event_handler and then waits for the signal from the handler that something
        has happened.
        
        Parameters
        ----------
        
        Returns
        -------
        
        
        """
        event_handler = Handler(self.dirInput, self.dirStore, self.dirDisplay, self.ui)
        self.observer.schedule(event_handler, self.dirInput, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    
    def __init__(self, dirInput, dirStore, dirDisplay, mainWindow):
        super(Handler, self).__init__()
        self.dirInput = dirInput
        self.dirStore = dirStore
        self.dirDisplay = dirDisplay
        self.mainWindow = mainWindow
        self.index = guiProject.Ui_MainWindow.INDEX_MIN

    def on_created(self, event):
        """
        Monitors a directory and calls the MainWindow update function on the GUI
        
        Monitors a directory, when a file is created in the directory, it checks that there is a jpeg
        and a text file.  If there is both file types then it calls the MainWindow update function,
        and passes in both file paths.
        
        Parameters
        ----------
        
        Returns
        -------
        
        
        """
        if(guiProject.Ui_MainWindow.TESTING_COMM):
            for fileData in glob.glob(self.dirInput+"/*" + ".txt"):
                with open(fileData, 'r') as f:
                    read = f.read().split('\n')
                    self.mainWindow.commTest(read)
                os.remove(fileData)
        else:
            for fileImage in glob.glob(self.dirInput+"/*"+ guiProject.Ui_MainWindow.IMAGE_TYPE):
                for fileData in glob.glob(self.dirInput+"/*" +  guiProject.Ui_MainWindow.DATA_TYPE):
                    self.mainWindow.update( fileImage, fileData)

            
