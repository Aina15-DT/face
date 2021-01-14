import numpy as np
import threading

import cv2

from PyQt5 import QtCore, QtGui, QtQml
from PIL import Image
gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]

class CvCamera(QtCore.QObject) :

    started = QtCore.pyqtSignal()
    imageReady = QtCore.pyqtSignal()
    indexChanged = QtCore.pyqtSign

    def __init__(self, parent=None):
        super(CvCamera, self).__init__(parent)
        pilImage = Image.open("assets/img/bg.jpg")
        frame = np.array(pilImage)
        # frame = cv2.resize(frame, (self.imageWidth, self.imageHeight), cv2.INTER_AREA)
        self._image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
        # self._image = QtGui.QImage()
        self._index = 0
        self.m_videoCapture = cv2.VideoCapture()
        # self.m_timer = QtCore.QBasicTimer()
        self.m_filters = []
        self.m_busy = False

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(int)
    def start(self, *args):
        if args:
            self.setIndex(args[0])
        self.m_videoCapture.release()
        self.m_videoCapture = cv2.VideoCapture(self._index)
        # if self.m_videoCapture.isOpened():
        #     self.m_timer.start(0, self)
        #     self.started.emit()

    @QtCore.pyqtSlot(np.ndarray)
    def process_image(self, frame):
        self.m_busy = True
        # for f in self.m_filters:
        #     frame = f.process_image(frame)
        image = CvCamera.ToQImage(frame)
        # self.m_busy = False
        QtCore.QMetaObject.invokeMethod(self, "setImage", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(QtGui.QImage, image))

    @staticmethod
    def ToQImage(im):
        if im is None:
            return QtGui.QImage()
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QtGui.QImage(
                    im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_Indexed8)
                qim.setColorTable(gray_color_table)
                return qim.copy()

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    w, h, _ = im.shape
                    rgb_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    flip_image = cv2.flip(rgb_image, 1)
                    qim = QtGui.QImage(flip_image.data, h, w,QtGui.QImage.Format_RGB888)
                    return qim.copy()
        return QtGui.QImage()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if self._image == image:
            return
        self._image = image
        self.imageReady.emit()

    def setIndex(self, index):
        if self._index == index:
            return
        self._index = index
        self.indexChanged.emit()
    
    def image(self):
        return self._image

    def index(self):
        return self._index

    image = QtCore.pyqtProperty(QtGui.QImage, fget=image, notify=imageReady)
    index = QtCore.pyqtProperty(int, fget=index, fset=setIndex, notify=indexChanged)
