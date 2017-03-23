from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
import sys
import tempfile
import os
import shutil
import datetime
import maps
import threading
from qtGUI import monitor
from PyQt5.Qt import QDoubleValidator
from PyQt5.Qt import pyqtSignal
import stationLocation
import serial
import time
 
#TO DO:
#    1) # GPS for circle coming round
#    2) Comm with Fizza
#    3) Implement Hover
#    4) integration with Ann
class Ui_MainWindow(QtCore.QObject):
    INDEX_MIN = 1
    TIMEOUT = 60
    IMAGE_NAME = "image"
    IMAGE_TYPE = ".jpg"
    DATA_TYPE = ".txt"
    updateMapAndImage = pyqtSignal()
    updateLoc = pyqtSignal()
    timeOutSignal = pyqtSignal()
    resetTimer = pyqtSignal()
    warningBox = pyqtSignal()
    
    READ_FILE = False
        
    def setupUi(self, MainWindow):
        
        #USED FOR TESTING ONLY
        self.dirInput = "/home/calla/Input"
        self.dirDisplay = "/home/calla/workspace/Gui/src/qtGUI"
        
        
        cwd = os.getcwd()
        
        currTime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.dirStore = cwd+'/'+currTime
        os.makedirs(self.dirStore)
        self.dirDisplay = tempfile.mkdtemp()
        self.mapLocal = 'file://'+self.dirDisplay+'/map.html'
        
        
        self.index = 1
        self.previousLat = -1
        self.previousLng = -1
        self.latitude = 0
        self.longitude = 0
        self.waypoints = []
        self.uavLocations = []
        self.mapLocLat =0
        self.mapLocLng =0
        self.pictureLocation = 0
        self.maxIndex = 1
        self.currWaypoint = 1
        self.timedOut = False
        self.counter = 0;

        
        #set up the serial port for Communication
        if(not self.READ_FILE):
            self.ser = serial.Serial()
            self.ser.port = '/dev/ttyUSB0'
            self.ser.baudrate = 19200
            self.ser.timeout = 1
            self.ser.open()
        
        #Set up MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(899, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        #Set up the image widget for displaying JPEGS
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap(self.dirDisplay+"/"+Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
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
        with open(self.dirDisplay+'/map.html', "w") as out:
            print(map_google, file=out)
        self.map = QWebView(self.centralwidget)
        self.map.load(QtCore.QUrl(self.mapLocal))
        self.map.setObjectName("map")
        self.frame = self.map.page().mainFrame()
        self.frame.addToJavaScriptWindowObject('statLoc', self)
        self.verticalLayout.addWidget(self.map)
        self.updateMapAndImage.connect(self.changeMap)
        self.updateLoc.connect(self.panToLoc)
        self.resetTimer.connect(self.resetTime)
        self.warningBox.connect(self.commWarning)
        self.timeOutSignal.connect(self.commDownWarn)
        
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
        
        #Controls: UAV; return home, emergency stop, send Control
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
        self.sendControlButton= QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendControlButton.sizePolicy().hasHeightForWidth())
        self.sendControlButton.setSizePolicy(sizePolicy)
        self.sendControlButton.setObjectName("sendControlButton")
        self.sendControlButton.clicked.connect(self.sendControlCommand)
        self.horizontalLayout_5.addWidget(self.sendControlButton)
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
        
        
    def retranslateUi(self, MainWindow):
        """
        Set the text on the widgets in the MainWindow.
        
        Parameters
        ----------
        MainWindow: Ui_MainWindow
            The window which the widgets belong to.
        Returns
        -------
        
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.leftButton.setText(_translate("MainWindow", "Backwards"))
        self.rightButton.setText(_translate("MainWindow", "Forwards"))
        self.flightLabel.setText(_translate("MainWindow", "Flight Path"))
        self.controlLabel.setText(_translate("MainWindow", "Map and UAV Controls"))
        self.pathDonePushButton.setText(_translate("MainWindow", "Path Complete"))
        self.originLabelLat.setText(_translate("MainWindow", "Latitude"))
        self.originLabelLon.setText(_translate("MainWindow", "Longitude"))
        self.centerMap.setText(_translate("MainWindow", "Center Map"))
        self.returnHomeButton.setText(_translate("MainWindow", "Return Home"))
        self.sendControlButton.setText(_translate("MainWindow", "Send Control")) 
        self.emergButton.setText(_translate("MainWindow", "Emergency Land"))
        self.batteryLabel.setText(_translate("MainWindow", "Battery Power"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionFile.setText(_translate("MainWindow", "File"))
    
    #ONLY USED FOR TESTING
    def update(self, fileImage, fileData):
        """
        Used for testing, reads a file and updates the dislayed variables and the picture.
        
        This method is called from the monitor object when a file and image appears in the 
        monitored directory.  The file is parsed for latitude, longitude, power, and waypoint values.
        The jpeg is added to the stream of images. The method emits updateMapAndImage which calls 
        the changeMap method
        
        Parameters
        ----------
        fileImage: String
            Path to the jpeg
        fileData: String
            Path to the data text file
        
        Returns
        -------
        
        
        """
        currTime = datetime.datetime.now().strftime("%I-%M-%S")
        
        txtName =  self.dirStore+"/"+ currTime +"-data" +Ui_MainWindow.DATA_TYPE
        shutil.move(fileData, txtName)
        
        f =open(txtName, "r")
        self.previousLat = self.latitude
        self.previousLng = self.longitude
        self.latitude = f.readline()
        self.longitude = f.readline()
        power = f.readline()
        waypoint = f.readline()
        self.batteryProgress.setProperty("value", float(power))
            
        if((not (str(self.currWaypoint).strip() == str(waypoint).strip() )) and str(waypoint).strip() == "1"):
                self.maxIndex = self.pictureLocation
                self.pictureLocation = Ui_MainWindow.INDEX_MIN
        else:
                self.pictureLocation = self.pictureLocation +1
        self.currWaypoint = waypoint
       
        if(self.pictureLocation > self.maxIndex):
            self.maxIndex = self.pictureLocation
        
        shutil.move(fileImage, self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE)
        shutil.copy(self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE, 
                    self.dirDisplay+"/"+ Ui_MainWindow.IMAGE_NAME +str(self.pictureLocation)+ Ui_MainWindow.IMAGE_TYPE)
       
        self.updateMapAndImage.emit()
        '''doc = untangle.parse(xmlName)
        self.latitude = float(doc.data.gps['latitude'])
        self.longitude = float(doc.data.gps['longitude'])
        power = float(doc.data.battery['power'])
        self.batteryProgress.setProperty("value", power)
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.updateMapAndImage.emit()'''
    
    def changeMap(self):
        """
        Updates the map points and the currently displayed image.
        
        This method reloads currently displayed image incase the image has changed when data was received.
        The new latitude and longitude values are added to the map, if a picture was removed from the stream
        then the corresponding map point is removed from the map.
        
        Parameters
        ----------
        
        Returns
        -------
        
        
        """
        self.image.setPixmap(QtGui.QPixmap(self.dirDisplay+"/"+Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        if(not self.previousLat == -1 and not self.previousLng==-1):
            self.frame.evaluateJavaScript("addMarker("+str(self.previousLat)+", "+str(self.previousLng)+")")
        self.frame.evaluateJavaScript("addCurrMarker("+str(self.latitude)+", "+str(self.longitude)+")")
        
        if(self.maxIndex > len(self.uavLocations)):
            self.uavLocations.append([self.latitude, self.longitude]);
        else:
            print(str(self.uavLocations[self.pictureLocation-1][0]) + "   " + str(self.uavLocations[self.pictureLocation-1][1]))
            self.frame.evaluateJavaScript("removeMarker("+str(self.uavLocations[self.pictureLocation-1][0]) +", "+str(self.uavLocations[self.pictureLocation-1][1]) +")")
            self.uavLocations[self.pictureLocation-1] = [self.latitude, self.longitude]
            
    def scrollLeft(self):
        """
        Updates the displayed picture with the picture to the left of the current picture in the stream
        
        This method changes the displayed picture to the picture left of the current picture in the stream.
        If index is updates to the index of the newly displayed picture.  If the current picture is the first in the
        stream, the last picture in the stream is displayed.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        self.index=self.index-1
        if self.index < Ui_MainWindow.INDEX_MIN:
            self.index = self.maxIndex
        print(self.index)
        self.image.setPixmap(QtGui.QPixmap(self.dirDisplay + "/"+Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
    
    def scrollRight(self):
        """
        Updates the displayed picture with the picture to the right of the current picture in the stream
        
        This method changes the displayed picture to the picture right of the current picture in the stream.
        If index is updates to the index of the newly displayed picture.  If the current picture is the last in the
        stream, the first picture in the stream is displayed.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        self.index=self.index+1
        if self.index > self.maxIndex:
            self.index = Ui_MainWindow.INDEX_MIN
        print(self.index)
        self.image.setPixmap(QtGui.QPixmap(self.dirDisplay+"/"+Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
    
    @QtCore.pyqtSlot(float, float)
    def changePicture(self,lat,lng):
        """
        Adjust Picture to Users click
        
        This method is called from the map html file when the user double clicks on a marker
        on the map and the picture changes to the related image
        
        Parameters
        ----------
        lat: float
            The latitude location of the users click
            
        lng: float
            The longitude location of the users click
        
        Returns
        -------
        
        """
        i=0
        for point in self.uavLocations:
            i=i+1
            if(str(point[0]).strip()==str(lat).strip() and str(point[1]).strip()==str(lng).strip()):
                self.index=i;
        
        self.image.setPixmap(QtGui.QPixmap(self.dirDisplay+"/"+Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))



    @QtCore.pyqtSlot(float, float)
    def addPath(self,lat,lng):
        """
        Adds a user entered point to the waypoints list.
        
        This method is called from the map html file when the user clicks on the map and the maps 
        pathComplete variable is set to false.  The latitude and longitude(in reference to the map)
        of where the user click is passes to this method.  The coordinates are added to the waypoints
        list.
        
        Parameters
        ----------
        lat: float
            The latitude location of the users click
            
        lng: float
            The longitude location of the users click
        
        Returns
        -------
        
        """
        self.waypoints.append([lat,lng])
        print(self.waypoints)
    
    #remove path point from waypoint list    
    @QtCore.pyqtSlot(float, float)
    def removePoint(self,lat,lng):
        """
        Removes a user entered point from the waypoints list.
        
        This method is called from the map html file when the user double clicks on a marker
        on the map and the maps pathComplete variable is set to false.  
        The latitude and longitude(in reference to the map) of where the user click is passes to 
        this method.  The coordinates are added to the waypoints list.
        
        Parameters
        ----------
        lat: float
            The latitude location of the users click
            
        lng: float
            The longitude location of the users click
        
        Returns
        -------
        
        """
        self.waypoints.remove([lat,lng])
        print(self.waypoints)
        
    def setMapLoc(self):
        """
        Reads the user entered latitude and longitude and emits the updateLoc signal.
        
        The user entered latitude location is read from the latitude text edit box.
        The user entered longitude location is read from the longitude text edit box.
        The updateLoc signal is emitted.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        self.mapLocLat= self.OriginEditLat.text()
        self.mapLocLng = self.OriginEditLon.text()
        self.updateLoc.emit()
    
    def panToLoc(self):
        """
        Sends a command to the displayed map center map around user entered latitude and longitude values
        
        This method is called when the updateLoc signal is emitted.  The map pans to the coordinate
        specified by the mapLocLat and mapLocLng variables.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        self.frame.evaluateJavaScript("setCenter("+self.mapLocLat+", "+self.mapLocLng+")")
    
    def pathSet(self):
        """
        Toggles the users ability to add/remove path points to the map, and sends msg to the serial port
        
        This method sends a command to the map to toggle the pathComplete variable.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        self.frame.evaluateJavaScript("setPathComplete()")
        if(not self.READ_FILE):
            self.ser.write(b'path set send waypoints?')
      
    def returnHomeCommand(self):
        """
        Send return home command.
        
        Write the return home command to the serialport
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        print("return home command")
        if(not self.READ_FILE):
            self.ser.write(b'returnHomeCommand')
    
    def sendControlCommand(self):
        """
        Send sendControl command.
        
        Write the sendControl command to the serialport
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        print("control command")
        if(not self.READ_FILE):
            self.ser.write(b'control command')
     
    #send emergency stop command to UAV    
    def emergCommand(self):
        """
        Send return emergency command.
        
        Write the  emergency to the serialport
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        print("emergency stop")
        if(not self.READ_FILE):
            self.ser.write(b'emergency command')
     
    def commWarning(self):
        """
        Creates message box to warn users of the comm link being down.
        
        This method is called when the commTime timer times out, therefore indicating that
        a message from the UAV has not been received in timeout seconds.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        while True:
            if(self.timedOut == False):
                self.counter = self.counter+1
                time.sleep(1)
                if(self.counter == self.TIMEOUT):
                    self.timeOutSignal.emit()
            else:
                pass
       

    def commDownWarn(self): 
        if(not self.READ_FILE):
            self.timedOut = True
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("The Commlink is down")
            msgBox.exec()
        
        
    def resetTime(self):
        """
        The commTime timer is restarted
        
        This method is called when data is received on the serial port, the current commTime 
        timer is cancelled and a new one is started.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        self.counter = 0
        self.timedOut = False
        
        
    
    def monitorSerial(self):
        """
        Monitors the serial port for data, and parses data when it is received.
        
        This method waits for data to be received on the serial port.  When data is received, this method
        parses the data, and resets the commTime timer.  The method reads in latitude, longitude, power, 
        currentwaypoint, and jpeg data.  It checks if the UAV is restarting a loop around the building,
        and the index should be reset to one.  It updates the power progress bar, and copies the jpeg
        to a directory with the rest of the stream photos.  The method emits the updateMapAndImage signal.
        
        Parameters
        ----------
        
        Returns
        -------
        
        """
        #fcntl.fcntl(sys.stdin, fctnl.F_SETFL, os.O_NONBLOCK)
        while 1:
            receive = self.ser.inWaiting()
            if receive:
                print("rec")
                self.resetTimer.emit()
                currTime = datetime.datetime.now().strftime("%I-%M-%S")
                self.previousLat = self.latitude
                self.latitude = self.ser.readline().decode('UTF-8')
                print(self.latitude)
                self.previousLng = self.longitude;
                self.longitude = self.ser.readline().decode('UTF-8')
                print(self.longitude)
                power = self.ser.readline().decode('UTF-8')
                print(power)
                waypoint = self.ser.readline().decode('UTF-8')
                data = []
                jpeg = True
                print(waypoint)
                while jpeg:
                    b = self.ser.read()
                    data.append(b)
                    if(str(b)[2:-1] == "\\xff"):
                        b = self.ser.read()
                        print(b)
                        if(str(b)[2:-1]  == "\\xd9"):
                            jpeg = False
                            print("end")
                        data.append(b)
                #self.ser.readline()
                with open(self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE, 'wb') as f:
                    for i in data:
                        f.write(bytearray(i))
                print(str(self.currWaypoint).strip() + "   "+ str(waypoint).strip())
                if((not (str(self.currWaypoint).strip() == str(waypoint).strip() )) and str(waypoint).strip() == "1"):
                    self.maxIndex = self.pictureLocation
                    self.pictureLocation = Ui_MainWindow.INDEX_MIN
                else:
                    self.pictureLocation = self.pictureLocation +1
                self.currWaypoint = waypoint
                
                #First round through circle
                if(self.pictureLocation > self.maxIndex):
                    self.maxIndex = self.pictureLocation   
                
                shutil.copy(self.dirStore+"/"+ currTime +"-image" + Ui_MainWindow.IMAGE_TYPE, 
                    self.dirDisplay+"/"+ Ui_MainWindow.IMAGE_NAME +str(self.pictureLocation)+ Ui_MainWindow.IMAGE_TYPE)    
                self.batteryProgress.setProperty("value", int(power))
                
                self.updateMapAndImage.emit()
                
        
            
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    if(ui.READ_FILE):
        w = monitor.Watcher(ui.dirInput, ui.dirStore, ui.dirDisplay, ui)
        t1 = threading.Thread(target=w.run, daemon=True)
    else:
        t1 = threading.Thread(target=ui.monitorSerial, daemon=True)
    t1.start()
    t2 = threading.Thread(target=ui.commWarning, daemon=True)
    t2.start()
    try:
        sys.exit(app.exec_())
    except:
        pass
    finally:
        shutil.rmtree(ui.dirDisplay)