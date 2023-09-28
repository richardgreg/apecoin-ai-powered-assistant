# AI-powered Discord Bot

An AI-powered discord bot built for the ApeCoin DAO Discord.

## How to set up

* Initialize a bot @ [discord developer portal](https://discord.com/developers/applications)
* Give your bot a name, profile pic and set preferences.
* Go to OAuth2 URL Generator and in scope, select `bot`, `application.command`; in permissions, select only `send messages`
* Follow the generated link and use it to invite the bot to your channel
* Set up variable in `.env`
* `python3 -m venv .venv`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`
* `python bot.py`

## Usage

Inside of your discord server, `/apegpt What is ApeCoin DAO?`
