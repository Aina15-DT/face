from PyQt5.QtCore import QUrl,pyqtProperty,pyqtSignal,pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlComponent
from PyQt5.QtQuick import QQuickItem
import sys
class Widget(QQuickItem):
    _name = "MonNom"
    def __init_(self,parent=None) :
        super().__init__(parent)
        self._name = ""
        print("New widget ha,dle create with name : "+str(self._nom))

    nameChanged = pyqtSignal()

    @pyqtProperty('QInt', notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self,new_name):
        self._name = new_name
        self.nameChanged.emit()

    @pyqtSlot(str,name="change")
    def change(self,value):
        print("Catched : "+str(value))
        print(self.name)
        self.name = "Changement de nom " + value
        print(self._name)


qmlRegisterType(Widget, 'Mywidget', 1, 0, 'Widget')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load('test.qml')
sys.exit(app.exec_())
