from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
import sys
import shutil
import datetime
import maps
import threading
import untangle
from qtGUI import monitor
from PyQt5.Qt import QDoubleValidator
from PyQt5.Qt import pyqtSignal
import tester
import serial
 
#TO DO:
#    1) # GPS for circle coming round
#    2) Comm with Fizza
#    3) Implement Hover
#    4) integration with Ann
class Ui_MainWindow(QtCore.QObject):
    INDEX_MAX = 3
    INDEX_MIN = 1
    IMAGE_NAME = "image"
    IMAGE_TYPE = ".jpeg"
    DATA_TYPE = ".txt"
    mysignal = pyqtSignal()
    updateLoc = pyqtSignal()
    
    TESTING_COMM = False
    
        
    def setupUi(self, MainWindow):
        self.coordinates = []
        self.index = 1
        self.power = []
        self.latitude = 0
        self.longitude = 0
        self.waypoints = []
        self.uavLocations = []
        self.mapLocLat =0
        self.mapLocLng =0
        self.pictureLocation = 0
        self.dirStore = "/home/calla/Output"
        self.dirInput = "/home/calla/Input"
        self.dirDisplay = "/home/calla/workspace/Gui/src/qtGUI"
        self.maxIndex = 0
        self.currWaypoint = 0
        
        #serial port
        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyUSB0'
        self.ser.baudrate = 9600
        self.ser.timeout = 1
        self.ser.open()
        
        #Set up MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(899, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        #Image View
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
      
        #Set Up Map
        map_google = maps.Map()
        with open("map.html", "w") as out:
            print(map_google, file=out)
        self.map = QWebView(self.centralwidget)
        self.map.load(QtCore.QUrl('file:///home/calla/workspace/Gui/src/qtGUI/map.html'))
        self.map.setObjectName("map")
        self.frame = self.map.page().mainFrame()
        self.station_location = tester.StationLocation()
        self.frame.addToJavaScriptWindowObject('statLoc', self)
        self.verticalLayout.addWidget(self.map)
        self.mysignal.connect(self.changeMap)
        self.updateLoc.connect(self.panToLoc)
        
        #Controls: MAP; set origin, finish path
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
        
        #Controls: UAV; return home, emergency stop, hover
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.returnHomeButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnHomeButton.sizePolicy().hasHeightForWidth())
        self.returnHomeButton.setSizePolicy(sizePolicy)
        self.returnHomeButton.setObjectName("returnHomeButton")
        self.returnHomeButton.clicked.connect(self.returnHomeCommand)
        self.horizontalLayout_5.addWidget(self.returnHomeButton)
        self.hoverButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hoverButton.sizePolicy().hasHeightForWidth())
        self.hoverButton.setSizePolicy(sizePolicy)
        self.hoverButton.setObjectName("hoverButton")
        self.hoverButton.clicked.connect(self.hoverCommand)
        self.horizontalLayout_5.addWidget(self.hoverButton)
        self.emergButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emergButton.sizePolicy().hasHeightForWidth())
        self.emergButton.setSizePolicy(sizePolicy)
        self.emergButton.setObjectName("emergButton")
        self.emergButton.clicked.connect(self.emergCommand)
        self.horizontalLayout_5.addWidget(self.emergButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        
        #Battery View progress bar
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
        
        #Display GUI
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()
        
        
        #Set Widget Text
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
        self.returnHomeButton.setText(_translate("MainWindow", "Return Home"))
        self.hoverButton.setText(_translate("MainWindow", "Hover")) 
        self.emergButton.setText(_translate("MainWindow", "Emergency Land"))
        self.batteryLabel.setText(_translate("MainWindow", "Battery Power"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionFile.setText(_translate("MainWindow", "File"))
    
    #update the GUI when image and xml file are delivered to base station
    def update(self, fileImage, fileData):
        #UPDATE for GPS 
        #Read Textfile
        #Time used as file name
        currTime = datetime.datetime.now().strftime("%I-%M-%S")
        
        txtName =  self.dirStore+"/"+ currTime +"-data" +Ui_MainWindow.DATA_TYPE
        shutil.move(fileData, txtName)
        
        f =open(txtName, "r")
        
        self.latitude = f.readline()
        self.longitude = f.readline()
        self.coordinates.append([self.latitude, self.longitude])
        power = f.readline()
        self.batteryProgress.setProperty("value", float(power)) 
        waypoint = f.readline()
            
        
        if(self.pictureLocation == Ui_MainWindow.INDEX_MAX):
            self.pictureLocation = Ui_MainWindow.INDEX_MIN
        else:
            self.pictureLocation = self.pictureLocation +1
            if(self.pictureLocation > self.maxIndex):
                self.maxIndex = self.pictureLocation
        
        shutil.move(fileImage, self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE)
        shutil.copy(self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE, 
                    self.dirDisplay+"/"+ Ui_MainWindow.IMAGE_NAME +str(self.pictureLocation)+ Ui_MainWindow.IMAGE_TYPE)
       
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.mysignal.emit()
        '''doc = untangle.parse(xmlName)
        self.latitude = float(doc.data.gps['latitude'])
        self.longitude = float(doc.data.gps['longitude'])
        self.coordinates.append([self.latitude, self.longitude])
        power = float(doc.data.battery['power'])
        self.batteryProgress.setProperty("value", power)
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.mysignal.emit()'''
    
    #Add new GPS point to map
    def changeMap(self):
        self.frame.evaluateJavaScript("addMarker("+str(self.latitude)+", "+str(self.longitude)+")")
        if(self.maxIndex > len(self.uavLocations)):
            self.uavLocations.append([self.latitude, self.longitude]);
        else:
            print(str(self.uavLocations[self.pictureLocation-1][0]) + "   " + str(self.uavLocations[self.pictureLocation-1][1]))
            self.frame.evaluateJavaScript("removeMarker("+str(self.uavLocations[self.pictureLocation-1][0]) +", "+str(self.uavLocations[self.pictureLocation-1][1]) +")")
            self.uavLocations[self.pictureLocation] = [self.latitude, self.longitude]
            
    #Scroll Backwards
    def scrollLeft(self):
        self.index=self.index-1
        if self.index < Ui_MainWindow.INDEX_MIN:
            self.index = self.maxIndex
        print(self.index)
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
    
    #Scroll forward 
    def scrollRight(self):
        self.index=self.index+1
        if self.index > self.maxIndex:
            self.index = Ui_MainWindow.INDEX_MIN
        print(self.index)
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
     
    #Add new path point to waypoint list      
    @QtCore.pyqtSlot(float, float)
    def addPath(self,lat,lng):
        self.waypoints.append([lat,lng])
        print(self.waypoints)
    
    #remove path point from waypoint list    
    @QtCore.pyqtSlot(float, float)
    def removePoint(self,lat,lng):
        self.waypoints.remove([lat,lng])
        print(self.waypoints)
        
    #Set map origin lcoation
    def setMapLoc(self):
        self.mapLocLat= self.OriginEditLat.text()
        self.mapLocLng = self.OriginEditLon.text()
        self.updateLoc.emit()
        
    def panToLoc(self):
        print("setCenter("+self.mapLocLat+", "+self.mapLocLng+")")
        self.frame.evaluateJavaScript("setCenter("+self.mapLocLat+", "+self.mapLocLng+")")
    
    #  toggle path complete boolean; pathComplete = true means points can not be added or removed  
    def pathSet(self):
        self.frame.evaluateJavaScript("setPathComplete()")
    
    #send return home command to UAV    
    def returnHomeCommand(self):
        print("return home command")
        self.ser.write(b'returnHomeCommand')
    
    #send hover command to UAV
    def hoverCommand(self):
        print("hover command")
     
    #send energency stop command to UAV    
    def emergCommand(self):
        print("emergency stop")
        
    #comm test for Fizza
    def commTest(self, read):
        self.batteryProgress.setProperty("value", read[0])
        
    def monitorSerial(self):
        
        #fcntl.fcntl(sys.stdin, fctnl.F_SETFL, os.O_NONBLOCK)
        
        while 1:
            receive = self.ser.inWaiting()
            if receive:
                
                self.latitude = self.ser.readline().decode('UTF-8')
                print(self.latitude)
                '''self.longitude = self.ser.readline().decode('UTF-8')
                self.coordinates.append([self.latitude, self.longitude])
                power = self.ser.readline().decode('UTF-8')
                self.batteryProgress.setProperty("value", int(power))
                waypoint = self.ser.readline().decode('UTF-8')
                
                if(self.pictureLocation == Ui_MainWindow.INDEX_MAX):
                    self.pictureLocation = Ui_MainWindow.INDEX_MIN
                else:
                    self.pictureLocation = self.pictureLocation +1
                if(self.pictureLocation > self.maxIndex):
                    self.maxIndex = self.pictureLocation
                    
                self.mysignal.emit()'''
                
        
            
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    w = monitor.Watcher(ui.dirInput, ui.dirStore, ui.dirDisplay, ui)
    #t1 = threading.Thread(target=w.run, daemon=True)
    t1 = threading.Thread(target=ui.monitorSerial, daemon=True)
    t1.start()
    sys.exit(app.exec_())