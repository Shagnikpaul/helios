from pymongo import MongoClient
import os
from pymongo.collection import Collection

def compare(collection:Collection):
    localCount = len(os.listdir(os.path.join(os.getcwd(), 'users')))
    cloudCount = collection.count_documents({})
    if(localCount == cloudCount):
        print("Local and Cloud have ",cloudCount, " documents.")
        return "e"
    elif(localCount > cloudCount):
        return "l"
    else:
        return "c"