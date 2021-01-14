from PyQt5 import QtCore, QtGui, QtQuick
from PIL import Image
import numpy as np
import cv2


class ImageView(QtQuick.QQuickPaintedItem):

    widthChanged = QtCore.pyqtSignal()
    heightChanged = QtCore.pyqtSignal()
    sourceChanged = QtCore.pyqtSignal()
    _imageWidth = 640
    _imageHeight = 480
    _source = "assets/img/bg.jpg"

    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        # self.setRenderTarget(QtQuick.QQuickPaintedItem.FramebufferObject)
        pilImage = Image.open(self.source)
        frame = np.array(pilImage)
        frame = cv2.resize(frame, (self.imageWidth, self.imageHeight), cv2.INTER_AREA)
        self.im_frame = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)

    def paint(self, painter):
        if self.m_image.isNull():
            return
        image = self.m_image.scaled(self.size().toSize())
        painter.drawImage(QtCore.QPoint(), image)

    def source(self):
        return self._source

    def setSource(self,src):
        if self._source == src:
            return
        self._source = src
        self.sourceChanged.emit()
        self.update()

    def imageWidth(self):
        return self._imageWidth

    def setImageWidth(self, w):
        if self._imageWidth == w:
            return
        self._imageWidth = w
        self.widthChanged.emit()
        self.update()

    def imageHeight(self):
        return self._imageHeight

    def setImageHeight(self, h):
        if self._imageHeight == h:
            return
        self._imageHeight = h
        self.heightChanged.emit()
        self.update()

    source = QtCore.pyqtProperty("QString", fget=source, fset=setSource, notify=sourceChanged)
    imageWidth = QtCore.pyqtProperty(int, fget=imageWidth, fset=setImageWidth, notify=widthChanged)
    imageHeight = QtCore.pyqtProperty(int, fget=imageHeight, fset=setImageHeight, notify=heightChanged)
