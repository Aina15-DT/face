import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Material 2.3
import QtQuick.Controls.Universal 2.3
import QtQuick.Layouts 1.11
import QtQuick.Dialogs 1.0
import QtQuick.Window 2.0

// Packages from python

// Packages from JS
import "material_design.js" as MD

ColumnLayout {
    FileDialog {
        id: fileDialog
        title: "Choisissez un image"
        folder: shortcuts.home
        nameFilters: [ "Image files (*.jpg *.png *.jpeg *.gif)", "All files (*)" ]
        onAccepted: {
            console.log("You chose: " + fileDialog.fileUrl)
            var str = fileDialog.fileUrl
            profile.source = str
            // Qt.quit()
        }
        onRejected: {
            console.log("Canceled")
            filepath.focus = false
            // Qt.quit()
        }
        Component.onCompleted: visible = false
    }

    y : 20
    width : parent.width
    Layout.alignment: Qt.AlignHCenter || Qt.AlignVCenter
    spacing : 20
    Row{
        width : parent.width
        Layout.alignment: Qt.AlignHCenter

        Rectangle {
            width: 120
            height : 120
            Material.background :"transparent"
            color : "transparent"
            Layout.alignment: Qt.AlignCenter
            border.width : 2
            border.color : "#cccccc"
            y : 5
            Image{
                Layout.alignment: Qt.AlignCenter
                id : profile
                width : 120
                height : 120
                sourceSize.width : 120
                sourceSize.height : 120
                fillMode : Image.PreserveAspectCrop
                source :"../assets/img/profile.png"

            }
            MouseArea{
                width : parent.width
                height : parent.height

                onClicked : {
                    console.log("Change profile");
                    fileDialog.open()
                }
            }
        }
    }
    Row{
        width : parent.width
        Layout.alignment: Qt.AlignHCenter

        Rectangle {
            width: 48
            height : 24
            Material.background :"transparent"
            color : "transparent"
            y : 5
            Text{
                font.family: iconFont.name
                font.pixelSize: 24
                text: MD.icons.account_circle
                anchors.centerIn : parent
                color : Material.color(Material.Blue)
            }
        }
            TextField {
            x : 20
            id: name
            placeholderText: "Nom"
            Layout.margins: 10
            implicitWidth : 200
            font.pixelSize: 12
            // enabled : false
        }
    }
    Row{
        Layout.alignment: Qt.AlignHCenter
        width : parent.width
        Rectangle {
            width: 48
            height : 24
            Material.background :"transparent"
            color : "transparent"
            y : 5
            Text{
                font.family: iconFont.name
                font.pixelSize: 24
                text: MD.icons.account_circle
                anchors.centerIn : parent
                color :  Material.color(Material.Blue)
            }
        }
        TextField {
            x : 20
            id: lastname
            placeholderText: "Prenom"
            Layout.margins: 10
            implicitWidth : 200
            font.pixelSize: 12
        }
    }
    Row{
        Layout.alignment: Qt.AlignHCenter
        width : parent.width
        Rectangle {
            width: 48
            height : 24
            Material.background :"transparent"
            color : "transparent"
            y : 5
            Text{
                font.family: iconFont.name
                font.pixelSize: 24
                text: MD.icons.fingerprint
                anchors.centerIn : parent
                color :  Material.color(Material.Blue)
            }
        }
        TextField {
            x : 20
            id: cin
            placeholderText: "CIN"
            Layout.margins: 10
            implicitWidth : 200
            font.pixelSize: 12
        }
    }
    Row{
        Layout.alignment: Qt.AlignHCenter
        width : parent.width
        Rectangle {
            width: 48
            height : 24
            Material.background :"transparent"
            color : "transparent"
            y : 5
            Text{
                font.family: iconFont.name
                font.pixelSize: 24
                text: MD.icons.work
                anchors.centerIn : parent
                color :  Material.color(Material.Blue)
            }
        }
        TextField {
            x : 20
            id: work
            placeholderText: "Profession"
            Layout.margins: 10
            implicitWidth : 200
            font.pixelSize: 12
        }
    }
    Row{
        Layout.alignment: Qt.AlignHCenter
        width : parent.width
        Rectangle {
            width: 48
            height : 24
            Material.background :"transparent"
            color : "transparent"
            y : 5
            Text{
                font.family: iconFont.name
                font.pixelSize: 24
                text: MD.icons.location_on
                anchors.centerIn : parent
                color :  Material.color(Material.Blue)
            }
        }
        TextField {
            x : 20
            id: address
            placeholderText: "Adresse"
            Layout.margins: 10
            implicitWidth : 200
            font.pixelSize: 12
        }
    }
    Row{
        Layout.alignment: Qt.AlignHCenter
        width : parent.width
        Rectangle {
            width: 48
            height : 24
            Material.background :"transparent"
            color : "transparent"
            y : 5
        }
        Button{
            id : save
            width : 200
            text : "Enregistrer"
            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 40
                opacity: enabled ? 1 : 0.3
                color: save.down ? "#d0d0d0" : Material.color(Material.Pink)
                radius : 5
            }
            onClicked : {
                var userData = '{"name" : "'+name.text+'","lastname" : "'+lastname.text+'","work" : "'+work.text+'","cin" : "'+cin.text+'","address" : "'+address.text+'","image":"'+profile.source+'"}'
                console.log(userData);
                MainWindow.newUser(userData)
                name.text = ""
                lastname.text = ""
                cin.text = ""
                address.text = ""
                work.text = ""
                profile.source = "../assets/img/logo.jpg"
            }

        }
    }
    
}
