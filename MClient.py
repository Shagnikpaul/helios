
from pymongo import MongoClient
from dbSyncFunctions import dataCompare,dataSync
from dbFunctions.delete import *
from dbFunctions.insert import *
import os
class MClient:
    
    def __init__(self, CONNECTION_URI = 'mongodb://localhost:27017/', DATABASE = 'helios', COLLECTION = 'userdata'):
        
        if os.path.exists('users') == False:
            print("Local database non existent... Aborting MONGO DB sync operations")
            return; 
        self.client = MongoClient(CONNECTION_URI)
        db = self.client[DATABASE]
        self.userdata = db[COLLECTION]
        print("\n\n----------------------------------\n")
        print("LOADED TABLE of \'userdata\'")
        print("- Total entries in the table - ",self.userdata.count_documents({}))
        print("\n----------------------------------\n\n")
  
    def userDataSync(self):
        dataSync.sync(dataCompare.compare(self.userdata), self.userdata)

    def delUserD(self,userId:str):
        deleteUserData(self.userdata, userId)
    
    def addUser(self, data:dict):
        insertUserData(data, self.userdata)
