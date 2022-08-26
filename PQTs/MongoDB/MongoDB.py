# -*- coding: utf-8 -*-

import pymongo

from PQTs.Utilizar import UrlDB,accountsDB

class MongoDB:

    def __init__(self):
        self.UrlDB = UrlDB
        self.accountsDB = accountsDB
        self.Client = None
        self.DB = None

    def iniciarDB(self):
        self.Client = pymongo.MongoClient(self.UrlDB)
        self.DB = self.Client[self.accountsDB]

    def insertOne(self,coleccion,dato):
        self.DB[coleccion].insert_one(dato)

    def insertMany(self,coleccion,dato):
        self.DB[coleccion].insert_many(dato)

    def find(self,coleccion,dato):
        return list(self.DB[coleccion].find(dato))

    def findOne(self,coleccion,dato):
        return self.DB[coleccion].find_one(dato)

    def updateOne(self,coleccion,id,actualizar):
        self.DB[coleccion].update_one({"_id": id},{"$set":actualizar})

    def cerrarConexion(self,):
        self.Client.close()