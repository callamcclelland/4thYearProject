'''
Created on Oct 22, 2016

@author: calla
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui.autosave.autosave'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
import sys
import math
import time
import folium
import maps
import threading
import untangle
from shutil import copyfile
from qtGUI import monitor
from geojson import Point
from PyQt5.Qt import pyqtSlot, QIntValidator, QDoubleValidator
from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

class Ui_MainWindow(QtCore.QObject):
    INDEX_MAX = 3
    INDEX_MIN = 1
    IMAGE_NAME = "image"
    IMAGE_TYPE = ".jpeg"
    DATA_TYPE = ".xml"
    mysignal = pyqtSignal()
    
        
    def setupUi(self, MainWindow):
        self.coordinates = []
        self.index = 1
        self.power = []
        self.latitude = []
        self.longitude = []
        self.waypoints = []
        self.initialized = False
        
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
        self.verticalLayout.addWidget(self.map)
        self.mysignal.connect(self.changeMap)
        
        #Controls
        self.controlLabel = QtWidgets.QLabel(self.centralwidget)
        self.controlLabel.setObjectName("controlLabel")
        self.verticalLayout.addWidget(self.controlLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.originLabelLat = QtWidgets.QLabel(self.centralwidget)
        self.originLabelLat.setObjectName("originLabelLat")
        self.horizontalLayout_2.addWidget(self.originLabelLat)
        self.OriginEditLat = QtWidgets.QLineEdit(self.centralwidget)
        self.OriginEditLat.setObjectName("OriginEditLat")
        self.OriginEditLat.setValidator(QDoubleValidator(-90.0, 90.0, 3,))
        self.OriginEditLat.textChanged.connect(self.textChanged)
        self.horizontalLayout_2.addWidget(self.OriginEditLat)
        self.originLabelLon = QtWidgets.QLabel(self.centralwidget)
        self.originLabelLon.setObjectName("originLabelLon")
        self.horizontalLayout_2.addWidget(self.originLabelLon)
        self.OriginEditLon = QtWidgets.QLineEdit(self.centralwidget)
        self.OriginEditLon.setObjectName("OriginEditLon")
        self.OriginEditLon.setValidator(QDoubleValidator(-180.0, 180.0,3,))
        self.OriginEditLon.textChanged.connect(self.textChanged)
        self.horizontalLayout_2.addWidget(self.OriginEditLon)
        self.radiusLabel = QtWidgets.QLabel(self.centralwidget)
        self.radiusLabel.setObjectName("radiusLabel")
        self.horizontalLayout_2.addWidget(self.radiusLabel)
        self.radiusEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.radiusEdit.setObjectName("radiusEdit")
        self.radiusEdit.setValidator(QDoubleValidator(0, 60,3,))
        self.radiusEdit.textChanged.connect(self.textChanged)
        self.horizontalLayout_2.addWidget(self.radiusEdit)
        self.initialization = QtWidgets.QPushButton(self.centralwidget)
        self.initialization.setObjectName("initialization")
        self.initialization.clicked.connect(self.initalizeWaypoints)
        self.initialization.setEnabled(False)
        self.horizontalLayout_2.addWidget(self.initialization)
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
        self.controlLabel.setText(_translate("MainWindow", "Controls"))
        self.originLabelLat.setText(_translate("MainWindow", "Latitude"))
        self.originLabelLon.setText(_translate("MainWindow", "Longitude"))
        self.radiusLabel.setText(_translate("MainWindow", "Radius"))
        self.initialization.setText(_translate("MainWindow", "Enter"))
        self.returnHome.setText(_translate("MainWindow", "Return Home"))
        self.hover.setText(_translate("MainWindow", "Hover")) 
        self.Emerg.setText(_translate("MainWindow", "Emergency Land"))
        self.batteryLabel.setText(_translate("MainWindow", "Battery Power"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionFile.setText(_translate("MainWindow", "File"))
    
    
    def update(self, xml):
        doc = untangle.parse(xml)
        latitude = float(doc.data.gps['latitude'])
        longitude = float(doc.data.gps['longitude'])
        self.coordinates.append([latitude, longitude])
        power = float(doc.data.battery['power'])
        self.batteryProgress.setProperty("value", power)
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.mysignal.emit()
    
    #Add new point to map
    def changeMap(self):
        map_google = maps.Map()
        i = 1;
        for point in self.coordinates:
            if(self.index == i):
                map_google.add_main_point((point[0], point[1]))
            else:
                map_google.add_point((point[0], point[1]))
            i = i+1
        with open("map.html", "w") as out:
            print(map_google, file=out)
        self.map.load(QtCore.QUrl('file:///home/calla/workspace/Gui/src/qtGUI/map.html'))
    
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
    
    def textChanged(self):
        if(not self.initialized):
            if(not self.OriginEditLat.text() or not self.OriginEditLon.text() or not self.radiusEdit.text()):
                self.initialization.setEnabled(False)
            else:
                self.initialization.setEnabled(True)
    
    def initalizeWaypoints(self):
        self.initialized = True
        self.initialization.setEnabled(False)
        lat = float(self.OriginEditLat.text())
        lon = float(self.OriginEditLon.text())
        radius = float(self.radiusEdit.text())
        if(lat < -90.0 or lat > 90.0 or lon <-180 or lon >180):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Origin entered is outside standard latitude/longitude coordinates")
            msg.setWindowTitle("Error with Origin Point")
            msg.exec()
            self.initialized = False
        else:
            for x in range(0,20):
                self.waypoints.append([lat+radius*math.cos(math.radians(18)*x), lon+radius*math.sin(math.radians(18)*x)])
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    w = monitor.Watcher("/home/calla/Input", "/home/calla/Output", "/home/calla/workspace/Gui/src/qtGUI", ui)
    t1 = threading.Thread(target=w.run, daemon=True)
    t1.start()
    sys.exit(app.exec_())
