import discord
import mysql.connector

##### configuration #####

discordToken = ""

intents = discord.Intents.default() #don´t touch
intents.message_content = True #don´t touch
client = discord.Client(intents=intents) #don´t touch


mydb = mysql.connector.connect(
    host="localhost", #your host or IP addresse
    user="your-username", #your database username
    password="your-password", #your database password
    database="snippetbot" #import snippetbot.sql
)

serverid = "", #your discord server id
adminrole = "" #role id for use the bot



##### Events #####

@client.event
async def on_ready():
    print(f"Wir haben uns als {client.user} eingeloggt!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hallo!")




##### Start ######
client.run(discordToken)