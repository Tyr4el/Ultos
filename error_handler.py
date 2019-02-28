import discord
from discord.ext import commands
import constants
import sys
import traceback


class ErrorHandlerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = commands.UserInputError
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"{constants.error_string} {ctx.command} was not found.")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"{constants.error_string} {ctx.command} has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f"{constants.error_string} {ctx.command} can not be used in a Private "
                                             f"Message.")
            except:
                pass

        elif isinstance(error, commands.NotOwner):
            return await ctx.send(f"{constants.error_string} You must be the owner of the server to perform this "
                                  f"command.")

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"{constants.error_string} Missing required argument: {error.param.name}")

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"{constants.error_string} You do not have permissions to do this.")

        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))
