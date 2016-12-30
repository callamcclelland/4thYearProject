import time
import datetime
import shutil
import glob
import guiProject
import untangle
import folium
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
        for fileImage in glob.glob(self.dirInput+"/*"+ guiProject.Ui_MainWindow.IMAGE_TYPE):
            for fileData in glob.glob(self.dirInput+"/*" +  guiProject.Ui_MainWindow.DATA_TYPE):
                if(self.index > guiProject.Ui_MainWindow.INDEX_MAX):
                    self.index = guiProject.Ui_MainWindow.INDEX_MIN
                currTime = datetime.datetime.now().strftime("%I-%M-%S")
                shutil.move(fileImage, self.dirStore+"/"+ currTime +"-image" +guiProject.Ui_MainWindow.IMAGE_TYPE)
                shutil.copy(self.dirStore+"/"+ currTime +"-image" +guiProject.Ui_MainWindow.IMAGE_TYPE, 
                         self.dirDisplay+"/"+ guiProject.Ui_MainWindow.IMAGE_NAME +str(self.index)+ guiProject.Ui_MainWindow.IMAGE_TYPE)
                xml_name =  self.dirStore+"/"+ currTime +"-data" +guiProject.Ui_MainWindow.DATA_TYPE
                shutil.move(fileData, xml_name)
                self.index = self.index+1
                self.mainWindow.update(xml_name)

            
