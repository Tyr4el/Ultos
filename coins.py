import discord
from discord.ext import commands
import constants
import asyncpg


class CoinsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def give(self, ctx, user: discord.Member, amount: int = None):
        if user is not None and amount is not None:
            if user.bot:
                await ctx.send(f"{constants.error_string} Bots cannot have coins!")
                return
            try:
                await self.bot.db.add_coins(user.id, amount)
                await self.bot.db.remove_coins(ctx.author.id, amount)
                await ctx.send(f"{constants.success_string} **{ctx.author.name}** gave **{amount}** Coins to "
                               f"**{user.name}**")
            except asyncpg.DataError as e:
                print(e)
        else:
            await ctx.send(f"{constants.error_string} Usage: `$give <@user> [amount]`")

    # Credit
    @commands.command(aliases=['addcoins'])
    @commands.guild_only()
    @commands.has_any_role("Boss Man", "Happy Fun Time Police")
    async def credit(self, ctx, user: discord.Member, amount: int = None):
        """Adds coins to a users bank/ledger"""
        if user is not None and amount is not None:
            # If the user is a bot
            if user.bot:
                await ctx.send(f"{constants.error_string} Bots cannot have coins!")
                return
            try:
                await self.bot.db.add_coins(user.id, amount)
                await ctx.send(f"{constants.success_string} Added **{amount}** Coins to **{user.name}**")
            except asyncpg.DataError as e:
                print(e)
        else:
            await ctx.send(f"{constants.error_string} Usage: `$debit <@user> [amount]`")

    # Debit
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role('Happy Fun Time Police', "Boss Man")
    async def debit(self, ctx, user: discord.Member, amount: int = None):
        """Removes the specified coin's from the user"""
        if user is not None and amount is not None:
            # If the user is a bot
            if user.bot:
                await ctx.send(f"{constants.error_string} Bots cannot have coins!")
                return
            try:
                await self.bot.db.remove_coins(user.id, amount)
                await ctx.send(f"{constants.success_string} Removed **{amount}** Coins from **{user.name}**")
            except asyncpg.DataError as e:
                print(e)
                await ctx.send(f"{constants.error_string} **{user.name}** does not have enough coins.  Use `$ledger` "
                               f"to check the number of coins that they have.")
        else:
            await ctx.send(f"{constants.error_string} Usage: `$debit <@user> [amount]`")

    # Set
    @commands.command(aliases=['setcoins'])
    @commands.guild_only()
    @commands.has_any_role('Happy Fun Time Police', "Boss Man")
    async def set(self, ctx, user: discord.Member, amount: int = None):
        """Sets the specified user's coins to the specified amount"""
        if user is not None and amount is not None:
            if user.bot:
                await ctx.send(f"{constants.error_string} Bots cannot have coins!")
                return
            await self.bot.db.set_coins(user.id, amount)
            await ctx.send(f"{constants.success_string} Coins set to **{amount}** for **{user.name}**")
        else:
            await ctx.send(f"{constants.error_string} Usage: `$set <@user> [amount]`")

    # Wallet
    @commands.command(aliases=['coins', 'getcoins'])
    @commands.guild_only()
    async def wallet(self, ctx, user: discord.Member):
        """Checks the specified user's coin ledger"""
        if user is not None:
            users_coins = await self.bot.db.get_coins(user.id)
            await ctx.send(f"**{user.name}** has **{users_coins}** Fun "
                           f"Time Coins!")
        else:
            await ctx.send(f"{constants.error_string} Usage: `$ledger <@user>`")

    # Leaderboard
    @commands.command(aliases=['leaders', 'lb'])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        leaders = await self.bot.db.get_all_users_coins()
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
