# bot.py
import discord
import config
import db
from localization import translations

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def get_translation(language, key):
    lang_translations = translations.get(language, translations['en'])
    if isinstance(lang_translations[key], dict):
        return lang_translations[key]
    else:
        return lang_translations[key]


async def generate_help_embed(language="en"):
    lang_translations = translations.get(language, translations['en'])

    embed = discord.Embed(title=lang_translations.get("help_title", "Commands Help"), color=0x00ff00)
    embed.set_thumbnail(url="https://example.com/your_image.png")

    commands = [
        ("add", "add_description"),
        ("show", "show_description"),
        ("delete", "delete_description"),
        ("allsnippets", "allsnippets_description"),
    ]

    for command, description_key in commands:
        name_translation = lang_translations.get(f"{command}_command", f"{config.praefix}{command}")
        description_translation = lang_translations.get(description_key, "No description available.")

        embed.add_field(name=name_translation, value=description_translation, inline=False)

    embed.set_footer(text=lang_translations.get("help_footer", "Use these commands to manage code snippets."))

    return embed


@client.event
async def on_ready():
    print(f"{client.user} is ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{config.praefix}add'):
        parts = message.content.split(
            maxsplit=3)
        if len(parts) == 4:
            try:
                name = parts[1]
                code_lang = parts[2]
                code = parts[3]
                if db.insert_snippet(name, code_lang, code):
                    embed = discord.Embed(title=get_translation("en", "success_title"),
                                          description=get_translation("en", "success_description"), color=0x00ff00)
                    formatted_code = f"```{code_lang}\n{code}\n```"
                    embed.add_field(name=name, value=formatted_code, inline=False)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=get_translation("en", "error_title"),
                                          description=get_translation("en", "error_description")["db"], color=0xff0000)
                    await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title=get_translation("en", "error_title"),
                                      description=get_translation("en", "error_description")["db"], color=0xff0000)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=get_translation("en", "error_title"),
                                  description=get_translation("en", "error_description")["params"], color=0xff0000)
            await message.channel.send(embed=embed)

    if message.content.startswith(f'{config.praefix}show'):
        parts = message.content.split()
        if len(parts) == 2:
            try:
                name = parts[1]
                result = db.retrieve_snippet(name)
                if result:
                    code_lang, code = result
                    embed = discord.Embed(title=name, color=0x00ff00)
                    formatted_code = f"```{code_lang}\n{code}\n```"
                    embed.description = formatted_code
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=get_translation("en", "error_title"), description=get_translation("en", "error_description")["not_found"], color=0xff0000)
                    await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title=get_translation("en", "error_title"), description=get_translation("en", "error_description")["db"], color=0xff0000)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=get_translation("en", "error_title"), description=get_translation("en", "error_description")["not_specified"], color=0xff0000)
            await message.channel.send(embed=embed)

    if message.content.startswith(f'{config.praefix}delete'):
        parts = message.content.split()
        if len(parts) == 2:
            try:
                name = parts[1]
                if db.delete_snippet(name):
                    embed = discord.Embed(title=get_translation("en", "success_title"), description=get_translation("en", "delete_success").format(name=name), color=0x00ff00)
                else:
                    embed = discord.Embed(title=get_translation("en", "error_title"), description=get_translation("en", "delete_error"), color=0xff0000)
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title=get_translation("en", "error_title"), description=get_translation("en", "error_description")["db"], color=0xff0000)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=get_translation("en", "error_title"), description=get_translation("en", "error_description")["not_specified"], color=0xff0000)
            await message.channel.send(embed=embed)

    if message.content.startswith(f'{config.praefix}allsnippets'):  # !showall
        try:
            snippet_names = db.get_all_snippet_names()
            if snippet_names:
                embed = discord.Embed(title=get_translation("en", "show_all_snippets_title"), color=0x00ff00)
                embed.description = "\n".join(snippet_names)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=get_translation("en", "error_title"),
                                      description=get_translation("en", "show_all_snippets_empty"), color=0xff0000)
                await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title=get_translation("en", "error_title"),
                                  description=get_translation("en", "error_description")["db"], color=0xff0000)
            await message.channel.send(embed=embed)

    if message.content.startswith(f'{config.praefix}info'):
        help_embed = await generate_help_embed()
        await message.channel.send(embed=help_embed)
# start
client.run(config.discordToken)
