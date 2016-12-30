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
import time
import folium
import maps
import threading
import untangle
from shutil import copyfile
from qtGUI import monitor
from geojson import Point
from PyQt5.Qt import pyqtSlot
from PyQt5.Qt import pyqtSignal

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
        
        #map_osm = folium.Map(location=[45.3852, -75.6969], zoom_start=15)
        #folium.CircleMarker([45.3854, -75.6969], radius = 2, color='#3186cc').add_to(map_osm)
        #folium.CircleMarker([45.3852, -75.6966], radius = 2, color='#3186cc').add_to(map_osm)
        #folium.CircleMarker([45.3852, -75.6974], radius = 2, color='#3186cc').add_to(map_osm)
        map_google = maps.Map()
        # Add Beijing, you'll want to use your geocoded points here:
        with open("map.html", "w") as out:
            print(map_google, file=out)
        self.map = QWebView(self.centralwidget)
        self.map.load(QtCore.QUrl('file:///home/calla/workspace/Gui/src/qtGUI/map.html'))
        self.map.setObjectName("map")
        self.verticalLayout.addWidget(self.map)
        self.mysignal.connect(self.changeMap)
        
        
        self.batteryLabel = QtWidgets.QLabel(self.centralwidget)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.returnHome = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnHome.sizePolicy().hasHeightForWidth())
        self.returnHome.setSizePolicy(sizePolicy)
        self.returnHome.setObjectName("returnHome")
        self.horizontalLayout_5.addWidget(self.returnHome)
        self.hover = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hover.sizePolicy().hasHeightForWidth())
        self.hover.setSizePolicy(sizePolicy)
        self.hover.setObjectName("hover")
        self.horizontalLayout_5.addWidget(self.hover)
        spacerItem4 = QtWidgets.QSpacerItem(0, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.label = QtWidgets.QLabel(self.centralwidget)
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
        self.label_3.setText(_translate("MainWindow", "Controls"))
        self.returnHome.setText(_translate("MainWindow", "Return Home"))
        self.hover.setText(_translate("MainWindow", "Hover"))
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
          
    def scrollLeft(self):
        self.index=self.index-1
      
        if self.index < Ui_MainWindow.INDEX_MIN:
            self.index = Ui_MainWindow.INDEX_MAX
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.mysignal.emit()
        
    def scrollRight(self):
        self.index=self.index+1
      
        if self.index > Ui_MainWindow.INDEX_MAX:
            self.index = Ui_MainWindow.INDEX_MIN
        self.image.setPixmap(QtGui.QPixmap(Ui_MainWindow.IMAGE_NAME + str(self.index) + Ui_MainWindow.IMAGE_TYPE))
        self.mysignal.emit()
           
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    w = monitor.Watcher("/home/calla/Input", "/home/calla/Output", "/home/calla/workspace/Gui/src/qtGUI", ui)
    t1 = threading.Thread(target=w.run, daemon=True)
    t1.start()
    sys.exit(app.exec_())
