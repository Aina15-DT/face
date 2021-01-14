import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Material 2.3
import QtQuick.Controls.Universal 2.3
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.0
// Packages from JS
// import imageView 1.0
import "material_design.js" as MD


ListView {
    spacing : 10
    populate: Transition {
        NumberAnimation { properties: "x,y"; duration: 300 }
    }
    ListModel {
        id : list
        ListElement {
            name: "Bill Smith"
            number: "555 3264"
        }
        ListElement {
            name: "John Brown"
            number: "555 8426"
        }
        ListElement {
            name: "Sam Wise"
            number: "555 0473"
        }
    }
    width: 180; height: 200
    model: list
    delegate: Pane{
        width : parent.width
        height : 60
        Material.elevation: 6
        padding : 0
        // radius : 4
        Row{
            spacing : 20
            width : parent.width
            height : 60
            Column{
                anchors.verticalCenter: parent.verticalCenter
                Rectangle{
                    x : 4
                    width : 50
                    height : 50
                    radius : 25
                    Image{
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        source : '../assets/img/logo.jpg'
                        fillMode : Image.PreserveAspectFit
                        width : parent.width - 10
                        height : parent.height
                        sourceSize.width : parent.width
                        sourceSize.height : parent.width
                    }
                }
            }
            Column{
                spacing : 5
                anchors.verticalCenter: parent.verticalCenter
                Text {
                    text: '<b>Name:</b> ' + name;
                    width: 160
                    font.pixelSize: 12
                    color : "#cccccc"
                }
                Text {
                    text: '<b>Number:</b> ' + number;
                    width: 160
                    font.pixelSize: 12
                    color : "#cccccc"
                }
            }
        }
    }
}
