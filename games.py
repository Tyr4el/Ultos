import asyncio
import itertools
import random

import constants
import discord
from discord.ext import commands

FRUIT_WHEEL = ['🍒', '🍇', '🍐', '🍎', '🍋', '🍈', '🍑', '🍊']


def beats(a, b):
    return ((a == 'rock' and b == 'scissors') or
            (a == 'paper' and b == 'rock') or
            (a == 'scissors' and b == 'paper'))


class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # RPS
    @commands.command()
    @commands.guild_only()
    async def rps(self, ctx, person_challenged: discord.Member, bet_amount: int = 0):
        """Challenges a member to rock, paper, scissors betting a specified number of Fun Time Coins"""

        game_emoji = {'rock': '<:rock:542385712557850635>', 'paper': '📰', 'scissors': '✂'}
        game_choices = ['rock', 'paper', 'scissors']
        author_coins = await self.bot.db.get_coins(ctx.author.id)
        challenger_coins = await self.bot.db.get_coins(person_challenged.id)

        # Check definitions for the wait_for calls used below
        def reaction_check(reaction, user):
            return user == person_challenged and str(reaction.emoji) == "⬆"

        def dm_check(m):
            person_challenged_locked = False
            initiator_locked = False
            if m.author == ctx.author and m.content.lower() in game_choices and person_challenged_locked is not True:
                initiator_locked = True
                return True
            if m.author == person_challenged and m.content.lower() in game_choices and initiator_locked is not True:
                person_challenged_locked = True
                return True
            else:
                return False

        # If both players do not have enough coins
        if author_coins < bet_amount and challenger_coins < bet_amount:
            await ctx.send(f"{constants.error_string} Both players do not have enough coins.  Game not started.")
        # If the author does not have enough coins
        elif author_coins < bet_amount:
            await ctx.send(f"{constants.error_string} **{ctx.author.name}** does not have enough coins.  "
                           f"Game not started.")
        # If the challenger does not have enough coins
        elif challenger_coins < bet_amount:
            await ctx.send(f"{constants.error_string} **{person_challenged.name}** does not have enough coins.  "
                           f"Game not started.")
        # If the challenger specified is the author
        elif ctx.author == person_challenged:
            await ctx.send(f"{constants.error_string} You cannot play yourself!")
        # If the challenger and bet_amount are specified in the command arguments do this
        elif person_challenged and bet_amount:
            bot_message = await ctx.send(f"{person_challenged.mention} has been challenged by **{ctx.author.name}** to a game "
                                         f"of Rock Paper, Scissors!  The wager is **{bet_amount}** Fun Time Coins!\n\n"
                                         f"{constants.warning_string} **{person_challenged.name}**, you now have 15 seconds "
                                         f"to respond with ⬆ to this message to confirm your entry.")
            await bot_message.add_reaction("⬆")
            # Start the first check of the reaction on the message to initiate the game
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=reaction_check)
            except asyncio.TimeoutError:
                await ctx.send(f"{constants.error_string} **{person_challenged.name}**, time has run out.")
            # If the user that was challenged responds with the correct reaction in the proper time
            else:
                await ctx.send(f"{constants.success_string} **{person_challenged.name}** has accepted **{ctx.author.name}**'s "
                               f"request!  Game on!\n"
                               f"**{person_challenged.mention}** and **{ctx.author.mention}**, please send me a DM with your "
                               f"choice of 'Rock', 'Paper', or 'Scissors'")
                await person_challenged.send("'Rock', 'Paper' or 'Scissors'?")
                await ctx.author.send("'Rock', 'Paper' or 'Scissors'?")
                # Start the second check of if the bot was DM'd by the two users
                try:
                    msg_person1 = await self.bot.wait_for('message', timeout=30.0, check=dm_check)
                    msg_person2 = await self.bot.wait_for('message', timeout=30.0, check=dm_check)
                except asyncio.TimeoutError:
                    await ctx.send(f"{constants.error_string} Responses were not sent from both parties.  Game "
                                   f"cancelled.")
                # If both users respond, do the things here
                else:
                    person_1_emoji = game_emoji[msg_person1.content.lower()]
                    person_2_emoji = game_emoji[msg_person2.content.lower()]
                    # Check if the first person who DM'd the bot won
                    if beats(msg_person1.content.lower(), msg_person2.content.lower()):
                        await ctx.send(f"{person_1_emoji} vs. {person_2_emoji}: **{msg_person1.author.name}** wins "
                                       f"**{bet_amount}** Fun Time Coins!!")
                        await self.bot.db.add_coins(str(msg_person1.author.id), bet_amount)
                        await self.bot.db.remove_coins(str(msg_person2.author.id), bet_amount)
                    # Check if the second person who DM'd the bot won
                    elif beats(msg_person2.content.lower(), msg_person1.content.lower()):
                        await ctx.send(f"{person_2_emoji} vs. {person_1_emoji}: **{msg_person2.author.name}** wins "
                                       f"**{bet_amount}** Fun Time Coins!!")
                        await self.bot.db.add_coins(str(msg_person2.author.id), bet_amount)
                        await self.bot.db.remove_coins(str(msg_person1.author.id), bet_amount)
                    # Otherwise it's a draw
                    else:
                        await ctx.send(f"{person_1_emoji} vs. {person_2_emoji}: It's a draw!")
        # If the command is entered incorrectly
        else:
            await ctx.send(f"{constants.error_string} Usage: `$rps <@user> [bet_amount]`")

    def calculate_slots_bonus(self, n: int) -> int:
        """
        Calculates the winning bonus for the slots game

        follows curve generated from set {1,2,4,10,...}
        see https://www.wolframalpha.com/input/?i=1,2,4,10,... for the specifics

        Args:
            n (int): integer value. **must** be less than 5**


        Raises:
            ValueError: input value `n` >= 5 (outside domain, avoids div 0 error.)
        Returns:
            int: calculated coefficient
        """
        if n > 5:
            raise ValueError("domain of function is (-inf, 5) exclusive.")

        numerator = -2 * (n + 1)
        denominator = n - 5

        # return integer division of a/b
        return numerator // denominator
    # Slots
    @commands.command()
    @commands.guild_only()
    async def slots(self, ctx, bet_amount: int = 0):
        """Plays the slots for a specified bet amount"""
        authors_coins = await self.bot.db.get_coins(ctx.author.id)
        if authors_coins < bet_amount:
            await ctx.send(f"{constants.error_string} **{ctx.author.name}** does not have enough coins.  "
                           f"Game not started.")
        if not bet_amount:
            await ctx.send(f"{constants.error_string} You need to enter a bet amount!")
            return  # bail out
        else:  # author has enough coins, and has specified a bet

            # steal their coins
            await self.bot.db.remove_coins(ctx.author.id, bet_amount)

            results = [fruit for fruit in random.choices(FRUIT_WHEEL, k=5)]
            joined_results = " ".join(results)
            grouped_fruits = [len(list(g)) for k, g in itertools.groupby(results)]
            max_grouped_fruits = max(grouped_fruits)

            await ctx.send(f"**{ctx.author.name}** bet **{bet_amount}** Fun Time Coins to spin the slot machine!")
            await ctx.send(joined_results)

            if max_grouped_fruits >= 2 <= 5:
                # calculate our multiple, evaluating the function at n-1
                multiple = self.calculate_slots_bonus(max_grouped_fruits - 1)
                await ctx.send(f"**{ctx.author.name}** wins with **{max_grouped_fruits}**"
                               f"in a row! they win **{multiple}x** their original!")
                await self.bot.db.add_coins(ctx.author.id, bet_amount * multiple)

            else:
                await ctx.send(f"**{ctx.author.name}** did not win.")


def setup(bot):
    bot.add_cog(GamesCog(bot))
