from pymongo.collection import Collection

def insertUserData(data:dict, collection:Collection):
    if(data.get('userID') == None):
        print("Faulty data not matching the schema.")
    else:
        if(collection.count_documents({"userID":data['userID']}) > 0):
            print("Data already exists skipping insertion.")
        else:
            collection.insert_one(data)
            print("1 record inserted....")
