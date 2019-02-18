import discord
from discord.ext import commands
import traceback
import sys
import constants
from datetime import timezone
from datetime import datetime
import psutil


class BasicCog:
    def __init__(self, bot):
        self.bot = bot

    # Help
    @commands.command()
    async def help(self, ctx):
        """The command to get help with this bot"""
        author = ctx.author

        embed = discord.Embed(
            title='Help',
            color=discord.Colour.orange()
        )
        for command in self.bot.commands:
            embed.add_field(name=command.name, value=command.help, inline=False)

        await author.send(embed=embed)

    # Roles - List all roles of server
    @commands.command(aliases=['rolelist', 'listroles'])
    @commands.guild_only()
    async def roles(self, ctx):
        """Lists all the available roles that can be added by users"""
        role_list = [role.name for role in ctx.message.guild.roles if role.name.startswith("Playing: ")]
        separator = "\n"
        roles = separator.join(role_list)
        embed = discord.Embed(
            title=f"{ctx.message.guild.name}'s Roles",
            description=roles,
            color=discord.Colour.gold()
        )

        await ctx.send(embed=embed)

    # Role - Add role to user
    @commands.command(aliases=['addrole', 'roleadd'])
    @commands.guild_only()
    async def role(self, ctx, *, role_name: str = None):
        """Adds an available role to the user"""
        author = ctx.author
        role = discord.utils.get(author.guild.roles, name=role_name)
        if role_name is None:
            await ctx.send(f"{constants.error_string} Missing required role name.")
        elif role is None:
            await ctx.send(f"{constants.error_string} Role: `{role_name}` does not exist")
        else:
            await author.add_roles(role)
            await ctx.send(f"{constants.success_string} Role: `{role}` has been added")

    @commands.command(aliases=['roleremove', 'removerole'])
    @commands.guild_only()
    async def remove(self, ctx, *, role_name: str = None):
        """Removes an existing role from a user"""
        author = ctx.author
        role = discord.utils.get(author.guild.roles, name=role_name)
        if role_name is None:
            await ctx.send(f"{constants.error_string} Missing required role name.")
        elif role is None:
            await ctx.send(f"{constants.error_string} Role: `{role_name}` does not exist")
        else:
            await author.remove_roles(role)
            await ctx.send(f"{constants.success_string} Role: `{role}` has been removed")

    @commands.command(aliases=['statistics'])
    @commands.guild_only()
    async def stats(self, ctx):
        """Gets usage statistics for the system the bot is running on"""
        uptime = datetime.now(tz=timezone.utc) - self.bot.start_time
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_count = psutil.cpu_count()
        used_mem = psutil.virtual_memory().used
        free_mem = psutil.virtual_memory().free
        total_mem = psutil.virtual_memory().total
        percent_mem_used = (used_mem / total_mem) * 100
        embed = discord.Embed(
            title=f"**{self.bot.user.name} Statistics**",
            color=discord.Colour.dark_green()
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Uptime", value=uptime, inline=False)
        embed.add_field(name="CPU Utilization", value=f"{cpu_percent:.2f}%", inline=True)
        embed.add_field(name="CPU Count", value=cpu_count, inline=True)
        embed.add_field(name="Free Memory", value=free_mem, inline=True)
        embed.add_field(name="Used Memory", value=used_mem, inline=True)
        embed.add_field(name="Memory Utilization", value=f"{percent_mem_used:.2f}%", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BasicCog(bot))
