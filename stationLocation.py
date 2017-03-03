'''
        Created on Jan 23, 2017
        
        @author: calla
        '''
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *

class StationLocation(QtCore.QObject):
    latitude = 0.0
    longitude = 0.0

    def __init__(self):
        super(StationLocation, self).__init__()
    @QtCore.pyqtSlot(float, float)
    def updateLoc(self,lat,long):
        self.latitude = lat
        self.longitude = long
        print(self.latitude, self.longitude)