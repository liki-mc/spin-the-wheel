# Spin the wheel discord bot

This repository uses a [discord bot template](https://github.com/Tibo-Ulens/discord-bot-template).

See the [discord.py docs](https://discordpy.readthedocs.io/en/stable/) for more info

## Running

Make a file called `discord_token.txt` in the folder `secrets/` and paste your discord token into it.

Create and activate a venv with `python -m venv venv` and `source venv/bin/activate`.

Install the requirements with `pip install -r requirements.txt`.

This library requires ffmpeg to be installed on your system. On linux you can install it with `sudo apt install ffmpeg`.

Run `python -m bot` to start the bot.

## Commands

This bot implements a command `spin` and `quickspin` which both spin a wheel and chooses a random option. Options for the spin can be seperated using a newline, a semicolon, a comma or using command line syntax.
