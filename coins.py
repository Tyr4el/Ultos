import discord
from discord.ext import commands
import constants
import sqlite3


class CoinsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['give', 'givecoins', 'addcoins'])
    @commands.guild_only()
    @commands.has_any_role("Boss Man", "Happy Fun Time Police")
    async def credit(self, ctx, user: discord.Member, amount: int = None):
        """Adds coins to a users bank/ledger"""
        if user is not None and amount is not None:
            print(user, amount)
            # If the user is a bot
            if user.bot:
                await ctx.send(f"{constants.error_string} Bots cannot have coins!")
                return
            try:
                self.bot.db.add_coins(user.id, amount)
                await ctx.send(f"{constants.success_string} Added **{amount}** Coins to **{user.name}**")
            except sqlite3.Error as e:
                print(e)
        else:
            await ctx.send(f"{constants.error_string} Usage: `$debit <@user> [amount]`")

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role('Happy Fun Time Police', "Boss Man")
    async def debit(self, ctx, user: discord.Member, amount: int = None):
        """Removes the specified coin's from the user"""
        if user is not None and amount is not None:
            print(user, amount)
            # If the user is a bot
            if user.bot:
                await ctx.send(f"{constants.error_string} Bots cannot have coins!")
                return
            try:
                self.bot.db.remove_coins(user.id, amount)
                await ctx.send(f"{constants.success_string} Removed **{amount}** Coins from **{user.name}**")
            except sqlite3.Error as e:
                print(e)
                await ctx.send(f"{constants.error_string} **{user.name}** does not have enough coins.  Use `$ledger` "
                               f"to check the number of coins that they have.")
        else:
            await ctx.send(f"{constants.error_string} Usage: `$debit <@user> [amount]`")

    @commands.command(aliases=['setcoins'])
    @commands.guild_only()
    @commands.has_any_role('Happy Fun Time Police', "Boss Man")
    async def set(self, ctx, user: discord.Member, amount: int = None):
        """Sets the specified user's coins to the specified amount"""
        if user is not None and amount is not None:
            if user.bot:
                await ctx.send(f"{constants.error_string} Bots cannot have coins!")
                return
            self.bot.db.set_coins(user.id, amount)
            await ctx.send(f"{constants.success_string} Coins set to **{amount}** for **{user.name}**")
        else:
            await ctx.send(f"{constants.error_string} Usage: `$set <@user> [amount]`")

    @commands.command(aliases=['coins', 'getcoins'])
    @commands.guild_only()
    async def wallet(self, ctx, user: discord.Member):
        """Checks the specified user's coin ledger"""
        if user is not None:
            await ctx.send(f"**{user.name}** has **{self.bot.db.get_coins(user.id)}** Fun "
                           f"Time Coins!")
        else:
            await ctx.send(f"{constants.error_string} Usage: `$ledger <@user>`")

    @commands.command(aliases=['leaders', 'lb'])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        leaders = self.bot.db.get_all_users_coins()
        joined_leaders = ""
        index = 1
        for leader, coins in leaders:
            joined_leaders += f"**{index}.** {leader} - {coins}\n"
            index += 1

        embed = discord.Embed(
            title="Coins Leaderboard",
            description=f"Top 10 Leaders in Coins\n{joined_leaders}",
            color=discord.Colour.gold()
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CoinsCog(bot))
