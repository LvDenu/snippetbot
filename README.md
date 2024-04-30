# SnippetBot README

## Overview

SnippetBot is a Discord bot designed to store, display, and delete code snippets. The bot uses a MySQL database to store the snippets and the discord.py library to interact on Discord.

## Configuration

The bot's configuration can be done in two separate files:

### `config.py`

In this file, you can set the main configuration parameters:

- `discordToken`: The token of your Discord bot application. You can get this token from the Discord Developer Portal page of your application.
- `prefix`: The prefix for your commands. By default, it is `!`.

### `db.py`

This file contains the configuration for connecting to your MySQL database. You need to specify your hostname or IP address, your username, your password, and the name of your database.

## Commands

The bot supports the following commands:

- `!add <name> <code_lang> <code>`: Adds a new snippet to the database. `name` is the name of the snippet, `code_lang` is the programming language of the snippet, and `code` is the code of the snippet.
- `!show <name>`: Displays the snippet with the given name.
- `!delete <name>`: Deletes the snippet with the given name from the database.
- `!allsnippets`: Shows all available code snippets.

## Note

Please note that deleting a snippet from the database cannot be undone. So be careful when using the delete command.

Enjoy coding with SnippetBot!

## Starting the Bot

To start the bot, simply run the `main.py` file. Make sure you have Python and the required libraries installed.

```bash
python main.py
