from OpenGL import GL
import sys
from PyQt5 import QtCore, QtGui, QtQml, QtQuick
from PyQt5.QtCore import QUrl, pyqtProperty, pyqtSignal, pyqtSlot
import numpy as np
import cv2
import os
from PIL import Image


class ImageView(QtQuick.QQuickPaintedItem):

    _imageWidth = 640
    _imageHeight = 480
    _source = "assets/img/bg.jpg"

    def __init__(self, *args, **kwargs):
        print("Init called")
        super(ImageView, self).__init__(*args, **kwargs)
        # self.setRenderTarget(QtQuick.QQuickPaintedItem.FramebufferObject)
        if self.source  == "" :
                self.cam_frame = QtGui.QImage()
                print("Source null")
        else :
            try :
                pilImage = Image.open(self.source)
                frame = np.array(pilImage)
                frame = cv2.resize(frame, (self.imageWidth, self.imageHeight), cv2.INTER_AREA)
                # frame = cv2.imread("assets/img/bg.jpg",0)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                # frame = cv2.flip(frame, 1)
                self.cam_frame = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
            except Exception as e :
                print("Exception e : "+str(e))
                self.cam_frame = QtGui.QImage()

    widthChanged = pyqtSignal()
    heightChanged = pyqtSignal()
    sourceChanged = pyqtSignal()

    @pyqtProperty(int, notify=widthChanged)
    def imageWidth(self):
        return self._imageWidth

    @imageWidth.setter
    def imageWidth(self, new_width):
        self._imageWidth = new_width
        self.widthChanged.emit()
        self.update()

    @pyqtProperty(int, notify=heightChanged)
    def imageHeight(self):
        return self._imageHeight

    @imageHeight.setter
    def imageHeight(self, new_height):
        self._imageHeight = new_height
        self.heightChanged.emit()
        self.update()

    @pyqtProperty("QString", notify=sourceChanged)
    def source(self):
        return self._source

    @source.setter
    def source(self, new_source):
        self._source = new_source
        self.sourceChanged.emit()
        self.update()

    def paint(self, painter):
        painter.drawImage(0, 0, self.cam_frame)


