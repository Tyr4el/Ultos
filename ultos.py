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


extensions = ['basic', 'admin', 'anime', 'fun', 'games', 'error_handler', 'coins']


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(532936314631225346)
    bot_spam_channel = bot.get_channel(541969928606056462)
    embed = discord.Embed(
        title="Welcome!",
        description=f"Welcome **{member.mention}** to Happy Fun Time Express!  Upon joining the server, you've been "
        f"awarded 1,000 Fun Time Coins!  Use these on the different games that I have!  Use `$help` to see what "
        f"commands there are.  Oh, and don't be a dick.  kthxbai.",
        color=discord.Colour.dark_gold()
    )

    try:
        bot.db.set_default_coins(member.id, member.name, coins=1000)
        await bot_spam_channel.send(f"{constants.success_string} Member ({member.id}) joined the server!  1000 coins "
                                    f"have been added.")
    except sqlite3.Error as e:
        print(e)
        await bot_spam_channel.send(f"{constants.error_string} Member ({member.id}) already exists.  Coins not added.")

    await member.send(embed=embed)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(541969928606056462)
    bot.db.remove_user_from_db(member.id, member.name, coins=None)
    await channel.send(f"{constants.success_string} {member.name} left the server.  Removed coins.")


@bot.event
# TODO: Don't print stuff every time the bot loads and don't update db every time
async def on_ready():
    channel = bot.get_channel(541969928606056462)
    print(f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n")
    await bot.change_presence(activity=discord.Game(name='Use $help'))
    print(f"Successfully logged in and booted...!")
    guild_members = bot.get_all_members()
    for member in guild_members:
        if not member.bot:
            bot.db.set_default_coins(member.id, member.name, coins=1000)


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()


bot.run(TOKEN, bot=True, reconnect=True)
