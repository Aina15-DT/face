import QtQuick 2.12
import QtQuick.Controls 2.12
import Mywidget 1.0

ApplicationWindow{
    visible : true
    width : 300
    height : 400
    Widget{
        id : self
        Rectangle{
            width : 100
            height : 40
            Text{
                text : self.name
            }
            MouseArea{
                anchors .fill : parent
                onClicked : {
                    self.name = self.name +" OK"
                }
            }
        }
    }
}