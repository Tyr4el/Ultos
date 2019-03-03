import discord
from discord.ext import commands
import aiohttp

class GameDeal:
    def __init__(self):


class ITADCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def deals(self, region, *, game_name):