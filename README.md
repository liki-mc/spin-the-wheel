# Spin the wheel discord bot

This repository uses a [discord bot template](https://github.com/Tibo-Ulens/discord-bot-template).

See the [discord.py docs](https://discordpy.readthedocs.io/en/stable/) for more info

## Running

Make a file called `discord_token.txt` in the folder `secrets/` and paste your discord token into it.

Run `docker compose up --build` to start the bot.

## Managing dependencies

Create and activate a venv with `python -m venv venv` and `source venv/bin/activate`.

Install [poetry](https://python-poetry.org/docs/#installation)

Add dependencies with `poetry add <dep>` and make sure they're installed with `poetry install`

## Commands

This bot implements a command `spin` which spins a wheel and chooses a random option. Options for the spin can be seperated using a newline, a semicolon, a comma or using command line syntax.
