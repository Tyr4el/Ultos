import discord
from discord.ext import commands
import constants
import asyncpg


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        bot_spam_channel = self.bot.get_channel(541969928606056462)
        embed = discord.Embed(
            title="Welcome!",
            description=f"Welcome **{member.mention}** to Happy Fun Time Express!  Upon joining the server, you've been "
            f"awarded 1,000 Fun Time Coins!  Use these on the different games that I have!  Use `$help` to see what "
            f"commands there are.  Oh, and don't be a dick.  kthxbai.",
            color=discord.Colour.dark_gold()
        )

        await member.send(embed=embed)

        try:
            await self.bot.db.set_default_coins(member.id, member.name, coins=1000)
            await bot_spam_channel.send(
                f"{constants.success_string} Member ({member.id}) joined the server!  1000 coins "
                f"have been added.")
        except asyncpg.UniqueViolationError:
            await bot_spam_channel.send(
                f"{constants.error_string} Member ({member.id}) already exists.  Coins not added.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        bot_spam_channel = self.bot.get_channel(541969928606056462)
        await self.bot.db.remove_user_from_db(member.id)
        await bot_spam_channel.send(f"{constants.success_string} {member.name} left the server.  Removed coins.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.db.start_connection()
        print(f"\n\nLogged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}\n")
        await self.bot.change_presence(activity=discord.Game(name='Use $help'))
        print(f"Successfully logged in and booted...!")
        guild_members = self.bot.get_all_members()
        for member in guild_members:
            if not member.bot:
                try:
                    await self.bot.db.set_default_coins(member.id, member.name, coins=1000)
                except asyncpg.UniqueViolationError:
                    print(f"User {member.name} already exists in database...skipping.")


def setup(bot):
    bot.add_cog(EventsCog(bot))
