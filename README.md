
![Logo](https://github.com/Shagnikpaul/helios/blob/main/images/banner.png)


<h1 align="center">🌞 Hi I am Helios.</h1>
<p align="center">I am an easy-to-use discord weather bot. I fetch data from <a href="https://openweathermap.org/api">OpenWeatherMap</a> API and then generate a Weather card based on that data and display it to the user through a discord embed.</p>

<p align="center">
<a href="https://discord.com/api/oauth2/authorize?client_id=1045392740499853312&permissions=2147600384&scope=bot%20applications.commands"><img src="https://github.com/Shagnikpaul/helios/blob/main/images/button.png" width=150px align="center"></a>
<a href="https://discord.com/api/oauth2/authorize?client_id=1045392740499853312&permissions=2147600384&scope=bot%20applications.commands"><img src="https://github.com/Shagnikpaul/helios/blob/main/images/button.png" width=150px align="center"></a>
<a href="https://discord.com/api/oauth2/authorize?client_id=1045392740499853312&permissions=2147600384&scope=bot%20applications.commands"><img src="https://github.com/Shagnikpaul/helios/blob/main/images/button.png" width=150px align="center"></a>  
</p>


<br><br>

<h1 align="center">❓ How to use the bot.</h1>
<br>


<h2>🔧 First time setup.</h2>
<ul>
  <li>Firstly, invite the bot to your server and also give it the required permissions while doing so.</li>
  <li>Go to <a href="https://openweathermap.org/api">OpenWeatherMap</a> create a new account, generate a new API_KEY from your 'profile section' of the website.</li>
  <li>Wait for 10-15 mins for the API_KEY to get activated before you can use it in the bot.</li>
  <li>Run the following slash command with API_KEY</li>
  
  <br>
  
  
  
  
```python 
/server-setup

# API_KEY required.   
```
  <li>Now run the following slash command with location and weather forecast units you want.</li>
  
  
  <br>
  
  
```python 
/user-setup

# location and units required.   
```

 <li>Now you can start using the bot.</li>
  
</ul> 

<br>
<h2>🟢 General usage.</h2>
<p>After completing the setup run the following slash command to get weather.</p>


```python 
/weather 
```


<h2>*️⃣ Other commands.</h2>
<p>List of all commands supported by the bot can be obtained by running the following slash command.</p>


```python 
/help-helios   
```
<br>
<h1 align="center">😎 Host the bot locally.</h1>
<p>Sometimes hosting services don't work properly or just randomly shut down resulting in bot becoming offline and in that case no one can invite the bot to their 
server and use it. So if you have an old spare computer why not use it to host this bot for your own use? Following are the instructions on how to do so.</p>
<br>




<ul>
  <li>First of all, create a bot account and invite your bot to your server. Here's a brief <a href="https://discordpy.readthedocs.io/en/stable/discord.html">guide</a> on how to do so.</li>
  <li>Download and install the latest version of <a href="https://www.python.org/downloads/">Python</a>.</li>
  <li>Clone the repository and navigate to that repository folder.</li>
 <br>
 

```
git clone https://github.com/Shagnikpaul/helios.git
cd helios
```

 <li>Inside the root directory, create a <code>.env</code> file and put the following tokens.</li>
 <br>
 
 
 ```
botToken=
latlonAPIKEY=
```
 
  <li><code>botToken</code> is your discord bot token. Here's a <a href="https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs#how-to-get-a-bot-token">guide</a> on how to get it.</li>
  <li><code>latlonAPIKEY</code> is your positionstack API KEY required for searching a particular location's latitude and longitute. Get it <a href="https://positionstack.com/signup/free">here</a>.</li>
  <li>Open terminal <b>in the root/project directory</b>.</li> 
 <li>Install the required dependencies by running the following command in the terminal.</li>
 
 <br>
 
 
 ```
pip install -r requirements.txt
```

 <li>Start the bot by running the following command in the terminal.</li>
 <br>
 
 ```
python main.py
```
<li>Your bot is now ready for use! Refer to <a href="https://github.com/Shagnikpaul/helios#-how-to-use-the-bot">Bot Commands</a> for setting up the bot for server use.</li>
</ul>
<br>
<h1 align="center">😇 Contributing.</h1>
<p align="center"><b>All contributions are welcome! Just try to make meaningful contributions to the code, no goofy aah scripts or malware please 🤓</b></p>
<br>
<h2>📖 Instructions</h2>
<ul>
  <li>Follow the first few steps given in <a href="https://github.com/Shagnikpaul/helios#-host-the-bot-locally">Bot Hosting</a>.</li>
  <li>Start developing. 🤯</li>
</ul>
<br>
<h1 align="center">🌟 Python Libraries and APIs used in this Project.</h1>
<br>
<ul>
  <li><a href="https://github.com/nextcord/nextcord">NextCord</a> for... yes you guessed it <b>tO connECT tO disCORd APi. 🤯</b></li>
  <li><a href="https://pypi.org/project/Pillow/">Pillow</a> to generate the weather cards.</b></li>
  <li><a href="https://pypi.org/project/python-dotenv/">Python-dotenv</a> to hide API keys and tokens from Romanian Citizens.</li>
  <li><a href="https://pypi.org/project/requests/">Python-requests</a> to request some <del>bit**es</del> I mean data from REST APIs.</li>
  <li><a href="https://openweathermap.org/api">OpenWeatherMap</a> for weather data.</li>
  <li><a href="https://positionstack.com/">Position Stack</a> for geolocation data.</li>
</ul>
<br>
<h1 align="center">🚨 License.</h1>
<br>


```
MIT License

Copyright (c) 2022 Shagnik Paul

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
