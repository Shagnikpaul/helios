from pymongo.collection import Collection

def deleteUserData(collection:Collection, userID:str) -> None:
    if(collection.count_documents({"userID":userID}) > 0):
        res = collection.delete_one({"userID" :userID})
        print("Successfully deleted userdata for userID = ",userID, res.acknowledged)
    else:
        
        print("Data non existent in Cloud....")

def deleteInvalidData(collection:Collection, id:str) -> None:
    if(collection.count_documents({"_id":id}) > 0):
        res = collection.delete_one({"_id":id})
        print("Successfully deleted the following object with id ", id, res.acknowledged);
    else:
        print("Data non existent in Cloud....")


def purgeAll(collection:Collection):
    collection.delete_many({})
    print("Purged all 💀")