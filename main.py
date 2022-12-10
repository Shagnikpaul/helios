from dotenv import load_dotenv
from nextcord.ext import commands, tasks
from nextcord import SlashOption
import nextcord
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

load_dotenv()
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!w', intents=intents, help_command=None)
accountManager = accountManager()


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
async def on_application_command_error(interaction: nextcord.Interaction, error):
    error = getattr(error, "original", error)

    if isinstance(error, CallableOnCooldown):
        await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title=f"WAIT FOR {error.retry_after} SECONDS.",
                                                                                               description=f"This command is rate-limited per user. Please wait before you can use it again.")
                                                        .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png'),ephemeral=True)

    else:
        raise error


@bot.command(name='help')
async def helps(ctx: commands.Context):
    print(datetime.now().ctime(),
          f" RAN COMMAND {ctx.command.name} in {ctx.author.guild.name} by {ctx.author.name}#{ctx.author.discriminator}")
    emb1 = nextcord.embeds.Embed(color=nextcord.Colour.teal(
    ), title='Helios Bot Command list.', description='Here is a list of commands supported by Helios Bot.')
    emb1.add_field(name="\u200B", value="\u200B", inline=False)
    emb1.add_field(name='Setup API key for server use.',
                   value='``` /server-setup ```', inline=False)
    emb1.add_field(name="\u200B", value="\u200B", inline=False)
    emb1.add_field(name='Setup your own location and specify the units in which you want to get the weather forecast in.',
                   value='``` /user-setup ```', inline=False)
    emb1.add_field(name="\u200B", value="\u200B", inline=False)
    emb1.add_field(name='Get your weather.',
                   value='``` /weather ```', inline=False)
    emb1.add_field(name="\u200B", value="\u200B", inline=False)
    emb1.add_field(name='Delete your profile you had created previously',
                   value='``` /delete-user-data ```', inline=False)
    emb1.add_field(name="\u200B", value="\u200B", inline=False)
    emb1.add_field(name='Delete the API_KEY you had assigned for the server use.',
                   value='``` /delete-server-data ```', inline=False)
    emb1.add_field(name="\u200B", value="\u200B", inline=False)
    emb1.add_field(name='Get info about the bot and it\'s developer.',
                   value='``` /about-me ```', inline=False)
    emb1.add_field(name="\u200B", value="\u200B", inline=False)
    emb2 = nextcord.embeds.Embed(color=nextcord.Colour.yellow(
    ), title="NOTE", description="Helios only supports slash commands.")
    await ctx.send(embeds=[emb2, emb1])


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=nextcord.Game(name="/weather"))
    # lo.start()


@bot.event
async def on_guild_remove(guild: nextcord.Guild):
    if accountManager.serverAccountExists(serverID=str(guild.id)):
        accountManager.delServer(serverID=(str)(guild.id))
        print(datetime.now().ctime(),
              f" DELETED SERVER DATA OF {guild.name} ({guild.id})")
    else:
        print(datetime.now().ctime(),
              f" I LEFT (NO EXISTING SERVER DATA) {guild.name} ({guild.id})")


@bot.slash_command(name='help-helios', description="List all available commands of Helios bot with description.", guild_ids=bot.default_guild_ids)
async def helpCommand(interaction: nextcord.Interaction):
    logTheCommand(interaction=interaction)
    await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.teal(), title='Helios Bot Command list.', description='Here is a list of commands supported by Helios Bot.')
                           .add_field(name="\u200B", value="\u200B", inline=False)
                           .add_field(name='Setup API key for server use.', value='``` /server-setup ```', inline=False)
                           .add_field(name="\u200B", value="\u200B", inline=False)
                           .add_field(name='Setup your own location and specify the units in which you want to get the weather forecast in.', value='``` /user-setup ```', inline=False)
                           .add_field(name="\u200B", value="\u200B", inline=False)
                           .add_field(name='Get your weather.', value='``` /weather ```', inline=False)
                           .add_field(name="\u200B", value="\u200B", inline=False)
                           .add_field(name='Delete your profile you had created previously', value='``` /delete-user-data ```', inline=False)
                           .add_field(name="\u200B", value="\u200B", inline=False)
                           .add_field(name='Delete the API_KEY you had assigned for the server use.', value='``` /delete-server-data ```', inline=False)
                           .add_field(name="\u200B", value="\u200B", inline=False)
                           .add_field(name='Get info about the bot and it\'s developer.', value='``` /about-me ```', inline=False)
                           .add_field(name="\u200B", value="\u200B", inline=False), ephemeral=True)


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
                               .add_field(name="First run the following command.", value="``` /delete-user {not added} ```", inline=False)
                               .add_field(name="Then run this one.", value="``` /user-setup ```", inline=False), ephemeral=True)
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
    await interaction.send(embed=emb, ephemeral=True)


@bot.slash_command(name="delete-user-data", description="Delete your location profile from the server.", guild_ids=bot.default_guild_ids)
async def delUser(interaction: nextcord.Interaction):
    logTheCommand(interaction=interaction)
    if (accountManager.userAccountExists(userID=str(interaction.user.id))):
        accountManager.delUser(userID=str(interaction.user.id))
        await interaction.edit_original_message(embed=nextcord.embeds.Embed(colour=nextcord.Colour.green(), title="SUCCESS.", description="Your location profile has been deleted from the server.")
                                                .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/322/check-mark-button_2705.png'), ephemeral=True)
    else:
        await interaction.edit_original_message(embed=nextcord.embeds.Embed(colour=nextcord.Colour.brand_red(), title="ERROR.", description="You don't have any profile setup yet.")
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
    await interaction.send(embed=nextcord.embeds.Embed(colour=nextcord.Colour.blue(), title="Fetching your data...", description="Please wait it might take some time.")
                           .set_thumbnail('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/clockwise-vertical-arrows_1f503.png'))
    if (accountManager.serverAccountExists(str(interaction.guild_id))):
        if (accountManager.userAccountExists(userID=str(interaction.user.id))):
          
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
        emb = weatherEmbBuilder(interaction=interaction)
        file = nextcord.File(
            f'users/{interaction.user.id}/imf.png', filename='imf.png')
        await interaction.edit_original_message(embed=emb, file=file)
        # await interaction.send(embed=nextcord.embeds.Embed(color=nextcord.Colour.gold(), title="WARNING.",
        #                                                    description="No existing server configuration was found. Please get a OpenWeatherMap API key by creating a new account (or existing). Then run the server setup command.")
        #                        .set_thumbnail(url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/319/warning_26a0-fe0f.png')
        #                        .add_field(name="Run the following command.", value="``` /server-setup ```", inline=False), ephemeral=True)


def weatherEmbBuilder(interaction: nextcord.Interaction):
    keyUsed=""
    u = accountManager.getUserData(userID=str(interaction.user.id))
    if accountManager.serverAccountExists(str(interaction.guild_id)):
        keyUsed="Server API_KEY"
        w = weatherService.weatherServices(accountManager.getServerData(
            serverID=str(interaction.guild_id)).get("API_KEY"), u.get('lat'), u.get('lon'), u.get('units'))
    else:
        keyUsed="Global API_KEY"
        w = weatherService.weatherServices(
            os.getenv('weatherKey'), u.get('lat'), u.get('lon'), u.get('units'))
    w.getData()
    imageGenerator.createImage(
        (w.temp+w.unitText), w.weatherCondition, w.icon, w.location, str(interaction.user.id))
    emb = nextcord.embeds.Embed(colour=nextcord.Colour.random(
    ), title="Current Weather Data.", description="\u200B")
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
    emb.set_footer(text=f"{keyUsed} was used.",
                   icon_url="http://openweathermap.org/img/wn/02d@2x.png")
    emb.set_image('attachment://imf.png')
    return emb


def logTheCommand(interaction: nextcord.Interaction):
    print(datetime.now().ctime(),
          f" RAN COMMAND {interaction.application_command.name} in {interaction.guild} by {interaction.user}")


if __name__ == '__main__':
    if (os.path.exists('servers') == False):
        os.mkdir('servers')
    if (os.path.exists('users') == False):
        os.mkdir('users')
    bot.run(os.getenv("botToken"))
