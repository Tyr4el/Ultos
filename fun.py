import discord
import random
from discord.ext import commands
import constants


class FunCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Simple ping test"""
        await ctx.send("Pong!")

    # Roll
    @commands.command(aliases=['dice', 'rolldice', 'diceroll'])
    @commands.guild_only()
    async def roll(self, ctx, *, dice_type: int = 0):
        """Rolls either a 4, 6, 8, 10 or 20 sided dice (specified by user) and returns the result"""
        valid_dice = [4, 6, 8, 10, 20]
        if dice_type != 0 and dice_type in valid_dice:
            dice_roll = random.randint(1, dice_type)
            await ctx.send(f"**{ctx.author.name}** rolled a **d{dice_type}** and got {dice_roll}!")
        elif dice_type not in valid_dice:
            await ctx.send(f"{constants.error_string} {dice_type} is not a valid dice type!")
        else:
            await ctx.send(f"{constants.error_string} Pick a number to roll dice!")

    # Choose
    @commands.command(aliases=['choices'])
    @commands.guild_only()
    async def choose(self, ctx, *, choices=""):
        """Chooses between comma delimited options"""
        if choices == "":
            await ctx.send(f"{constants.error_string} No choices given!")
            return

        choices_split = choices.split(',')
        if len(choices_split) > 1:
            random_choice = random.choice(choices_split).strip()
            await ctx.send(f"🤔 | **{ctx.author.name}**, I pick **{random_choice}**!")
        else:
            await ctx.send("You need to enter more than one option!")

    @commands.command()
    @commands.guild_only()
    async def f(self, ctx, *, respects_string=None):
        """Pays respects to something"""
        if respects_string is None:
            await ctx.send(
                f"{constants.error_string} Please pay your respects by entering something after the command")
        else:
            bot_message = await ctx.send(f"Press :regional_indicator_f: to pay respects to {respects_string}")
            await discord.Message.add_reaction(bot_message, '🇫')

    @commands.command()
    @commands.guild_only()
    async def palindrome(self, ctx, *, word=None):
        """Checks if the given word is a palindrome"""
        if word is None:
            await ctx.send(f"{constants.error_string} Please enter a word to check!")
        elif word.lower() == word.lower()[::-1]:
            await ctx.send(f"**{ctx.author.name}**, your word, {word} is a palindrome!")
        else:
            await ctx.send(f"**{ctx.author.name}**, your word, {word} is not a palindrome!")


def setup(bot):
    bot.add_cog(FunCog(bot))
