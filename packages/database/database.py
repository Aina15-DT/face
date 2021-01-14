import sqlite3
import os

class DatabaseHelper(object) :

    def __init__(self,name) :
        self.dbname = name
        self.connexion = sqlite3.connect(self.dbname)

    def _open(self) :
        self.cursor = self.connexion.cursor()

    def _create(self,table_name):
        self.table_name = table_name
        sql_request = """CREATE TABLE IF NOT EXISTS """+str(table_name)+""" (
            id integer PRIMARY KEY AUTOINCREMENT,
            user_id text NOT NULL,
            name text NOT NULL,
            lastname text,
            cin integer NOT NULL,
            work text,
            address text NOT NULL,
            image text NOT NULL
        )
        """
        self.cursor = self.connexion.cursor()
        a = self.cursor.execute(sql_request)
        self.connexion.commit()
        
        return a

    def insert(self,data):
        sql_request = """
            INSERT INTO """+str(self.table_name)+""" (user_id,name,lastname,cin,work,address,image) VALUES (?,?,?,?,?,?,?)
        """
        self.cursor = self.connexion.cursor()
        rep = self.cursor.execute(sql_request,data)
        self.connexion.commit()
        

    def getall(self):
        sql_request = """SELECT * FROM """+str(self.table_name)
        self.cursor = self.connexion.cursor()
        self.cursor.execute(sql_request)
        data = self.cursor.fetchall()
        self.connexion.commit()
        user_data = []
        for d in data :
            user = {}
            user['id'] = d[0]
            user['userId'] = d[1]
            user['name'] = d[2]
            user['lastname'] = d[3]
            user['work'] = d[4]
            user['cin'] = d[5]
            user['adress'] = d[6]
            user['profile'] = d[7]
            user_data.append(user)
        return user_data

    def getById(self,userId):
        sql_request = """SELECT * FROM """+str(self.table_name)+""" WHERE user_id = ?"""
        self.cursor = self.connexion.cursor()
        self.cursor.execute(sql_request, (userId))
        data = self.cursor.fetchone()
        self.connexion.commit()
        
        return  data

    def update(self,userId,data) :
        sql_request = """UPGDATE """+str(self.table_name)+""" SET (user_id,name,lastname,cin,work,address,image) VALUES (?,?,?,?,?,?,?) WHERE user_id = """+str(userId)
        self.cursor = self.connexion.cursor()
        data = self.cursor.execute(sql_request, data)
        self.connexion.commit()
        
        return data

    def delete(self,userId) :
        sql_request = """DELETE FROM """+str(self.table_name)+""" WHERE user_id = ?"""
        self.cursor = self.connexion.cursor()
        self.cursor.execute(sql_request, (userId,))
        self.connexion.commit()
        

