from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
import sys
import math
import time
import folium
import shutil
import datetime
import maps
import threading
import untangle
from shutil import copyfile
from qtGUI import monitor
from geojson import Point
from PyQt5.Qt import pyqtSlot, QIntValidator, QDoubleValidator
from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

import tester
 
 #TODO: Find out how to get back to first index if within % of first lat and lng
class Ui_MainWindow(QtCore.QObject):
    INDEX_MAX = 3
    INDEX_MIN = 1
    IMAGE_NAME = "image"
    IMAGE_TYPE = ".jpeg"
    DATA_TYPE = ".xml"
    mysignal = pyqtSignal()
    updateLoc = pyqtSignal()
    
        
    def setupUi(self, MainWindow):
        self.coordinates = []
        self.index = 1
        self.power = []
        self.latitude = 0
        self.longitude = 0
        self.waypoints = []
        self.mapLocLat =0
        self.mapLocLng =0
        self.pictureLocation = 1
        self.dirStore = "/home/calla/Output"
        self.dirInput = "/home/calla/Input"
        self.dirDisplay = "/home/calla/workspace/Gui/src/qtGUI"
        
        #MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(899, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        #Image
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.gridLayout.addWidget(self.image, 0, 0, 1, 1)
        #Image Scroll Buttons
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftButton = QtWidgets.QPushButton(self.centralwidget)
        self.leftButton.setObjectName("leftButton")
        self.horizontalLayout.addWidget(self.leftButton)
        self.leftButton.clicked.connect(self.scrollLeft)
        spacerItem = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.rightButton = QtWidgets.QPushButton(self.centralwidget)
        self.rightButton.setObjectName("rightButton")
        self.horizontalLayout.addWidget(self.rightButton)
        self.rightButton.clicked.connect(self.scrollRight)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.flightLabel = QtWidgets.QLabel(self.centralwidget)
        self.flightLabel.setObjectName("flightLabel")
        self.verticalLayout.addWidget(self.flightLabel)
        #map
        
        map_google = maps.Map()
        with open("map.html", "w") as out:
            print(map_google, file=out)
        self.map = QWebView(self.centralwidget)
        self.map.load(QtCore.QUrl('file:///home/calla/workspace/Gui/src/qtGUI/map.html'))
        self.map.setObjectName("map")
        #TEST#######################
        self.frame = self.map.page().mainFrame()
        self.station_location = tester.StationLocation()
        self.frame.addToJavaScriptWindowObject('statLoc', self)
        self.verticalLayout.addWidget(self.map)
        self.mysignal.connect(self.changeMap)
        self.updateLoc.connect(self.panToLoc)
        
        #Controls
        self.controlLabel = QtWidgets.QLabel(self.centralwidget)
        self.controlLabel.setObjectName("controlLabel")
        self.verticalLayout.addWidget(self.controlLabel)
        self.pathDonePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pathDonePushButton.setObjectName("pathDonePushButton")
        self.pathDonePushButton.clicked.connect(self.pathSet)
        self.verticalLayout.addWidget(self.pathDonePushButton)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.originLabelLat = QtWidgets.QLabel(self.centralwidget)
        self.originLabelLat.setObjectName("originLabelLat")
        self.horizontalLayout_2.addWidget(self.originLabelLat)
        self.OriginEditLat = QtWidgets.QLineEdit(self.centralwidget)
        self.OriginEditLat.setObjectName("OriginEditLat")
        self.OriginEditLat.setValidator(QDoubleValidator(-90.0, 90.0, 8,))
        self.horizontalLayout_2.addWidget(self.OriginEditLat)
        self.originLabelLon = QtWidgets.QLabel(self.centralwidget)
        self.originLabelLon.setObjectName("originLabelLon")
        self.horizontalLayout_2.addWidget(self.originLabelLon)
        self.OriginEditLon = QtWidgets.QLineEdit(self.centralwidget)
        self.OriginEditLon.setObjectName("OriginEditLon")
        self.OriginEditLon.setValidator(QDoubleValidator(-180.0, 180.0,8,))
        self.horizontalLayout_2.addWidget(self.OriginEditLon)
        self.centerMap = QtWidgets.QPushButton(self.centralwidget)
        self.centerMap.setObjectName("centerMap")
        self.centerMap.clicked.connect(self.setMapLoc)
        self.horizontalLayout_2.addWidget(self.centerMap)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.returnHome = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnHome.sizePolicy().hasHeightForWidth())
        self.returnHome.setSizePolicy(sizePolicy)
        self.returnHome.setObjectName("returnHome")
        self.horizontalLayout_5.addWidget(self.returnHome)
        self.hover = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hover.sizePolicy().hasHeightForWidth())
        self.hover.setSizePolicy(sizePolicy)
        self.hover.setObjectName("hover")
        self.horizontalLayout_5.addWidget(self.hover)
        self.Emerg = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Emerg.sizePolicy().hasHeightForWidth())
        self.Emerg.setSizePolicy(sizePolicy)
        self.Emerg.setObjectName("Emerg")
        self.horizontalLayout_5.addWidget(self.Emerg)
        spacerItem4 = QtWidgets.QSpacerItem(40, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.batteryLabel = QtWidgets.QLabel(self.centralwidget)
        self.batteryLabel.setObjectName("batteryLabel")
        self.verticalLayout.addWidget(self.batteryLabel)
        self.batteryProgress = QtWidgets.QProgressBar(self.centralwidget)
        self.batteryProgress.setProperty("value", 100)
        self.batteryProgress.setObjectName("batteryProgress")
        self.verticalLayout.addWidget(self.batteryProgress)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 899, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFile = QtWidgets.QAction(MainWindow)
        self.actionFile.setObjectName("actionFile")
        self.menubar.addAction(self.menuFile.menuAction())
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()
        
        
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.leftButton.setText(_translate("MainWindow", "PushButton"))
        self.rightButton.setText(_translate("MainWindow", "PushButton"))
        self.flightLabel.setText(_translate("MainWindow", "Flight Path"))
        self.controlLabel.setText(_translate("MainWindow", "Map and UAV Controls"))
        self.pathDonePushButton.setText(_translate("MainWindow", "Path Complete"))
        self.originLabelLat.setText(_translate("MainWindow", "Latitude"))
        self.originLabelLon.setText(_translate("MainWindow", "Longitude"))
        self.centerMap.setText(_translate("MainWindow", "Center Map"))
        self.returnHome.setText(_translate("MainWindow", "Return Home"))
        self.hover.setText(_translate("MainWindow", "Hover")) 
        self.Emerg.setText(_translate("MainWindow", "Emergency Land"))
        self.batteryLabel.setText(_translate("MainWindow", "Battery Power"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionFile.setText(_translate("MainWindow", "File"))
    
    
    def update(self, fileImage, fileData):
        currTime = datetime.datetime.now().strftime("%I-%M-%S")
        shutil.move(fileImage, self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE)
        shutil.copy(self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE, 
                    self.dirDisplay+"/"+ Ui_MainWindow.IMAGE_NAME +str(self.pictureLocation)+ Ui_MainWindow.IMAGE_TYPE)
        xmlName =  self.dirStore+"/"+ currTime +"-data" +Ui_MainWindow.DATA_TYPE
        shutil.move(fileData, xmlName)
        if(self.pictureLocation == Ui_MainWindow.INDEX_MAX):
            self.pictureLocation = Ui_MainWindow.INDEX_MIN
        else:
            self.pictureLocation = self.pictureLocation +1
        doc = untangle.parse(xmlName)
        self.latitude = float(doc.data.gps['latitude'])
        self.longitude = float(doc.data.gps['longitude'])
        self.coordinates.append([self.latitude, self.longitude])
        power = float(doc.data.battery['power'])
        self.batteryProgress.setProperty("value", power)
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        
        self.mysignal.emit()
    
    #Add new point to map
    def changeMap(self):
        self.frame.evaluateJavaScript("addMarker("+str(self.latitude)+", "+str(self.longitude)+")")
         #   if(self.index == i):
           #     map_google.add_main_point((point[0], point[1]))
       #     else:
        #        map_google.add_point((point[0], point[1]))
         #   i = i+1
    
    #Scroll Backwards, Update Map
    def scrollLeft(self):
        self.index=self.index-1
      
        if self.index < Ui_MainWindow.INDEX_MIN:
            self.index = Ui_MainWindow.INDEX_MAX
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.mysignal.emit()
    
    #Scroll forward, update map    
    def scrollRight(self):
        self.index=self.index+1
      
        if self.index > Ui_MainWindow.INDEX_MAX:
            self.index = Ui_MainWindow.INDEX_MIN
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.mysignal.emit()
                
    @QtCore.pyqtSlot(float, float)
    def addPath(self,lat,lng):
        self.waypoints.append([lat,lng])
        print(self.waypoints)
        
    @QtCore.pyqtSlot(float, float)
    def removePoint(self,lat,lng):
        self.waypoints.remove([lat,lng])
        print(self.waypoints)
        
    
    def setMapLoc(self):
        self.mapLocLat= self.OriginEditLat.text()
        self.mapLocLng = self.OriginEditLon.text()
        self.updateLoc.emit()
        
    def panToLoc(self):
        print("setCenter("+self.mapLocLat+", "+self.mapLocLng+")")
        self.frame.evaluateJavaScript("setCenter("+self.mapLocLat+", "+self.mapLocLng+")")
        
    def pathSet(self):
        self.frame.evaluateJavaScript("setPathComplete()")
            
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    w = monitor.Watcher(ui.dirInput, ui.dirStore, ui.dirDisplay, ui)
    t1 = threading.Thread(target=w.run, daemon=True)
    t1.start()
    sys.exit(app.exec_())