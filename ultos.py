import discord
from discord.ext import commands
import constants
import logging
import character
import re
import aiohttp
import traceback
from datetime import timezone
from datetime import datetime
import json
import os
import sys
import sqlite
import sqlite3

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = constants.TOKEN

bot = commands.Bot(command_prefix='$')
bot.session = aiohttp.ClientSession()
bot.start_time = datetime.now(tz=timezone.utc)
bot.db = sqlite.SqlLiteConnector.start_connection('coins_ledger.db')
bot.remove_command("help")


extensions = ['basic', 'admin', 'anime', 'fun', 'games', 'error_handler', 'coins', 'events']
unloaded_extensions = []


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()


bot.run(TOKEN, bot=True, reconnect=True)
