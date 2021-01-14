import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Material 2.3
import QtQuick.Controls.Universal 2.3
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.0
import QtMultimedia 5.4


// Packages from python

// Packages from JS
import "material_design.js" as MD

import QtQuick 2.0
import PyCVQML 1.0
import cameraFlip 1.0
import faceRecognition 1.0


ColumnLayout{
    anchors.fill : parent
    spacing : 0
    Layout.margins : 0
    width : parent.width
    height : parent.height
    Layout.alignment: Qt.AlignHCenter
    Rectangle{
        Layout.margins : 0
        color:"transparent"
        id : imageShow
        width : parent.width
        height : parent.height - 60
        Item {
            width: parent.width
            height: parent.height
            FaceRecognition{
                id : face_rec
            }
            CVItem  {
                id: imageWriter
                anchors.fill: parent
                image: capture.image
            }
            CVCapture{
                id: capture
                index: 0
                filters : [face_rec]
                Component.onCompleted: capture.start()
            }
        }
    }
    Rectangle{
        Layout.fillWidth : true
        height : 60
        color:"transparent"
        Layout.alignment: Qt.AlignBottom
        id : cap

        RoundButton{
            font.family: iconFont.name
            Material.background : "transparent"
            padding:-5
            font.pixelSize: 40
            Image{
                fillMode : Image.PreserveAspectFit
                sourceSize.width : parent.width - 10
                width : parent.width - 10
                height : parent.height -10
                source:'../assets/img/camera.ico'
                anchors.centerIn : parent
            }
            Layout.alignment: Qt.AlignCenter
            anchors.centerIn : parent
            Material.foreground : Material.Pink
            onClicked : {
                // if (camera.cameraStatus == Camera.ActiveStatus){
                //     camera.stop()
                //     timer.start()
                // }
                // else{
                //     camera.start()
                //     cap.checkStatus()
                // }
                capture.begin()
            }
        }
    }

}
