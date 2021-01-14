import ctypes
from ctypes import util
ctypes.CDLL(util.find_library('GL'),ctypes.RTLD_GLOBAL)

import os
import sys
import numpy as np
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtQuick import QQuickView
from PyQt5.QtMultimedia import QAbstractVideoFilter,QVideoFilterRunnable,QVideoFrame
import cv2
from packages.image import ImageView
from packages import PyCVQML
import json
import requests
import shutil
from packages.database.database import DatabaseHelper
import pickle
#Face recognition module
from PIL import Image
import face_recognition
#Cryptography
from Crypto.Hash import SHA256
import _thread as thread

database = DatabaseHelper("./assets/data/.face_recognition.sqlite3")
database._open()
database._create("userIdentity")
user_data = database.getall()


class FaceRecognition(PyCVQML.CVAbstractFilter):

    def __init__(self,app):
        super().__init__()

    def loadEncodingFile(self):
        try:
            json_file = open('./assets/data/face_encoding.json', 'rb')
            mon_pickle = pickle.Unpickler(json_file)
            data = mon_pickle.load()
        except Exception as e:
            print(e)
            data = {"encodings": [], "labels": []}
        return data

    def process_image(self,frame):
        #process recognition
        face_names = []
        known_face_encodings_data = self.loadEncodingFile()
        encodings = list(known_face_encodings_data["encodings"])
        labels = list(known_face_encodings_data["labels"])
        frame = cv2.flip(frame,1)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                userid = labels[best_match_index]
                # print(userid +" : "+str(user_data))
                matched_db = [user for user in user_data if user['userId'] == userid]
                # print(matched_db)
                #user_data = database.getById(userid)
                #nom = user_data["name"]
                if len(matched_db) > 0 :
                    rate = round((1 - face_distances[best_match_index])*100,2)
                    name = matched_db[0]['name']+" "+str(rate)+"%"
                face_names.append(name)
            else : print('Not mached')
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            #cv2.rectangle(frame, (left, top), (right, bottom), (194,200,52), 2)
            # Draw a label with a name below the face
            #cv2.rectangle(frame, (left, bottom - 35),(right, bottom), (200,194,52), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_DUPLEX
            radius = 10
            lg = 30
            cv2.line(frame, (left+lg, top-lg), (left+radius, top-lg), (194, 200, 52), 2)
            cv2.line(frame, (left+radius, top-lg), (left, top-lg+radius), (194, 200, 52), 2)
            cv2.line(frame, (left, top-lg+radius), (left, top), (194, 200, 52), 2)

            cv2.line(frame, (left, bottom-lg-radius), (left, bottom-2*radius), (194, 200, 52), 2)
            cv2.line(frame, (left, bottom-2*radius), (left+radius, bottom-radius), (194, 200, 52), 2)
            cv2.line(frame, (left+radius, bottom-radius), (left+lg,bottom-radius), (194, 200, 52), 2)

            cv2.line(frame, (right-lg, top-lg), (right-radius, top-lg), (194, 200, 52), 2)
            cv2.line(frame, (right-radius, top-lg), (right, top-lg+radius), (194, 200, 52), 2)
            cv2.line(frame, (right, top-lg+radius), (right, top), (194, 200, 52), 2)

            cv2.line(frame, (right, bottom-lg-radius), (right, bottom-2*radius), (194, 200, 52), 2)
            cv2.line(frame, (right, bottom-2*radius), (right-radius, bottom-radius), (194, 200, 52), 2)
            cv2.line(frame, (right-radius, bottom-radius), (right-lg,bottom-radius), (194, 200, 52), 2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + radius, bottom - 2*radius),font, 0.5, (255, 255, 255), 1)
        # print('Rocognition ')
        frame = cv2.flip(frame, 1)
        return frame

class CameraFilter(QVideoFilterRunnable):
    def __init__(self,app):
        super().__init__()
        self.database = DatabaseHelper("./assets/data/.face_recognition.sqlite3")
    def run(self,frame,surfaceFormat,flags):
        
        print("run")
        return frame

class CameraFlip(QAbstractVideoFilter):
    def createFilterRunnable(self) :
        return CameraFilter(self)

class MainWindow(QQmlApplicationEngine) :
    def __init__(self,app):
        super().__init__()
        self.app = app
        #self.database = DatabaseHelper("./assets/data/.face_recognition.sqlite3")
        self.cap = None
        self.isOpen = False
        self.load(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),'qml','main.qml')))
        self.rootContext().setContextProperty("MainWindow", self)
        #self.cursor = self.database._open()
        #self.database._create("userIdentity")
        # self.database.delete()

    def addProperty(self,string,value):
        self.rootContext().setContextProperty(string,value)

    # @pyqtSlot('QString')
    # def afficher(self, value):
    #     print(value)
    #     return str(value)+" : "+str(value)

    @pyqtSlot('QString')
    def newUser(self,s_data) :
        hasher = SHA256.new()
        hasher.update(s_data.encode())
        userId =  hasher.hexdigest()
        data = json.loads(s_data)
        print(data)
        tuple_data = (userId, data['name'], data['lastname'], data['work'], data['cin'], data['address'], "./assets/data/"+str(userId)+".jpg")
        print(tuple_data)
        image_path = data['image']
        print(image_path)
        #Processing training
        thread.start_new_thread(self.saveFaceEncoding,(userId, image_path[6:]))
        isSaveUser = database.insert(tuple_data)
        print(isSaveUser)
        user_data = database.getall()
        print(user_data)

    def saveImage(self,userId,url):
        shutil.copyfile(url, './assets/data/'+str(userId)+'.jpg')

    def getFaces(self,image_path):
        if image_path.endswith('.jpeg') or image_path.endswith('.jpg') or image_path.endswith('.png') :
            img = Image.open(image_path)
            img = img.convert('RGB')
            basewidth = 960
            if img.size[0] > basewidth:
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                #img.save(image_path)
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

            print("Face founded "+str(len(face_locations)))
            for i, face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)

    def saveFaceEncoding(self, userId, image_path):
        face_encodings = self.loadEncodingFile()
        encodings = list(face_encodings["encodings"])
        labels = list(face_encodings["labels"])
        try:
            img = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(img)[0]
            encodings.append(list(face_encoding))
            labels.append(userId)
            face_encodings["encodings"] = encodings
            face_encodings["labels"] = labels
            self.saveEncodingFile(face_encodings)
            print("Encodings saved . . .", face_encodings, len(encodings))
            self.saveImage(userId, image_path)
            print('Data Saved')
            return face_encoding
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")


    def saveEncodingFile(self,data):
        with open('./assets/data/face_encoding.json', 'wb') as json_file:
            mon_pickle = pickle.Pickler(json_file)
            mon_pickle.dump(data)

    def loadEncodingFile(self):
        try:
            json_file = open('./assets/data/face_encoding.json', 'rb')
            mon_pickle = pickle.Unpickler(json_file)
            data = mon_pickle.load()
        except Exception as e:
            print(e)
            data = {"encodings": [], "labels": []}
        return data

    # @pyqtSlot()
    # def startCamera(self):
    #     if not self.isOpen:
    #         self.cap = cv2.VideoCapture(0)
    #         self.isOpen = True
    #         imgw = CameraView()
    #         while True:
    #             ret, frame = self.cap.read()
    #             if ret:
    #                 #traitemet de l'image, recognition
    #                 imgw.update_frame(frame)
    #                 self.app.processEvents()
    #             if not self.isOpen :
    #                 break
    #     else :
    #         #save if necessary
    #         self.isOpen = False
    #         self.cap.release()
    #         # self.startCamera()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    PyCVQML.registerTypes()
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    qmlRegisterType(CameraFlip, "cameraFlip", 1, 0, "CameraFlip")
    qmlRegisterType(FaceRecognition, "faceRecognition", 1, 0, "FaceRecognition")
    engine = MainWindow(app)
    engine.quit.connect(app.quit)
    # get_frames(app)
    sys.exit(app.exec_())
