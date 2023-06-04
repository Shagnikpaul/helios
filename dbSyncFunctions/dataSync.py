import json
import os
from pymongo.collection import Collection
from dbFunctions.delete import deleteInvalidData

def sync(code:str, collection:Collection):
    if code == "e":
        print("Cloud and Local data is already synced...")
        pass
    elif code == "l":
        print("Cloud data behind Local... Uploading extra local files to MongoDB")
        users = os.listdir('users')
        c = 0
        for userID in users:
            if(collection.count_documents({"userID":userID}) == 0):
                c+=1
                with open(f"users/{userID}/USER_DATA.json", "r") as outfile:
                    data = json.load(outfile)
                    data = {"lat": data['lat'], "lon":data['lon'], "units":data['units'], "userID":userID}
                    collection.insert_one(data).inserted_id
            else:
                pass
        print("Uploaded ",c," more files to cloud.")
    else:   # cloud has more
        c = 0
        lis = collection.find({})
        for data in lis:
            try:
                if(os.path.exists(os.path.join(os.getcwd(), 'users', data['userID']))):
                    pass

                else:
                    c+=1
                    os.mkdir(f"users/{data['userID']}")
                    del data['_id']
                    with open(os.path.join(os.getcwd(), "users", data['userID'],"USER_DATA.json"), "w") as outfile:
                        json.dump(data, outfile)
            except KeyError:
                print("Not a valid user data entry. Proceeding to delete the following entry. ",data['_id'])
                deleteInvalidData(collection, data['_id'])

        print("Total ",c," files downloaded from cloud.")


    