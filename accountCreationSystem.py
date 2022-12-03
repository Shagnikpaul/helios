import os
import json
import shutil

class acuSystem:
    def __init__(self) -> None:
        print(os.getcwd())

    def serverAccountExists(self, serverID: str) -> bool:
        return os.path.exists(f'servers/{serverID}')

    def userAccountExists(self, userID: str) -> bool:
        return os.path.exists(f'users/{userID}')

    def createUserAccount(self, userID: str, lat: str, lon: str, units:str):
        os.chdir('users')
        os.mkdir(userID)
        os.chdir('../')
        userData = {"lat": lat, "lon": lon, "units": units}
        with open(f"users/{userID}/USER_DATA.json", "w") as outfile:
            json.dump(userData, outfile)

    def createServerAccount(self, serverID: str, API_KEY: str):
        os.mkdir(f'servers/{serverID}')
        serverData = {"API_KEY": API_KEY}
        with open(f"servers/{serverID}/SERVER_DATA.json", "w") as outfile:
            json.dump(serverData, outfile)

    def getServerData(self, serverID: str) -> dict:
        with open(f"servers/{serverID}/SERVER_DATA.json", "r") as outfile:
            data = json.load(outfile)
            return data

    def getUserData(self, userID: str) -> dict:
        with open(f"users/{userID}/USER_DATA.json", "r") as outfile:
            data = json.load(outfile)
            return data

    def delUser(self, userID:str):
        shutil.rmtree(f'users/{userID}')        

    def delServer(self, serverID:str):
        shutil.rmtree(f'servers/{serverID}')  
