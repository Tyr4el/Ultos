import discord
from discord.ext import commands
import constants
import logging
import aiohttp
import traceback
from datetime import datetime
import sys
import database

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = constants.TOKEN


class MyBotClass(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.db = database.DatabaseConnector('coins_ledger')
        self.session = aiohttp.ClientSession()
        self.start_time = datetime.now()
        super().__init__(*args, **kwargs)


bot = MyBotClass(command_prefix="$")
bot.remove_command("help")

extensions = ['basic', 'admin', 'anime', 'fun', 'games', 'error_handler', 'coins', 'events']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()


bot.run(TOKEN, bot=True, reconnect=True)
