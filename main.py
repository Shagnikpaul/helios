from dotenv import load_dotenv
from nextcord.ext import commands, tasks
from nextcord import SlashOption, abc
import nextcord
import json
import shutil
import threading
import os
import weatherService
from weatherService import weatherServices as accountManager
from typing import Optional
from datetime import datetime
from accountCreationSystem import acuSystem as accountManager
import imageGenerator
from cooldowns import SlashBucket
from cooldowns import CallableOnCooldown
import cooldowns
import time
from random import randint
import asyncio


load_dotenv()
firstTime = True
intents = nextcord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!w', intents=intents, help_command=None)

accountManager = accountManager()
server_count: int = 0
quote_list = ["Vote me on Top.gg", "/help-helios | !whelp",
              "check out my weather feed feature! (type /help-helios for more info)", 'leave a comment on my Top.gg profile']


class AboutLinks(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None
        self.add_item(nextcord.ui.Button(label="💖 VOTE ME (TOP.GG)",
                      url="https://top.gg/bot/1045392740499853312/vote"))
        self.add_item(nextcord.ui.Button(label="📝 REVIEW ME",
                      url="https://top.gg/bot/1045392740499853312"))
        self.add_item(nextcord.ui.Button(label="💛 VOTE ME (DISCORDBOTS.GG)",
                      url="https://discord.bots.gg/bots/1045392740499853312"))
        self.add_item(nextcord.ui.Button(label="😳 INVITE ME",
                      url="https://top.gg/bot/1045392740499853312/invite"))              

def kek():
    pass


class SupportLinks(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None
        self.add_item(nextcord.ui.Button(label="MY COMMANDS",
                      url="https://shagniks-organization.gitbook.io/helios-weather-bot/"))
        self.add_item(nextcord.ui.Button(label="DISCORD SERVER",
                      url="https://discord.gg/QeeQaJtJ3q"))


class MinimalLinks(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None
        self.add_item(nextcord.ui.Button(label="💖 VOTE ME",
                      url="https://top.gg/bot/1045392740499853312/vote"))
 


class Confirmation(nextcord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="YES", style=nextcord.ButtonStyle.green)
    async def yes(self,  button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()
        button.disabled = True

    @nextcord.ui.button(label="NO", style=nextcord.ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction,):
        self.value = False
        self.stop()
        button.disabled = True

@bot.event
async def on_message_delete(message: nextcord.Message):
    if os.path.exists(f'subscriptions/{message.guild.id}/{message.channel.id}.json'):
        acco = accountManager.getSubInfo(channelId=str(
            message.channel.id), serverID=str(message.guild.id))
        if not acco.get('mID') == str(message.id):
            return
        c: nextcord.TextChannel = bot.get_channel(int(acco.get('channelID')))
        try:
            await c.send(embed=nextcord.Embed(color=nextcord.Colour.brand_red(), title="ERROR", description='Original message was deleted. Weather feed configuration was removed. Re-run the `/set-weather-channel` to restore the feed.'))
        except:
            pass
        os.remove(
            f'subscriptions/{message.guild.id}/{message.channel.id}.json')


@bot.event
async def on_guild_channel_delete(channel: abc.GuildChannel):
    if os.path.exists(f'subscriptions/{channel.guild.id}/{channel.id}.json'):
        os.remove(f'subscriptions/{channel.guild.id}/{channel.id}.json')
    pass


@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    if (isinstance(error, nextcord.errors.NotFound)):
        await interaction.send(content='no')
    if (isinstance(error, nextcord.errors.Forbidden)):
        await interaction.send(embed=nextcord.embeds.Embed(title="MISSING PERMISSONS !", description="Make sure"))

    error = getattr(error, "original", error)
    if isinstance(error, CallableOnCooldown):
        await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title=f"WAIT FOR {error.retry_after} SECONDS.",
                                                                                               description=f"This command is rate-limited per user. Please wait before you can use it again.")
                               .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png'), ephemeral=True)
    else:
        raise error


@bot.event
async def on_command_error(interaction: nextcord.Interaction, error):
    if (isinstance(error, nextcord.errors.Forbidden)):
        await interaction.send(embed=nextcord.embeds.Embed(title="MISSING PERMISSONS !", description="Make sure"))


@tasks.loop(minutes=35)
async def embedUpdate():
    count = len(bot.guilds)
    if randint(2, 3) % 2 == 0:
        if (count <= 1):
            await bot.change_presence(activity=nextcord.Game(name=quote_list[randint(0, (len(quote_list)-1))]))
        else:
            await bot.change_presence(activity=nextcord.Game(name=quote_list[randint(0, (len(quote_list)-1))]))
    else:
        if (count <= 1):
            await bot.change_presence(activity=nextcord.Game(name=f"/weather in {len(bot.guilds)} server"))
        else:
            await bot.change_presence(activity=nextcord.Game(name=f"/weather in {len(bot.guilds)} servers"))
    lis = os.listdir('subscriptions')
    c = 0
    for u in lis:
        for subs in os.listdir(f'subscriptions/{u}'):
            c+=1
            t = asyncio.create_task(update(u,subs))       
    print(f'[TASK : SUCEEDED] Embeds Updated for a total of {c} subscriptions')
    
    

async def update(u,subs):
    print('[INFO] updating')
    acco = accountManager.getSubInfo(channelId=subs[:-5], serverID=u)
    c: nextcord.TextChannel = bot.get_channel(int(acco.get('channelID')))
    # channel editing part
    try:
        tx = ''
        if(acco.get('temp')[0] =='-'):
            tx='minus'
        await c.edit(name=(tx+acco.get('temp')+'-'+acco.get('location')))
    except nextcord.errors.Forbidden:
        try:
            m: nextcord.Message = await c.fetch_message(int(acco.get('mID')))
            await m.edit(embed=nextcord.Embed(color=nextcord.Colour.brand_red(), title="Missing Manage Channel permissions !"))
            return
        except:
            try:
                os.remove(
                    f'subscriptions/{acco.get("serverID")}/{acco.get("channelID")}.json')

            except:
                return
    # if channel does not exists
    except AttributeError:
        try:
            os.remove(
                f'subscriptions/{acco.get("serverID")}/{acco.get("channelID")}.json')
            return
        except:
            print('CRITICAL DELETION ERROR')
            return

    except Exception as e:
        # unknown shit occured.
        print('[ERROR] Not known error.', e)

    # message editing part
    if str(c.type) == 'voice':
            return
    try:
        m: nextcord.Message = await c.fetch_message(int(acco.get('mID')))
        imageGenerator.createImageSub(
        acco.get('temp'), acco.get('weatherCondition'), acco.get('icon'), acco.get('location'), acco.get('channelID'), acco.get('serverID'))
        emb = nextcord.embeds.Embed(colour=nextcord.Colour.from_rgb(
            r=47, g=49, b=54), title=f"Current Weather Data. (Updated <t:{round(time.time())}:R>)", description="\u200B")
        emb.add_field(name="Humidity",
                    value=f"``` {acco.get('humidity')} %  ```", inline=True)
        emb.add_field(name="Feels Like",
                    value=f"``` {acco.get('feelsLike')}  ```", inline=True)
        emb.add_field(name="\u200B", value="\u200B", inline=False)
        emb.add_field(name="Wind Speed",
                    value=f"``` {acco.get('windSpeed')} m/s  ```", inline=True)
        emb.add_field(name="Wind Direction",
                    value=f"``` {acco.get('windDirection')}  ```", inline=True)
        emb.add_field(name="\u200B", value="\u200B", inline=False)
        emb.add_field(name="Sunrise at",
                    value=f"<t:{acco.get('sunriseAt')}:t>", inline=True)
        emb.add_field(name="Sunset at",
                    value=f"<t:{acco.get('sunsetAt')}:t>", inline=True)
        emb.set_footer(text=f"Like the bot? A review or a vote on my Top.gg profile would be appreciated. Thank You UwU",
                    icon_url="https://em-content.zobj.net/thumbs/120/toss-face/342/red-heart_2764-fe0f.png")
        emb.set_image(f'attachment://{acco.get("channelID")}.png')
        file = nextcord.File(
            f'subimages/{acco.get("channelID")}.png', filename=f'{acco.get("channelID")}.png')
        await m.edit(embed=emb, file=file, view= MinimalLinks())
    
    
    
    except nextcord.errors.NotFound:
        try:
            try:
                c: nextcord.TextChannel = bot.get_channel(
                    int(acco.get('channelID')))
                await c.send(embed=nextcord.Embed(color=nextcord.Colour.brand_red(), title="ERROR", description='Original message was deleted. Weather feed configuration was removed. Re-run the `/set-weather-channel` to restore the feed.'))
            except:
                print('Error sending message. Maybe missing send_messages permission.')
                pass
            os.remove(
                f'subscriptions/{acco.get("serverID")}/{acco.get("channelID")}.json')
        except:
            return
    except Exception as e:
        # unknown shit occured.
        print('[ERROR] Not known error. ', e)
    

        # lis = os.listdir('subscriptions')
        # cou = 0
        # for u in lis:
        #     for subs in os.listdir(f'subscriptions/{u}'):
        #         cou += 1
        #         k = accountManager.getSubInfo(channelId=subs[:-5], serverID=u)
        #         if "maxT" in k.keys():
        #             pass
        #         else:
        #             with open(f'subscriptions/{u}/{subs}', 'r+') as fp:
        #                 await fUpdater(fp.name)
        #         # if os.path.exists(f'forecast/server_{u}_{subs}'):
        #         #     pass
        #         # else:
        #         #     with open(f'forecast/server_{u}_{subs}', 'w') as fp:
        #         #         json.dump({"lat_lon" : f"{k.get('lat')},{k.get('lon')}", 
        #         #                     "units":f"{k.get('units')}"}
        #         #                     ,fp)
        #         t = asyncio.create_task(updater(k))
        # print(
        #     f'Updated weather feeds for {cou} subscribers in a total of {len(lis)} servers')



# @tasks.loop(minutes=127)
# async def forecastUpdater():
#     global firstTime
#     if firstTime:
#         firstTime=False
#         return
#     lis = os.listdir('subscriptions')
#     for u in lis:
#         for subs in os.listdir(f'subscriptions/{u}'):
#             t = asyncio.create_task(fUpdater(f'subscriptions/{u}/{subs}'))
#     print('forecasts updated...')








@tasks.loop(minutes=27)
async def localWeatherDataUpdater():
    global firstTime
    if firstTime:
        print(f'[TASK : SKIPPED] Not updating local files for first time....')
        firstTime = False
        pass
    else:
        print(f'[TASK] Updating local files...')
        weatherUpdater()
        print(f'[TASK : SUCEEDED] Updated local files...')



@bot.event
async def on_ready():
    print(f'[SUCCESS] We have logged in as {bot.user}')
    count = len(bot.guilds)
    if (count <= 1):
        await bot.change_presence(activity=nextcord.Game(name=f"/weather in {len(bot.guilds)} server"))
    else:
        await bot.change_presence(activity=nextcord.Game(name=f"/weather in {len(bot.guilds)} servers"))
    print('[INFO] Now Playing status updated...')
    embedUpdate.start()
    localWeatherDataUpdater.start()

@bot.event
async def on_guild_remove(guild: nextcord.Guild):
    if os.path.exists(f'subscriptions/{guild.id}'):
        shutil.rmtree(f'subscriptions/{guild.id}')

    if accountManager.serverAccountExists(serverID=str(guild.id)):
        accountManager.delServer(serverID=(str)(guild.id))
        print(datetime.now().ctime(),
              f" DELETED SERVER DATA OF {guild.name} ({guild.id})")
    else:
        print(datetime.now().ctime(),
              f" I LEFT (NO EXISTING SERVER DATA) {guild.name} ({guild.id})")


    



@bot.command(name='help')
async def helps(ctx: commands.Context):
    print(datetime.now().ctime(),
          f" RAN COMMAND {ctx.command.name} in {ctx.author.guild.name} by {ctx.author.name}#{ctx.author.discriminator}")
    emb1 = nextcord.Embed(colour=nextcord.Colour.teal(), title='MY COMMANDS', description='Visit this GitBook Docs page for complete list of commands and detailed tutorials.').set_thumbnail('https://media.tenor.com/W-CbMoHi0ckAAAAj/information-symbols.gif')
    views = SupportLinks()
    await ctx.send(embed=emb1, view=views)


@bot.slash_command(name='help-helios', description="List all available commands of Helios bot with description.", guild_ids=bot.default_guild_ids)
async def helpCommand(interaction: nextcord.Interaction):
    logTheCommand(interaction=interaction)
    views = SupportLinks()
    await interaction.send(embed=nextcord.Embed(colour=nextcord.Colour.teal(), title='MY COMMANDS', description='Visit this GitBook Docs page for complete list of commands and detailed tutorials.').set_thumbnail('https://media.tenor.com/W-CbMoHi0ckAAAAj/information-symbols.gif'), view=views)


@bot.slash_command(name='list-feed-channels', description="List all the weather-feed channels currently in your server.", guild_ids=bot.default_guild_ids)
async def listFeeds(interaction: nextcord.Interaction):
    if os.path.exists(f'subscriptions/{interaction.guild.id}'):
        l = len(os.listdir(f'subscriptions/{interaction.guild.id}'))
        lis = os.listdir(f'subscriptions/{interaction.guild.id}')
        c = 1
        tx = ''
        for k in lis:
            tx += f'**{c}.** '+'<#'+k[:-5]+'> ' + \
                f'**configured by** <@{accountManager.getSubInfo(channelId=k[:-5], serverID=str(interaction.guild_id)).get("uID")}>'+'\n'
            c += 1
        f = ''
        if l != 1:
            f = 'feeds'
        else:
            f = 'feed'
        emb = nextcord.Embed(title="LIST OF WEATHER FEED CHANNELS",
                             description=f'This server currently has **{l} {f}** running. \n \n{tx}')
        emb.set_thumbnail(
            url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/input-numbers_1f522.png')
        await interaction.send(embed=emb)
    else:
        l = 0
        f = 'feeds'
        emb = nextcord.Embed(title="LIST OF WEATHER FEED CHANNELS",
                             description=f'This server currently has **{l} {f}** running.')
        emb.set_thumbnail(
            url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/input-numbers_1f522.png')
        await interaction.send(embed=emb)


@bot.slash_command(name="delete-weather-channel", description="Delete existing weather feed text, thread or a voice channel.", guild_ids=bot.default_guild_ids)
async def delSubChannel(interaction: nextcord.Interaction,
                        textchannel: Optional[nextcord.TextChannel] = SlashOption(required=False, name='textchannel', description='Existing weather feed text channel name.'),
                        threadchannel: Optional[nextcord.Thread] = SlashOption(required=False, name='thread', description='Existing weather feed thread name.'),
                        voicechannel: Optional[nextcord.VoiceChannel] = SlashOption(required=False, name='voicechannel', description='Existing weather feed voice channel name.')):
    c=3
    i=3
    channelname = None
    if textchannel == None:
        c-=1
    if threadchannel == None:
        c-=1
    if voicechannel == None:
        c-=1
    if c == 0:
        await interaction.send(embed=nextcord.Embed(color=nextcord.Colour.gold(), title="💀☠🤓" , description=f"Choose atleast one option from the {i}. Come on bro.")
        .set_thumbnail('https://media.tenor.com/xCc58fEqFREAAAAM/nerd-nerdy.gif')
        .add_field(name='PRO GAMER TIP', value='Press `TAB` key on the key board to show the available options.'))
        return
    if c > 1:
        await interaction.send(embed=nextcord.Embed(color=nextcord.Colour.gold(), title="💀☠🤓" , description=f"Choose atmost one option out of {i} not more than 1. Come on bro.")
        .set_thumbnail('https://media.tenor.com/xCc58fEqFREAAAAM/nerd-nerdy.gif'))
        return
    if not textchannel == None:
        channelname = textchannel
    elif not threadchannel == None:
        channelname = threadchannel
    elif not voicechannel == None:
        channelname = voicechannel
    
    if os.path.exists(f'subscriptions/{channelname.guild.id}/{channelname.id}.json'):
        os.remove(
            f'subscriptions/{channelname.guild.id}/{channelname.id}.json')
        await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description=f"Weather feed of <#{channelname.id}> was deleted")
                               .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png'))

    else:
        await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="ERROR.", description=f"No weather feed was configured for <#{channelname.id}>")
                               .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/cross-mark_274c.png'))










async def forumNewThread(interaction:nextcord.Interaction, 
                forum:nextcord.ForumChannel,
                location:str,
                units:str):
    
    logTheCommand(interaction=interaction)
    if not permissionChecker(member=interaction.channel.guild.me)[0]:
        await interaction.send(embed=permissionChecker(interaction.channel.guild.me)[1])
        return
    try:
        channelname = await forum.create_thread(name='Weather', auto_archive_duration=None,content=f'Weather for {interaction.user.display_name}{interaction.user.discriminator}')
    except:
        await interaction.send(embed=nextcord.Embed(colour=nextcord.Colour.brand_red(), title='ERROR', description='I cannot setup weather feed in a Forum where selecting tags are necessary to post threads. Disable it to proceed.')
        .add_field(name='How to disable it.', value='Go to Forum settings then scroll down to tags section and disable the following option.')
        .set_image('https://i.imgur.com/31qxn40.png'))    
        return
    await threadWeatherSetup(interaction=interaction,location=location,units=units,channelname=channelname)


@bot.slash_command(name='set-weather-feed', description='Setup bot to send weather feed in a thread, text channel or in a forum thread.', guild_ids=bot.default_guild_ids)
async def ultimate(interaction:nextcord.Interaction,
                    location: Optional[str] = SlashOption(required=True, description="Enter your town or city name. Don't give your exact address 💀"),
                    units: Optional[str] = SlashOption(name='units', required=True, choices={"Celcius": "Metric", "Fahrenheit": "Imperial"}), 
                    channelNewThread:Optional[nextcord.TextChannel] = SlashOption(name='channelforthread', description='The channel in which the weather thread should be created.',required=False),
                    forum:Optional[nextcord.ForumChannel] = SlashOption(name='forum', description='The forum in which the weather thread should be created.',required=False),
                    existingThread:Optional[nextcord.Thread] = SlashOption(name='existingthread', description='The already existing thread in which weather will be sent.',required=False),
                    textChannel:Optional[nextcord.TextChannel] = SlashOption(name='textchannel' , description='A particular text channel where you want the weather.', required=False),
                    voiceChannel:Optional[nextcord.VoiceChannel] = SlashOption(name='voicechannel' , description='A particular voice channel of whose name will be weather info.', required=False)):
    
    logTheCommand(interaction=interaction)
    c = 5
    i = c
    if channelNewThread == None:
        c-=1
    if forum == None:
        c-=1
    if existingThread == None:
        c-=1
    if textChannel == None:
        c-=1
    if voiceChannel == None:
        c-=1
    if c == 0:
        await interaction.send(embed=nextcord.Embed(color=nextcord.Colour.gold(), title="💀☠🤓" , description=f"Choose atleast one option from the {i}. Come on bro.")
        .set_thumbnail('https://media.tenor.com/xCc58fEqFREAAAAM/nerd-nerdy.gif')
        .add_field(name='PRO GAMER TIP', value='Press `TAB` key on the key board to show the available options.'))
        return
    if c > 1:
        await interaction.send(embed=nextcord.Embed(color=nextcord.Colour.gold(), title="💀☠🤓" , description=f"Choose atmost one option out of {i} not more than 1. Come on bro.")
        .set_thumbnail('https://media.tenor.com/xCc58fEqFREAAAAM/nerd-nerdy.gif'))
        return
    
    
    if not channelNewThread == None:
        await threadSubscribeCommand(interaction=interaction, location=location,units=units,channel=channelNewThread)
        return
    
    if not forum == None:
        await forumNewThread(interaction=interaction, forum=forum, location=location, units=units)
        return
    
    if not existingThread == None:
        await threadExistingSubscribeCommand(interaction=interaction, location=location,units=units,channel=existingThread)
        return

    if not textChannel == None:
        await subscribeCommand(interaction=interaction, location=location,units=units,channelname=textChannel)
        return
    
    if not voiceChannel == None:
        await subscribeCommand(interaction=interaction, location=location,units=units,channelname=voiceChannel)
        return








async def threadSubscribeCommand(interaction:nextcord.Interaction,
                            location:str,
                            units: str, 
                            channel:nextcord.TextChannel):
    
    if not permissionChecker(member=interaction.channel.guild.me)[0]:
        await interaction.send(embed=permissionChecker(interaction.channel.guild.me)[1])
        return
    mes = await channel.send(content=f'Weather for {interaction.user.display_name}')
    channelname = await channel.create_thread(name=location, message=mes, auto_archive_duration=10080, reason=f'weather for {interaction.user.name},{interaction.user.discriminator}')
    await threadWeatherSetup(interaction=interaction,location=location,units=units,channelname=channelname)








async def threadExistingSubscribeCommand(interaction:nextcord.Interaction,
                            location:str,
                            units:str, 
                            channel:nextcord.Thread):
    
    if not permissionChecker(member=interaction.channel.guild.me)[0]:
        await interaction.send(embed=permissionChecker(interaction.channel.guild.me)[1])
        return
    await threadWeatherSetup(interaction=interaction,location=location,units=units,channelname=channel)






async def subscribeCommand(interaction: nextcord.Interaction,
                           location:str,
                           units:str,
                           channelname:nextcord.TextChannel):
    typeofchannel = str(channelname.type)
    if not permissionChecker(member=interaction.channel.guild.me)[0]:
        await interaction.send(embed=permissionChecker(interaction.channel.guild.me)[1])
        return
    if os.path.exists(f'subscriptions/{interaction.guild_id}/{channelname.id}.json'):
        await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                           description=f"Existing Weather feed configuration was found for <#{channelname.id}>. If you want to change the location or any other setting first delete the current configuration by running the following command and then again re-run `/set-weather-channel` command.")
                               .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                               .add_field(name="First run this one.", value="``` /delete-weather-channel  ```", inline=False), ephemeral=True)
        return

    if not accountManager.userAccountExists(userID=str(interaction.user.id)):
        await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title='No existing user account found.',
                                                           description='You dont have any user account setup yet. Run the following command first.')
                               .add_field(name='Run the command below', value='``` /user-setup ```'))
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="YOU TRIED.", description="Bro is trying to run an `admin-only` command with no admin rights ☠ What an absolute clown. First obtain Administrator `Role` or `Permission` then try to run this command.")
                               .set_thumbnail('https://media.discordapp.net/attachments/926366898520739903/1047225277941559367/unknown.png'), ephemeral=True)
        return
    if os.path.exists(f'subscriptions/{channelname.guild.id}'):
        if len(os.listdir(f'subscriptions/{channelname.guild.id}')) >= 10:
            await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title='MAX LIMIT REACHED',
                                                               description='For now you can have upto 10 weather feeds per server and currently you have 10 feeds active.'))
            return
    await interaction.send(embed=nextcord.embeds.Embed(title="Searching your given location.", description="Just a moment....")
                           .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/face-with-monocle_1f9d0.png'), ephemeral=True)
    coord = weatherService.geoCode(location=location)
    if coord != None:
        views = Confirmation()
        await interaction.edit_original_message(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="CONFIRMATION.",
                                                                            description="Please check the location detected and confirm it by clicking the **Confirmation Button** below. (Some fields might show None)")
                                                .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                                                .add_field(name="Region", value=f"``` {coord.get('region')} ```", inline=False)
                                                .add_field(name="Street", value=f"``` {coord.get('street')} ```", inline=False)
                                                .add_field(name="County", value=f"``` {coord.get('county')} ```", inline=False)
                                                .add_field(name="Country", value=f"``` {coord.get('country')} ```", inline=False)
                                                .set_footer(text='Location not matching? Try giving nearby city or town name.'), view=views)
        await views.wait()
        if views.value == None:
            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="ERROR.", description="You did not respond to the question within 5 minutes!")
                                                    .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/cross-mark_274c.png'))
        elif views.value:

            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description=f"New weather feed subscription added successfully! Weather will get updated automatically in <#{channelname.id}> soon, wait for about 20-25 mins.")
                                                    .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png'))
            if typeofchannel == 'voice':
                sentone = await channelname.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="I WILL BE UPDATING THE WEATHER INFO AS NAME OF THIS VOICE CHANNEL.",
                                                                         description="For god's sake **do not** delete this text message or I will stop updating the weather. 🤓")
                                             .set_thumbnail(url='https://media.discordapp.net/attachments/1037609462405537862/1046979036318019635/WOAH.png'))
            else:
                sentone = await channelname.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="I WILL BE UPDATING WEATHER HERE  ☠",
                                                                         description="Can you believe it?")
                                             .set_thumbnail(url='https://media.discordapp.net/attachments/1037609462405537862/1046979036318019635/WOAH.png'))
            accountManager.createSub(
                channelID=str(channelname.id), lat=coord.get('lat'), lon=coord.get('lon'), units=units, messageID=str(sentone.id), uID=str(interaction.user.id), serverID=str(interaction.guild_id))
            k = 10 - len(os.listdir(f'subscriptions/{channelname.guild.id}'))
            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description=f"New weather feed subscription added successfully! Weather will get updated automatically in <#{channelname.id}> soon, wait for about 20-25 mins.")
                                                    .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png')
                                                    .set_footer(text=f'{k} Weather channels left.'))

        else:
            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                                                           description="User profile creation was cancelled.")
                                                    .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png'))

    else:
        await interaction.edit_original_message(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="WHAT DA HEEEEEEEEEELLLL  ☠",
                                                                            description="Can you believe it? The location you gave **does not f\*\*king exist in the Google Maps** 💀. Either you are trolling or you are using discord from OHIO bruh.")
                                                .set_thumbnail(url='https://media.discordapp.net/attachments/1037609462405537862/1046979036318019635/WOAH.png')
                                                .add_field(name="Location you gave :", value=f"``` {location}  ```", inline=False))


@bot.slash_command(name="server-setup", description="Setup the bot with default weather settings same for all the members of the server", guild_ids=bot.default_guild_ids)
async def serversetupCommand(interaction: nextcord.Interaction,
                             api_key: Optional[str] = SlashOption(required=True, description="Give your OpenWeatherMap API Key")):
    logTheCommand(interaction=interaction)
    if (accountManager.serverAccountExists(str(interaction.guild_id))):
        await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                           description="Existing server configuration was found. If you want to change the `API_KEY` then run the following command followed by the server setup command")
                               .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                               .add_field(name="First run this one.", value="``` /delete-server-data  ```", inline=False), ephemeral=True)
    else:
        await interaction.send(embed=nextcord.embeds.Embed(title="Checking your API_KEY", description="Just a moment....")
                               .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/face-with-monocle_1f9d0.png'), ephemeral=True)
        if weatherService.checkAPIKey(API_KEY=api_key):
            await interaction.edit_original_message(embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description="Server settings has been saved. Setup your location if you have not done else you are ready to run the weather command!")
                                                    .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png')
                                                    .add_field(name="Setup your location", value="``` /user-setup ```", inline=False)
                                                    .add_field(name="All setup done? Get your weather.", value="``` /weather ```", inline=False))
            accountManager.createServerAccount(
                serverID=str(interaction.guild_id), API_KEY=api_key)
        else:
            await interaction.edit_original_message(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="WHAT DA HEEEEEEEEEELLLL",
                                                                                description="Bro give your OpenWeatherMap API KEY not your bank account number ☠")
                                                    .set_thumbnail(url='https://media.discordapp.net/attachments/1037609462405537862/1046979036318019635/WOAH.png')
                                                    .add_field(name="How do I get the API Key ?",
                                                               value="Go to [OpenWeatherMap Website](https://openweathermap.org/) create a free account go to your profile get the API_KEY (it will take atleast 5-10 mins to get activated before you can use the key), then run the server setup command.")
                                                    .add_field(name="Run this command.", value="``` /server-setup ```", inline=False))


@bot.slash_command(name="user-setup", description="Configure the bot to get the weather of your own loction.", guild_ids=bot.default_guild_ids)
async def usersetupCommand(interaction: nextcord.Interaction,
                           location: Optional[str] = SlashOption(
                               required=True, description="Enter your town or city name. Don't give exact address 💀"),
                           units: Optional[str] = SlashOption(name='units', required=True, choices={"Celcius": "Metric", "Fahrenheit": "Imperial"})):
    logTheCommand(interaction=interaction)
    if (accountManager.userAccountExists(userID=str(interaction.user.id))):
        await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                           description="You have already setup your location. If you want to change your location then first delete your existing configuration and then again run this command.")
                               .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                               .add_field(name="First run the following command.", value="``` /delete-user ```", inline=False)
                               .add_field(name="> Then run this one.", value="``` /user-setup ```", inline=False), ephemeral=True)
    else:
        await interaction.send(embed=nextcord.embeds.Embed(title="Searching your given location.", description="Just a moment....")
                               .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/face-with-monocle_1f9d0.png'), ephemeral=True)
        coord = weatherService.geoCode(location=location)
        if coord != None:
            views = Confirmation()
            await interaction.edit_original_message(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="CONFIRMATION.",
                                                                                description="Please check the location detected and confirm it by clicking the **Confirmation Button** below. (Some fields might show None)")
                                                    .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                                                    .add_field(name="Region", value=f"``` {coord.get('region')} ```", inline=False)
                                                    .add_field(name="Street", value=f"``` {coord.get('street')} ```", inline=False)
                                                    .add_field(name="County", value=f"``` {coord.get('county')} ```", inline=False)
                                                    .add_field(name="Country", value=f"``` {coord.get('country')} ```", inline=False)
                                                    .set_footer(text='Location not matching? Try giving nearby city or town name.'), view=views)
            await views.wait()
            if views.value == None:
                await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="ERROR.", description="You did not respond to the question within 5 minutes!")
                                                        .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/cross-mark_274c.png'))
            elif views.value:
                await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description="Your location profile has been created and saved.")
                                                        .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png')
                                                        .add_field(name="All setup done? Get your weather.", value="``` /weather ```", inline=False))
                accountManager.createUserAccount(
                    userID=str(interaction.user.id), lat=coord.get('lat'), lon=coord.get('lon'), units=units)

            else:
                await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                                                               description="User profile creation was cancelled.")
                                                        .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png'))

        else:
            await interaction.edit_original_message(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="WHAT DA HEEEEEEEEEELLLL  ☠",
                                                                                description="Can you believe it? The location you gave **does not f\*\*king exist in the Google Maps** 💀. Either you are trolling or you are using discord from OHIO bruh.")
                                                    .set_thumbnail(url='https://media.discordapp.net/attachments/1037609462405537862/1046979036318019635/WOAH.png')
                                                    .add_field(name="Location you gave :", value=f"``` {location}  ```", inline=False))


@bot.slash_command(name="about-me", description="Get info regarding the bot and the developer of the bot", guild_ids=bot.default_guild_ids)
async def aboutCommand(interaction: nextcord.Interaction):
    views = AboutLinks()
    logTheCommand(interaction=interaction)
    emb = nextcord.embeds.Embed(title="Hi. I am Helios. 👋",
                                description="I am an easy-to-use discord weather bot. I fetch data from OpenWeatherMap and display it to the user. I am still under developement and will get new features soon in the future.")
    emb.add_field(name="I was developed by",
                  value="```Shagnik Paul```", inline=False)
    emb.add_field(name="Language used", value="```Python```", inline=True)
    emb.add_field(name="Library used",
                  value="```Nextcord Library```", inline=True)
    emb.add_field(name="Developer's Discord Tag",
                  value="```RicardoSenGupta#9839```", inline=False)
    emb.add_field(name="Developer's GitHub page link",
                  value="```https://github.com/Shagnikpaul```", inline=False)
    emb.set_image(
        'https://media.discordapp.net/attachments/926366898520739903/1047216245717598258/banner4.png?width=967&height=616')
    await interaction.send(embed=emb, ephemeral=True, view=views)


@bot.slash_command(name="delete-user-data", description="Delete your location profile from the server.", guild_ids=bot.default_guild_ids)
async def delUser(interaction: nextcord.Interaction):
    logTheCommand(interaction=interaction)
    if (accountManager.userAccountExists(userID=str(interaction.user.id))):
        accountManager.delUser(userID=str(interaction.user.id))
        await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description="Your location profile has been deleted from the server.")
                               .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png'), ephemeral=True)
    else:
        await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="ERROR.", description="You don't have any profile setup yet.")
                               .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/cross-mark_274c.png'), ephemeral=True)


@bot.slash_command(name="delete-server-data", description="Delete server configuration.", guild_ids=bot.default_guild_ids)
async def delServer(interaction: nextcord.Interaction):
    logTheCommand(interaction=interaction)
    if interaction.user.guild_permissions.administrator:
        if (accountManager.serverAccountExists(serverID=str(interaction.guild_id))):
            accountManager.delServer(serverID=str(interaction.guild_id))
            await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description="Server configuration was successfully deleted.")
                                   .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png'), ephemeral=True)
        else:
            await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="ERROR.", description="No server configuration was created before.")
                                   .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/cross-mark_274c.png'), ephemeral=True)
    else:
        await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="YOU TRIED.", description="Bro is trying to run an `admin-only` command with no admin rights ☠ What an absolute clown. First obtain Administrator `Role` or `Permission` then try to run this command.")
                               .set_thumbnail('https://media.discordapp.net/attachments/926366898520739903/1047225277941559367/unknown.png'), ephemeral=True)


@bot.slash_command(name="weather", description="Get weather.", guild_ids=bot.default_guild_ids)
@cooldowns.cooldown(1, 60, bucket=SlashBucket.author)
async def weatherCommand(interaction: nextcord.Interaction):
    logTheCommand(interaction=interaction)
    if (accountManager.serverAccountExists(str(interaction.guild_id))):
        if (accountManager.userAccountExists(userID=str(interaction.user.id))):
            await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.blue(), title="Fetching your data...", description="Please wait it might take some time.")
                                   .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/clockwise-vertical-arrows_1f503.png'))
            emb = weatherEmbBuilder(interaction=interaction)
            file = nextcord.File(
                f'users/{interaction.user.id}/imf.png', filename='imf.png')
            await interaction.edit_original_message(embed=emb, file=file)

        else:
            await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                               description="You have not setup your location. Please run the user setup command:")
                                   .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                                   .add_field(name="Run the following command.", value="``` /user-setup ```", inline=False), ephemeral=True)
    else:
        if (accountManager.userAccountExists(userID=str(interaction.user.id))):
            await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.blue(), title="Fetching your data...", description="Please wait it might take some time.")
                                   .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/clockwise-vertical-arrows_1f503.png'))
            emb = weatherEmbBuilder(interaction=interaction)
            file = nextcord.File(
                f'users/{interaction.user.id}/imf.png', filename='imf.png')
            await interaction.edit_original_message(embed=emb, file=file, view=MinimalLinks())
        else:
            await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                               description="You have not setup your location. Please run the user setup command:")
                                   .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                                   .add_field(name="Run the following command.", value="``` /user-setup ```", inline=False), ephemeral=True)

        # await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
        #                                                    description="No existing server configuration was found. Please get a OpenWeatherMap API key by creating a new account (or existing). Then run the server setup command.")
        #                        .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
        #                        .add_field(name="Run the following command.", value="``` /server-setup ```", inline=False), ephemeral=True)





async def threadWeatherSetup(interaction:nextcord.Interaction, location:str,units:str,channelname:nextcord.Thread):
    if not accountManager.userAccountExists(userID=str(interaction.user.id)):
        await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title='No existing user account found.',
                                                           description='You dont have any user account setup yet. Run the following command first.')
                               .add_field(name='Run the command below', value='``` /user-setup ```'))
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="YOU TRIED.", description="Bro is trying to run an `admin-only` command with no admin rights ☠ What an absolute clown. First obtain Administrator `Role` or `Permission` then try to run this command.")
                               .set_thumbnail('https://media.discordapp.net/attachments/926366898520739903/1047225277941559367/unknown.png'), ephemeral=True)
        return
    if os.path.exists(f'subscriptions/{channelname.guild.id}'):
        if len(os.listdir(f'subscriptions/{channelname.guild.id}')) >= 10:
            await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title='MAX LIMIT REACHED',
                                                               description='For now you can have upto 10 weather feeds per server and currently you have 10 feeds active.'))
            return
    await interaction.send(embed=nextcord.embeds.Embed(title="Searching your given location.", description="Just a moment....")
                           .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/face-with-monocle_1f9d0.png'), ephemeral=True)
    coord = weatherService.geoCode(location=location)
    if coord != None:
        views = Confirmation()
        await interaction.edit_original_message(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="CONFIRMATION.",
                                                                            description="Please check the location detected and confirm it by clicking the **Confirmation Button** below. (Some fields might show None)")
                                                .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
                                                .add_field(name="Region", value=f"``` {coord.get('region')} ```", inline=False)
                                                .add_field(name="Street", value=f"``` {coord.get('street')} ```", inline=False)
                                                .add_field(name="County", value=f"``` {coord.get('county')} ```", inline=False)
                                                .add_field(name="Country", value=f"``` {coord.get('country')} ```", inline=False)
                                                .set_footer(text='Location not matching? Try giving nearby city or town name.'), view=views)
        await views.wait()
        if views.value == None:
            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="ERROR.", description="You did not respond to the question within 5 minutes!")
                                                    .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/cross-mark_274c.png'))
        elif views.value:

            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description=f"New weather feed subscription added successfully! Weather will get updated automatically in <#{channelname.id}> soon, wait for about 20-25 mins.")
                                                    .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png'))
            sentone = await channelname.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="I WILL BE UPDATING WEATHER HERE  ☠",
                                                                         description="Can you believe it?")
                                             .set_thumbnail(url='https://media.discordapp.net/attachments/1037609462405537862/1046979036318019635/WOAH.png'))
            accountManager.createSub(
                channelID=str(channelname.id), lat=coord.get('lat'), lon=coord.get('lon'), units=units, messageID=str(sentone.id), uID=str(interaction.user.id), serverID=str(interaction.guild_id))
            k = 10 - len(os.listdir(f'subscriptions/{channelname.guild.id}'))
            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description=f"New weather feed subscription added successfully! Weather will get updated automatically in <#{channelname.id}> soon, wait for about 20-25 mins.")
                                                    .set_thumbnail('https://images.emojiterra.com/mozilla/128px/2705.png')
                                                    .set_footer(text=f'{k} Weather channels left.')
                                                    .add_field(name='IMPORTANT NOTE', value='After the thread has been created do send a text message in that thread (just type anything) so that the thread becomes visible in your left side channel list and also you will be able to delete the subscription in the thread if needed later.'))

        else:
            await interaction.edit_original_message(view=None, embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
                                                                                           description="User profile creation was cancelled.")
                                                    .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png'))

    else:
        await interaction.edit_original_message(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="WHAT DA HEEEEEEEEEELLLL  ☠",
                                                                            description="Can you believe it? The location you gave **does not f\*\*king exist in the Google Maps** 💀. Either you are trolling or you are using discord from OHIO bruh.")
                                                .set_thumbnail(url='https://media.discordapp.net/attachments/1037609462405537862/1046979036318019635/WOAH.png')
                                                .add_field(name="Location you gave :", value=f"``` {location}  ```", inline=False))
    







def weatherEmbBuilder(interaction: nextcord.Interaction):
    keyUsed = ""
    u = accountManager.getUserData(userID=str(interaction.user.id))
    if accountManager.serverAccountExists(str(interaction.guild_id)):
        keyUsed = "Server API_KEY"
        w = weatherService.weatherServices(accountManager.getServerData(
            serverID=str(interaction.guild_id)).get("API_KEY"), u.get('lat'), u.get('lon'), u.get('units'))
    else:
        keyUsed = "Global API_KEY"
        w = weatherService.weatherServices(
            os.getenv('weatherKey'), u.get('lat'), u.get('lon'), u.get('units'))
    w.getData()
    imageGenerator.createImage(
        (w.temp), w.weatherCondition, w.icon, w.location, str(interaction.user.id))
    emb = nextcord.embeds.Embed(colour=nextcord.Colour.from_rgb(
        r=47, g=49, b=54), title="Current Weather Data.", description="\u200B")
    emb.add_field(name="Humidity",
                  value=f"``` {w.humidity} %  ```", inline=True)
    emb.add_field(name="Feels Like",
                  value=f"``` {w.feelsLike} {w.unitText}  ```", inline=True)
    emb.add_field(name="\u200B", value="\u200B", inline=False)
    emb.add_field(name="Wind Speed",
                  value=f"``` {w.windSpeed} m/s  ```", inline=True)
    emb.add_field(name="Wind Direction",
                  value=f"``` {w.windDirection}  ```", inline=True)
    emb.add_field(name="\u200B", value="\u200B", inline=False)
    emb.add_field(name="Sunrise at",
                  value=f"<t:{w.sunriseAt}:t>", inline=True)
    emb.add_field(name="Sunset at",
                  value=f"<t:{w.sunsetAt}:t>", inline=True)
    emb.set_footer(text="Like the bot? A review or a vote on my Top.gg profile would be appreciated. Thank You UwU",
                   icon_url="https://em-content.zobj.net/thumbs/120/toss-face/342/red-heart_2764-fe0f.png")
    emb.set_image('attachment://imf.png')
    return emb


def permissionChecker(member: nextcord.Member) -> list:
    t = ""
    condi = True
    if not member.guild_permissions.view_channel:
        t += "- To view that channel \n"
        condi = False
    if not member.guild_permissions.send_messages:
        t += "- To send message in that channel \n"
        condi = False
    if not member.guild_permissions.manage_channels:
        t += "- To manage that channel \n"
        condi = False
    if not member.guild_permissions.manage_messages:
        t += "- To manage messages in that channel \n"
        condi = False

    if condi:
        return [True, nextcord.Embed(color=nextcord.Colour.gold(), title="MISSING PERMISSIONS !", description=f"I don't have the following permissions please make sure I have them before runnning this command \n ```{t}```")

                .add_field(name="\u200B", value="\u200B", inline=False)
                .add_field(name="**Having problems with permission settings?**", value='One simple way of fixing this would be to kick the bot and again reinviting it but make sure to keep all the checks marked of the permission list so as to make sure the bot has those required permissions server-wide.')
                .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')]
    else:
        return [False, nextcord.Embed(color=nextcord.Colour.gold(), title="MISSING PERMISSIONS !", description=f"I don't have the following permissions please make sure I have them before runnning this command \n ```{t}```")
                .add_field(name="\u200B", value="\u200B", inline=False)
                .add_field(name="**Having problems with permission settings?**", value='One simple way of fixing this would be to kick the bot and again reinviting it but make sure to keep all the checks marked of the permission list so as to make sure the bot has those required permissions server-wide.')
                .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')]


def logTheCommand(interaction: nextcord.Interaction):
    print("[INFO] ",datetime.now().ctime(),
          f" RAN COMMAND {interaction.application_command.name} in {interaction.guild} by {interaction.user}")



def directoryManager():
    if (os.path.exists('servers') == False):
        os.mkdir('servers')
    if (os.path.exists('users') == False):
        os.mkdir('users')
    if (os.path.exists('subscriptions') == False):
        os.mkdir('subscriptions')
    if (os.path.exists('subimages') == False):
        os.mkdir('subimages')




def weatherUpdater():
    lis = os.listdir('subscriptions')
    for u in lis:
        for subs in os.listdir(f'subscriptions/{u}'):
            
            try:
                k = accountManager.getSubInfo(channelId=subs[:-5], serverID=u)
            except Exception as e:
                print('[ERROR] INVALID FORMAT. ',e)
                continue;

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


def weatherInit():
    count = 0
    lis = os.listdir('subscriptions')
    for u in lis:
        for subs in os.listdir(f'subscriptions/{u}'):
            
            try:
                k = accountManager.getSubInfo(channelId=subs[:-5], serverID=u)
            except Exception as e:
                print('[ERROR] INVALID FORMAT. ',e)
                continue;
            
            
            if "weatherCondition" in k.keys():
                pass
            else:
                count+=1
                with open(f'subscriptions/{u}/{subs}', 'r') as fp:
                    try:
                        data = json.load(fp)
                        wea = {
                            "temp":"gg",
                            "weatherCondition":"gg",
                            "icon":"gg",
                            "humidity":"gg",
                            "windSpeed":"gg",
                            "windDirection":"gg",
                            "feelsLike":"gg",
                            "sunriseAt":"gg",
                            "sunsetAt":"gg",
                            "location":"gg"
                        }
                        forecas = weatherService.forecast(lat_lon= f'{data.get("lat")},{data.get("lon")}',units=data.get('units'))
                        with open(f'{fp.name}', "w") as oute:
                            data.update(forecas)
                            data.update(wea)
                            json.dump(data,oute)
                                    
                    except Exception as e:
                        print('[ERROR] Failed to write data to json files of subscriptions.... Details: ',e)
    if count > 0:
        print(f'[INFO] {count} files were initialized...')
    else:
        print('[INFO] No files needed to be initialized....')







if __name__ == '__main__':
    
    print(r""" 
             _    _ ______ _      _____ ____   _____   _      ____   _____  _____   __  
            | |  | |  ____| |    |_   _/ __ \ / ____| | |    / __ \ / ____|/ ____|  \ \ 
            | |__| | |__  | |      | || |  | | (___   | |   | |  | | |  __| (___   (_) |
            |  __  |  __| | |      | || |  | |\___ \  | |   | |  | | | |_ |\___ \    | |
            | |  | | |____| |____ _| || |__| |____) | | |___| |__| | |__| |____) |  _| |
            |_|  |_|______|______|_____\____/|_____/  |______\____/ \_____|_____/  (_) |
                                                                                    /_/ 
                                                                            
                                                                                                                    
                                                                                                                    
                                                                                                                    
    
    """)

    
    print("[INFO] Starting the BOT please wait...")
    print("[INFO] Creating important directories...")
    directoryManager()
    print("[SUCCESS] Directory Mananger job done!")
    print("[INFO] Checking for empty weather.jsons and re-initializing them...")
    weatherInit()
    print("[SUCCESS] Weather initialization done...")
    print("[INFO] Updating weather data in local files...")
    weatherUpdater()
    print("[SUCCESS] Weather data of subs updated...")
    print("[INFO] Connecting to Discord API...")
    bot.run(os.getenv("botToken"))



