import os
import json
import shutil
from weatherService import forecast
import weatherService

class acuSystem:
    def __init__(self) -> None:
        print(os.getcwd())

    def serverAccountExists(self, serverID: str) -> bool:
        """## Checks if that particular serverID folder exists in `servers` folder.

        Args:
            serverID (str): Give the server's discord `ID`.

        Returns:
            bool: Returns `True` if exists else `False`.
        """
        return os.path.exists(f'servers/{serverID}')

    def userAccountExists(self, userID: str) -> bool:
        """Checks if that particular userID folder exists in `users` folder.

        Args:
            userID (str): Give the user's discord `ID`.

        Returns:
            bool: Returns `True` if exists else `False`.
        """
        return os.path.exists(f'users/{userID}')

    def createUserAccount(self, userID: str, lat: str, lon: str, units: str):
        """Create a new folder in the `users` folder, containing the `.json` file having the coordinate data.

        Args:
            userID (str): Give the user's discord `ID`
            lat (str): Give your location's latitude.
            lon (str): Give your location's longitude.
            units (str): Give `Imperial` for Fahrenheit, `Metric` for Celcius.
        """
        os.chdir('users')
        os.mkdir(userID)
        os.chdir('../')
        userData = {"lat": lat, "lon": lon, "units": units}
        with open(f"users/{userID}/USER_DATA.json", "w") as outfile:
            json.dump(userData, outfile)

    def createServerAccount(self, serverID: str, API_KEY: str):
        """Create a new folder in the `servers` folder, containing the `.json` file having the `API_KEY`.

        Args:
            serverID (str): Give the server's discord `ID`.
            API_KEY (str): Give your OpenWeatherMap `API_KEY`.
        """
        os.mkdir(f'servers/{serverID}')
        serverData = {"API_KEY": API_KEY}
        with open(f"servers/{serverID}/SERVER_DATA.json", "w") as outfile:
            json.dump(serverData, outfile)

    def getServerData(self, serverID: str) -> dict:
        """Fetches server's json file containing the OpenWeatherMap key.

        Args:
            serverID (str): Give the server's discord `ID`

        Returns:
            dict: Dictionary containing the data.
        """
        with open(f"servers/{serverID}/SERVER_DATA.json", "r") as outfile:
            data = json.load(outfile)   
            return data

    def getUserData(self, userID: str) -> dict:
        """Fetches user's json file containing the coordinate data.

        Args:
            userID (str): Give the user's discord `ID`
        Returns:
            dict: Dictionary containg the user data.
        """
        with open(f"users/{userID}/USER_DATA.json", "r") as outfile:
            data = json.load(outfile)
            return data

    def delUser(self, userID: str):
        """Deletes user data with a particular userID from the `user` folder.

        Args:
            userID (str): Give the user's discord `ID`
        """
        shutil.rmtree(f'users/{userID}')

    def delServer(self, serverID: str):
        """Deletes server data with a particular serverID from the `servers` folder.

        Args:
            serverID (str): Give the server's discord `ID`
        """
        shutil.rmtree(f'servers/{serverID}')

    def createSub(self, channelID:str,lat:str,lon:str,units:str,messageID:str,uID:str,serverID:str):
        
        subInfo = {"channelID":channelID,
                   "lat":lat,
                   "lon":lon,
                   "units":units,
                   "mID":messageID,
                   "uID":uID,
                   "serverID":serverID}
        subInfo.update(forecast(lat_lon=f'{lat},{lon}', units=units))
        if not os.path.exists(f'subscriptions/{serverID}'):
            os.chdir('subscriptions')
            os.mkdir(serverID)
            os.chdir('../')
        with open(f"subscriptions/{serverID}/{channelID}.json", "w") as outfile:
            json.dump(subInfo, outfile)
        print('[INFO] Updating local data...')
        self.weatherInit()
        print('[SUCCESS] Local data updated...')
    
    def getSubInfo(self, channelId:str, serverID:str)-> dict:
        with open(f"subscriptions/{serverID}/{channelId}.json", "r") as outfile:
            data = json.load(outfile)
            return data   



    def weatherInit(self):
        lis = os.listdir('subscriptions')
        for u in lis:
            for subs in os.listdir(f'subscriptions/{u}'):
                
                try:
                    k = self.getSubInfo(channelId=subs[:-5], serverID=u)
                except Exception as e:
                    print('[ERROR] INVALID FORMAT. ',e)
                    continue;
                
                
                if "weatherCondition" in k.keys():
                    pass
                else:
                    with open(f'subscriptions/{u}/{subs}', 'r') as fp:
                        try:
                            data = json.load(fp)
                            weatherdata = weatherService.weatherServices(os.getenv('weatherKey'),data.get("lat"),data.get("lon"),data.get("units"))
                            weatherdata.getData()
                            wea = {
                                "temp":weatherdata.temp,
                                "weatherCondition":weatherdata.weatherCondition,
                                "icon":weatherdata.icon,
                                "humidity":weatherdata.humidity,
                                "windSpeed":weatherdata.windSpeed,
                                "windDirection":weatherdata.windDirection,
                                "feelsLike":weatherdata.feelsLike,
                                "sunriseAt":weatherdata.sunriseAt,
                                "sunsetAt":weatherdata.sunsetAt,
                                "location":weatherdata.location
                            }
                            forecas = weatherService.forecast(lat_lon= f'{data.get("lat")},{data.get("lon")}',units=data.get('units'))
                            with open(f'{fp.name}', "w") as oute:
                                data.update(forecas)
                                data.update(wea)
                                json.dump(data,oute)
                                        
                        except Exception as e:
                            print('[ERROR] Failed to write data to json files of subscriptions.... Details: ',e)