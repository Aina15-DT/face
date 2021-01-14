
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

ApplicationWindow {
    id : root
    // x: 200
    // y: 200
    visible: true
    title: "Face recognition"
    width: Screen.width
    height: Screen.width
    // maximumHeight: height
    // maximumWidth: width
    // minimumHeight: height
    // minimumWidth: width
    Material.theme: Material.Light
    Material.accent: Material.Teal
    Material.primary : Material.Teal
    Component.onCompleted: {
        setX((Screen.width / 2) - (width / 2));
        setY((Screen.height / 2 )- (height / 2));
    }
    FontLoader {
        id: iconFont
        source: "../assets/fonts/MaterialIcons-Regular.ttf"
    }
    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            ToolButton {
                text: qsTr("‹")
                onClicked: stack.pop()
            }
            Label {
                text: "Reconnaissance faciale Python"
                elide: Label.ElideRight
                horizontalAlignment: Qt.AlignHCenter
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
            }
            ToolButton {
                text: qsTr("⋮")
                onClicked: menu.open()
            }
        }
    }
    
    StackView{
        id: stackMain
        initialItem: cameraloader
        x : 200
        width:parent.width - 560
        height: parent.height
        Component{
            id : imageloader
            Pane {
                width:parent.width 
                height: parent.height
                Material.elevation: 6
                Layout.margins : 0
                padding : 6
                anchors.centerIn: parent
                
                Loader{
                    anchors.left : parent.left
                    anchors.right : parent.right
                    anchors.top : parent.top
                    anchors.bottom : parent.bottom
                    source : "image.qml"
                
                }
            }
        }
        Component{
            //progress: real
            //status: enumeration
            //url: url
            //onCompleted: { }
            //onDestruction: { }
             id : listloader
            Pane {
                width:parent.width
                height: parent.height
                Material.elevation: 6
                Layout.margins : 0
                anchors.centerIn: parent
                padding : 6
               
                Loader{
                    anchors.left : parent.left
                    anchors.right : parent.right
                    anchors.top : parent.top
                    anchors.bottom : parent.bottom
                    source : "liste.qml"
                
                }
            }
        }
        Component{
           
            id : cameraloader
            Pane {
                y : 200
                width:parent.width 
                height: parent.height
                Material.elevation: 6
                Layout.margins : 0
                padding : 6
                anchors.centerIn: parent
                Rectangle{
                    width:parent.width
                    height: parent.height
                    Loader{
                        anchors.left : parent.left
                        anchors.right : parent.right
                        anchors.top : parent.top
                        anchors.bottom : parent.bottom
                        source : "camera.qml"
                    
                    }
                    
                }
            }
        }
    }
    
    Pane {
        width:200
        height: parent.height
        Material.elevation:6
        Layout.fillWidth: true
        Layout.margins : 0
        y : 5
        // anchors.horizontalCenter: parent.horizontalCenter
        padding : 0
        ColumnLayout{
            Layout.margins:0
            // anchors.verticalCenter: parent.verticalCenter
            Layout.alignment: Qt.AlignHCenter
            width : parent.width
            spacing : -5
            Image{
                y : 10
                width : parent.width
                source :'../assets/img/logo.svg'
                fillMode:Image.PreserveAspectCrop
                sourceSize.width : 200
            }
            Row{
                width : parent.width
                Layout.topMargin : 20
                Rectangle{
                    property bool alredyClicked : true
                    id : btn1
                    width : 200
                    height : 36
                    // Material.background : Material.Teal
                    color : mouseLoad1.containsMouse || alredyClicked ? Material.color(Material.Teal) : "transparent"
                    Row{
                        Rectangle {
                            width: 48
                            height : 24
                            Material.background :"transparent"
                            color : "transparent"
                            y : 5
                            Text{
                                font.family: iconFont.name
                                font.pixelSize: 24
                                text: MD.icons.camera
                                anchors.centerIn : parent
                                color : Material.color(Material.Blue)
                            }
                        }
                        Text{
                            y : 8
                            font.bold : true
                            font.pixelSize: 14
                            text: "Recognition"
                            color : "#cccccc"
                        }
                    }
                    MouseArea{
                        anchors.fill: parent
                        id : mouseLoad1
                        hoverEnabled : true
                        onClicked: {
                            // loader.source = "image.qml"
                            console.log("Loader source change ");
                            btn3.color = "transparent"
                            btn2.color = "transparent"
                            btn1.color  =  Material.color(Material.Teal)
                            //loader.source = "camera.qml")
                            stackMain.push(cameraloader)
                            //capture.stop()
                            btn1.alredyClicked = true
                            btn2.alredyClicked = false
                            btn3.alredyClicked = false
                        }
                        onEntered : {
                            btn1.color  =  Material.color(Material.Teal)
                        }
                        onExited :{
                            if (!btn1.alredyClicked) btn1.color  =  "transparent"
                        }
                    }
                }
            }
            Row{
                width : parent.width
                Layout.topMargin : 4
                Rectangle{
                    id : btn2
                    property bool alredyClicked : false
                    width : 200
                    height : 36
                    Material.background : Material.Teal
                    color : mouseLoad2.containsMouse ? Material.color(Material.Teal) : "transparent"
                    Row{
                        Rectangle {
                            width: 48
                            height : 24
                            Material.background :"transparent"
                            color : "transparent"
                            y : 5
                            Text{
                                font.family: iconFont.name
                                font.pixelSize: 24
                                text: MD.icons.image
                                anchors.centerIn : parent
                                color : Material.accent
                            }
                        }
                        Text{
                            y : 8
                            font.bold : true
                            font.pixelSize: 14
                            text: "Load Image"
                            color : "#cccccc"
                        }
                    }
                    MouseArea{
                        anchors.fill: parent
                        id : mouseLoad2
                        hoverEnabled : true
                        onClicked: {
                            //loader.source = "image.qml"
                            console.log("Loader source change ");
                            btn3.color = "transparent"
                            btn2.color  =  Material.color(Material.Teal)
                            btn1.color = "transparent"
                            // capture.stop()
                            // loader.source = "image.qml"
                            //capture.stop()
                            stackMain.push(imageloader)
                            btn1.alredyClicked = false
                            btn2.alredyClicked = true
                            btn3.alredyClicked = false
                        }
                        onEntered : {
                            btn2.color  =  Material.color(Material.Teal)
                        }
                        onExited :{
                            if (!btn2.alredyClicked) btn2.color  =  "transparent"
                        }
                    }
                }
            }
            Row{
                width : parent.width
                Layout.topMargin : 4
                Rectangle{
                    id : btn3
                    property bool alredyClicked : false
                    width : 200
                    height : 36
                    Material.background : Material.Teal
                    color : mouseLoad3.containsMouse ? Material.color(Material.Teal) : "transparent"
                    Row{
                        Rectangle {
                            width: 48
                            height : 24
                            Material.background :"transparent"
                            color : "transparent"
                            y : 5
                            Text{
                                font.family: iconFont.name
                                font.pixelSize: 24
                                text: MD.icons.list
                                anchors.centerIn : parent
                                color : Material.color(Material.Pink)
                            }
                        }
                        Text{
                            y : 8
                            font.bold : true
                            font.pixelSize: 14
                            text: "Liste des bases"
                            color : "#cccccc"
                        }
                    }
                    MouseArea{
                        anchors.fill: parent
                        id : mouseLoad3
                        hoverEnabled : true
                        onClicked: {
                            // loader.source = "image.qml"
                            console.log("Loader source change ");
                            btn3.color  =  Material.color(Material.Teal)
                            btn2.color = "transparent"
                            btn1.color = "transparent"
                            // capture.stop()
                            // loader.source = "liste.qml"
                            capture.stop()
                            stackMain.push(listloader)
                            btn1.alredyClicked = false
                            btn2.alredyClicked = false
                            btn3.alredyClicked = true
                        }
                        onEntered : {
                            btn3.color  =  Material.color(Material.Teal)
                        }
                        onExited :{
                            if (!btn3.alredyClicked) btn3.color  =  "transparent"
                        }
                    }
                }
            }
        }
    }
    Pane {
        x : parent.width - 360
        width:360
        height: parent.height
        Material.elevation:6
        Layout.fillWidth: true
        Layout.margins : 0
        anchors.verticalCenter: parent.verticalCenter
        // Material.background : Material.Teal
        padding : 0
        Loader{
            id : userId
            anchors.left : parent.left
            anchors.right : parent.right
            anchors.top : parent.top
            // anchors.bottom : parent.bottom
            source : "newUser.qml"
        }
    }
    footer: Pane {
        // Material.background : Material.Teal
        Material.elevation : 6
        Layout.alignment : Qt.AlignRight
        RowLayout{
            Layout.alignment: Qt.AlignRight
            width : parent.width
            Item{
                Layout.fillWidth: true
                // implicitWidth : parent.width
                Button{
                    id:buttonAbout
                    background:Rectangle{
                        color:"transparent"
                    }
                }
            }
            Rectangle {
                width: 20
                height : 16
                Material.background :"transparent"
                color : "transparent"
                Text{
                    font.family: iconFont.name
                    font.pixelSize: 18
                    text: MD.icons.copyright
                    anchors.centerIn : parent
                    color : Material.accent
                }
            }
            Label {
                // font.bold: true
                font.pixelSize: 12
                minimumPixelSize: 6
                fontSizeMode: Label.Fit
                visible : true
                text: "Copyright reserved Milà"
                // Material.background: Material.color(Material.Red)
            }
        }
    }
}
