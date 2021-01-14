import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Material 2.3
import QtQuick.Controls.Universal 2.3
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.0
// Packages from JS
import imageView 1.0
import "material_design.js" as MD

ColumnLayout{
    FileDialog {
        id: fileDialog
        title: "Choisissez un image"
        folder: shortcuts.home
        nameFilters: [ "Image files (*.jpg *.png *.jpeg *.gif)", "All files (*)" ]
        onAccepted: {
            console.log("You chose: " + fileDialog.fileUrl)
            var str = fileDialog.fileUrl
            filepath.text = fileDialog.fileUrl
            // path = str.substr(8)
            // console.log(path);
            affichage.source = str
            filepath.focus = false
            // Qt.quit()
        }
        onRejected: {
            console.log("Canceled")
            filepath.focus = false
            // Qt.quit()
        }
        Component.onCompleted: visible = false
    }
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
        Image{
            id : affichage
            Layout.margins : 0
            Layout.fillWidth : true
            width : parent.width
            height : parent.height
            fillMode : Image.PreserveAspectFit
            source : "../assets/img/bg.jpg"
            sourceSize.width : width
            sourceSize.height : height
            antialiasing : true
        }
        // ImageView{
        //     source : "../assets/img/bg.jpg"
        //     imageWidth : parent.width
        //     imageHeight : parent.height
        // }
    }
    Rectangle{
        width : parent.width
        height : 60
        color : "transparent"
        Row{
            Layout.alignment: Qt.AlignVCenter
            width : parent.width
            height : 100
            y : 20
            Rectangle {
                width: 48
                height : 24
                Material.background :"transparent"
                color : "transparent"
                y : 5
                Text{
                    font.family: iconFont.name
                    font.pixelSize: 24
                    text: MD.icons.folder_open
                    anchors.centerIn : parent
                    color : Material.accent
                }
            }
            TextField {
                x : 20
                id: filepath
                placeholderText: "Selectionner un image"
                Layout.margins: 10
                implicitWidth :520
                font.pixelSize: 12
                onPressed : {
                    console.log("Open folder");
                    fileDialog.open()
                }
            }
        }
    }

}
