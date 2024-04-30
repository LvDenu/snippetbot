import discord
import mysql.connector
import json

##### configuration #####

discordToken = "" #token from your discord application bot
praefix = "!" # begin for your command DEFAULT: !

intents = discord.Intents.default() #don´t touch
intents.message_content = True #don´t touch
client = discord.Client(intents=intents) #don´t touch


mydb = mysql.connector.connect(
    host="localhost", #your host or IP addresse
    user="", #your database username
    password="", #your database password
    database="snippetbot" #import snippetbot.sql DONT TOUCH
)

serverid = "", #your discord server id
adminrole =     #role id for use the bot must be a number



##### events #####

@client.event
async def on_ready():
    print(f"{client.user} is ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{praefix}add'): #!add <name> <py> <snippet>
        parts = message.content.split()
        if len(parts) == 4:
            try:
                name = (parts[1])
                code_lang = (parts[2])
                code = (parts[3])
                cursor = mydb.cursor()

                sql = "INSERT INTO snippetbot (name, code_lang, code) VALUES (%s, %s, %s)"
                val = (name,code_lang,code)
                embed = discord.Embed(title="succes", description="your code was created", color=0x00ff00)
                formatted_code = f"```{code_lang}\n{code}\n```"
                embed.add_field(name=name, value=formatted_code, inline=False)
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="error", description="database error", color=0xff0000)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="error", description="you need <name> <code_lang> <code>", color=0xff0000)
            await message.channel.send(embed=embed)

    if message.content.startswith(f'{praefix}show'):  # !show <name>
        parts = message.content.split()
        if len(parts) == 2:
            try:
                name = (parts[1])
                cursor = mydb.cursor()

                sql = "SELECT code_lang, code FROM snippetbot WHERE name = %s"
                val = (name,)
                cursor.execute(sql, val)
                result = cursor.fetchone()

                if result:
                    code_lang, code = result
                    embed = discord.Embed(title=name, color=0x00ff00)
                    formatted_code = f"```{code_lang}\n{code}\n```"
                    embed.description = formatted_code
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="error", description="code not found", color=0xff0000)
                    await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="error", description="database error", color=0xff0000)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="error", description="you need <name>", color=0xff0000)
            await message.channel.send(embed=embed)


##### Start ######
client.run(discordToken)