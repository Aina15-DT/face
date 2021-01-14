
from OpenGL import GL
import sys
from PyQt5 import QtCore, QtGui, QtQml, QtQuick
import cv2

try:
    from PyQt5.QtCore import pyqtWrapperType
except ImportError:
    from sip import wrappertype as pyqtWrapperType


class Singleton(pyqtWrapperType, type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance

class ImageWriter(QtQuick.QQuickPaintedItem, metaclass=Singleton):

    def __init__(self, *args, **kwargs):
        super(ImageWriter, self).__init__(*args, **kwargs)
        self.setRenderTarget(QtQuick.QQuickPaintedItem.FramebufferObject)
        self.cam_frame = QtGui.QImage()

    def paint(self, painter):
        painter.drawImage(0, 0, self.cam_frame)

    def update_frame(self, frame):
        frame = cv2.resize(frame, (700, 500), cv2.INTER_AREA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frame = QtGui.QImage(frame, frame.shape[1], frame.shape[0], 17)
        self.cam_frame = frame.copy()
        self.update()

def get_frames(app):
    cap = cv2.VideoCapture(0)
    num = 0
    imgw = ImageWriter()
    while True:
        while num != 30:
            _, bgframe = cap.read()
            num += 1
        ret, frame = cap.read()
        if ret:
            imgw.update_frame(frame)
            #print("get frames")
            app.processEvents()


if __name__ == '__main__':
    app = QtGui.QGuiApplication(sys.argv)
    QtQml.qmlRegisterType(ImageWriter, "imageWriter", 1, 0, "ImageWriter")
    view = QtQuick.QQuickView()
    view.setSource(QtCore.QUrl('test.qml'))
    rootObject = view.rootObject()
    view.show()
    get_frames(app)
    sys.exit(app.exec_())
