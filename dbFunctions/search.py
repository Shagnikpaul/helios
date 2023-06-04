from pymongo.collection import Collection

def searchUserRecord(collection:Collection, userID:str) -> dict:
    if(collection.count_documents({"userID":userID}) > 0):
        return collection.find_one({"userID":userID})
    else:
        return {"status":"not found"}