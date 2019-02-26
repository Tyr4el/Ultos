import discord
from discord.ext import commands
import aiohttp
import constants
import asyncio
import traceback
import sys


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Shutdown
    @commands.command(aliases=['close', 'leave', 'shut', 'end'])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts the bot down"""
        await ctx.send(':wave: Bye :wave: bye!')
        await self.bot.session.close()
        await self.bot.close()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = None):
        """Bans the specified user"""
        await member.ban(reason=reason)
        await ctx.send(f"User **{member.name}** was banned (Reason: {reason})")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = None):
        """Kicks the specified user"""
        await member.kick(reason=reason)
        await ctx.send(f"User **{member.name}** was kicked (Reason: {reason})!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, messages: int):
        """Deletes the specified number of messages from the channel"""
        channel = ctx.channel
        try:
            deleted = await channel.purge(limit=messages)
            await ctx.send(f"{constants.success_string} {len(deleted)} messages deleted!", delete_after=3)
        except Exception as e:
            print(e)
            await ctx.send(f"{constants.error_string} {e} Messages were not deleted.  Try again.")


def setup(bot):
    bot.add_cog(AdminCog(bot))
